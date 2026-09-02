#!/usr/bin/env python3
"""
Importa dados reais do Google Maps para a landing page da Don Chacon.

O que ele traz:
  - avaliações (mantém somente as de 5 estrelas) -> assets/js/data.js
  - fotos do perfil do Google                     -> assets/img/galeria/
  - fachada em Street View                        -> assets/img/hero/

Como usar:
    export GOOGLE_MAPS_API_KEY="sua-chave"
    python3 scripts/importar-google.py

A chave precisa ter habilitadas, no Google Cloud, as APIs:
    Places API (New)  e  Street View Static API
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

RAIZ      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALERIA   = os.path.join(RAIZ, "assets", "img", "galeria")
HERO      = os.path.join(RAIZ, "assets", "img", "hero")
DATA_JS   = os.path.join(RAIZ, "assets", "js", "data.js")

# Barbearia Don Chacon — Av. Cerro Azul, 1990, Maringá/PR
CID_A, CID_B = 0x94ECD1C3ED1D432B, 0xECA9292C4CBAAE7D
LAT, LNG     = -23.4446587, -51.9328383
MAX_FOTOS    = 12


def place_id():
    raw = bytes([0x0A, 0x12, 0x09]) + CID_A.to_bytes(8, "little") + bytes([0x11]) + CID_B.to_bytes(8, "little")
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def pegar(url, headers=None, binario=False):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=45) as r:
        dados = r.read()
    return dados if binario else json.loads(dados)


def detalhes(chave):
    campos = ",".join([
        "displayName", "formattedAddress", "nationalPhoneNumber", "rating",
        "userRatingCount", "reviews", "photos", "regularOpeningHours", "websiteUri",
    ])
    url = ("https://places.googleapis.com/v1/places/%s?languageCode=pt-BR&regionCode=BR"
           % place_id())
    return pegar(url, {"X-Goog-Api-Key": chave, "X-Goog-FieldMask": campos})


def salvar(caminho, conteudo):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "wb") as f:
        f.write(conteudo)


def baixar_fotos(lugar, chave):
    """Tenta as fotos do perfil. Devolve a lista de arquivos salvos."""
    salvos = []
    for i, foto in enumerate(lugar.get("photos", [])[:MAX_FOTOS], 1):
        nome = foto.get("name")
        if not nome:
            continue
        url = ("https://places.googleapis.com/v1/%s/media?maxHeightPx=1600&key=%s"
               % (nome, urllib.parse.quote(chave)))
        try:
            dados = pegar(url, binario=True)
        except Exception as e:
            print("  foto %02d falhou: %s" % (i, e))
            continue
        if not dados.startswith(b"\xff\xd8") and not dados.startswith(b"\x89PNG"):
            print("  foto %02d nao veio como imagem, ignorada" % i)
            continue
        ext = ".jpg" if dados.startswith(b"\xff\xd8") else ".png"
        arq = os.path.join(GALERIA, "google-%02d%s" % (i, ext))
        salvar(arq, dados)
        atrib = (foto.get("authorAttributions") or [{}])[0].get("displayName", "")
        salvos.append(("assets/img/galeria/google-%02d%s" % (i, ext), atrib))
        print("  foto %02d salva (%d KB)" % (i, len(dados) // 1024))
    return salvos


def baixar_streetview(chave):
    """Fachada em Street View. Sai direto de maps.googleapis.com, sem redirecionamento."""
    salvos = []
    for i, heading in enumerate((0, 90, 180, 270), 1):
        url = ("https://maps.googleapis.com/maps/api/streetview"
               "?size=640x640&location=%s,%s&heading=%d&pitch=0&fov=90&source=outdoor&key=%s"
               % (LAT, LNG, heading, urllib.parse.quote(chave)))
        try:
            dados = pegar(url, binario=True)
        except Exception as e:
            print("  street view %d graus falhou: %s" % (heading, e))
            continue
        if not dados.startswith(b"\xff\xd8"):
            continue
        arq = os.path.join(HERO, "fachada-%d.jpg" % i)
        salvar(arq, dados)
        salvos.append("assets/img/hero/fachada-%d.jpg" % i)
        print("  street view %03d graus salvo (%d KB)" % (heading, len(dados) // 1024))
    return salvos


def js_lista(itens, indent="  "):
    return "\n".join(indent + json.dumps(i, ensure_ascii=False) + "," for i in itens).rstrip(",")


def escrever_data_js(fotos, heros, avaliacoes):
    fonte = open(DATA_JS, encoding="utf-8").read()

    if fotos:
        bloco = "window.DC_GALERIA = [\n" + "\n".join(
            "  { src: %s, alt: %s }," % (json.dumps(src, ensure_ascii=False),
                                         json.dumps(alt or "Barbearia Don Chacon, Maringá", ensure_ascii=False))
            for src, alt in fotos).rstrip(",") + "\n];"
        fonte = re.sub(r"window\.DC_GALERIA = \[.*?\];", bloco, fonte, flags=re.S)

    if heros:
        bloco = "window.DC_HERO = [\n" + js_lista(heros) + "\n];"
        fonte = re.sub(r"window\.DC_HERO = \[.*?\];", bloco, fonte, flags=re.S)

    if avaliacoes:
        linhas = []
        for a in avaliacoes:
            linhas.append(
                "  {\n"
                "    nome: %s,\n"
                "    data: %s,\n"
                "    texto: %s\n"
                "  }," % (json.dumps(a["nome"], ensure_ascii=False),
                          json.dumps(a["data"], ensure_ascii=False),
                          json.dumps(a["texto"], ensure_ascii=False)))
        bloco = "window.DC_AVALIACOES = [\n" + "\n".join(linhas).rstrip(",") + "\n];"
        fonte = re.sub(r"window\.DC_AVALIACOES = \[.*?\];", bloco, fonte, flags=re.S)

    open(DATA_JS, "w", encoding="utf-8").write(fonte)


def main():
    chave = os.environ.get("GOOGLE_MAPS_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else "")
    if not chave:
        sys.exit("Defina GOOGLE_MAPS_API_KEY ou passe a chave como primeiro argumento.")

    print("Place ID:", place_id())
    try:
        lugar = detalhes(chave)
    except urllib.error.HTTPError as e:
        sys.exit("Places API respondeu %s:\n%s" % (e.code, e.read().decode("utf-8", "replace")[:600]))

    print("Local: %s — nota %s (%s avaliações)" % (
        lugar.get("displayName", {}).get("text", "?"),
        lugar.get("rating", "?"), lugar.get("userRatingCount", "?")))

    print("\nAvaliações:")
    avaliacoes = []
    for r in lugar.get("reviews", []):
        if r.get("rating") != 5:
            continue
        texto = (r.get("originalText") or r.get("text") or {}).get("text", "").strip()
        if not texto:
            continue
        avaliacoes.append({
            "nome": (r.get("authorAttribution") or {}).get("displayName", ""),
            "data": r.get("relativePublishTimeDescription", ""),
            "texto": texto,
        })
        print("  5 estrelas — %s" % avaliacoes[-1]["nome"])
    print("  %d avaliação(ões) de 5 estrelas" % len(avaliacoes))

    print("\nFotos do perfil:")
    fotos = baixar_fotos(lugar, chave)
    if not fotos:
        print("  nenhuma foto do perfil baixada")

    print("\nStreet View:")
    heros = baixar_streetview(chave)

    escrever_data_js(fotos, heros, avaliacoes)
    print("\nassets/js/data.js atualizado.")
    print("Confira o site e apague os arquivos .svg de placeholder que sobraram.")


if __name__ == "__main__":
    main()

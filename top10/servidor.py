"""
TOP 10 - SERVIDOR
Trabalho 02 de Sistemas Operacionais: jogo com troca de mensagens e memória compartilhada.

Como no modo Top 10 do Topzi: sai uma lista de 10 itens em ordem e os jogadores,
um de cada vez, tentam adivinhar os itens. O número do item é a pontuação
(o nº 1 é o óbvio e vale 1; o nº 10 é o mais difícil e vale 10).

O ESTADO do jogo fica numa memória compartilhada (objeto `Estado`) usada por
várias threads ao mesmo tempo:
  - uma thread por jogador (recebe as mensagens daquele jogador);
  - a thread principal (controla a vez e o fim da partida).
O acesso é protegido por um Lock (exclusão mútua) e uma Condition
(a thread principal dorme até chegar a jogada de quem está na vez).

Uso:  python servidor.py [num_jogadores] [porta]
      ex.: python servidor.py 2 5000
"""
import random
import socket
import sys
import threading

from listas import LISTAS
from palpite import acha_item, normalizar

HOST = "0.0.0.0"


# ----------------------------------------------------------------------
# MEMÓRIA COMPARTILHADA
# ----------------------------------------------------------------------
class Estado:
    def __init__(self):
        self.lock = threading.Lock()                # exclusão mútua
        self.cond = threading.Condition(self.lock)  # espera / aviso entre threads
        self.jogadores = {}     # id -> {"nome", "sock", "pontos"}
        self.vez = 1            # id de quem está jogando agora
        self.itens = []         # itens da lista ("Nome|apelido|...")
        self.achados = {}       # índice do item -> id de quem achou
        self.tentados = set()   # chutes errados já feitos (não pune de novo)
        self.jogada = None      # ("CHUTE", texto) ou ("PASSA",) vinda de quem está na vez
        self.encerrado = False


estado = Estado()


# ----------------------------------------------------------------------
# TROCA DE MENSAGENS:  CODIGO|campo1|campo2|...\n
# ----------------------------------------------------------------------
def limpar(txt):
    return txt.replace("|", "/").replace(";", ",").replace("=", "-").replace("\n", " ").strip()


def enviar(sock, *campos):
    try:
        sock.sendall(("|".join(str(c) for c in campos) + "\n").encode("utf-8"))
    except OSError:
        pass


def broadcast(*campos):
    with estado.lock:
        socks = [j["sock"] for j in estado.jogadores.values()]
    for s in socks:
        enviar(s, *campos)


def nome_item(i):
    return estado.itens[i].split("|")[0]


def placar():
    with estado.lock:
        return ";".join(f"{jid}={j['nome']}={j['pontos']}" for jid, j in estado.jogadores.items())


# ----------------------------------------------------------------------
# THREAD DE CADA JOGADOR: só grava a jogada na memória compartilhada
# ----------------------------------------------------------------------
def atender(jid, sock):
    try:
        for linha in sock.makefile("r", encoding="utf-8"):
            p = linha.rstrip("\n").split("|")
            with estado.cond:                       # região crítica
                if jid != estado.vez or estado.jogada is not None:
                    continue                        # não é a vez dele: ignora
                if p[0] == "CHUTE" and len(p) > 1 and p[1].strip():
                    estado.jogada = ("CHUTE", limpar(p[1]))
                elif p[0] == "PASSA":
                    estado.jogada = ("PASSA",)
                elif p[0] == "SAIR":
                    estado.encerrado = True
                estado.cond.notify_all()            # acorda a thread principal
    except OSError:
        pass
    with estado.cond:
        estado.encerrado = True
        estado.cond.notify_all()


# ----------------------------------------------------------------------
# PARTIDA (thread principal)
# ----------------------------------------------------------------------
def esperar_jogada():
    with estado.cond:
        estado.cond.wait_for(lambda: estado.jogada is not None or estado.encerrado)
        jogada, estado.jogada = estado.jogada, None
        return None if estado.encerrado else jogada


def partida(lista):
    with estado.lock:
        estado.itens = lista["itens"]
        estado.achados = {}
        estado.tentados = set()
        ids = sorted(estado.jogadores)
        estado.vez = random.choice(ids)   # quem começa é sorteado
        total = len(estado.itens)

    broadcast("LISTA", lista["titulo"], lista["fonte"], total)
    passes_seguidos = 0
    anunciar = True   # avisar todo mundo de quem é a vez?

    while True:
        with estado.lock:
            vez = estado.vez
            nome = estado.jogadores[vez]["nome"]
            achados = ";".join(f"{i + 1}={nome_item(i)}" for i in sorted(estado.achados))
        if anunciar:
            broadcast("VEZ", vez, nome, achados)
        anunciar = True

        jogada = esperar_jogada()
        if jogada is None:
            return "Um jogador saiu da partida."

        if jogada[0] == "PASSA":
            passes_seguidos += 1
            broadcast("PASSOU", vez, nome)
            if passes_seguidos >= len(ids):
                return "Todo mundo passou a vez."
        else:
            texto = jogada[1]
            with estado.lock:
                i = acha_item(estado.itens, texto)
                chave = normalizar(texto)
                if i is not None and i in estado.achados:
                    quem = estado.jogadores[estado.achados[i]]["nome"]
                    aviso = f"\"{nome_item(i)}\" já foi achado por {quem}. Chute outro."
                elif i is None and chave in estado.tentados:
                    aviso = f"\"{texto}\" já foi chutado e não está na lista. Chute outro."
                else:
                    aviso = None
            if aviso:  # não conta como jogada: o mesmo jogador tenta de novo
                enviar(estado.jogadores[vez]["sock"], "DENOVO", aviso)
                anunciar = False
                continue

            passes_seguidos = 0
            if i is not None:  # acertou: o número do item é a pontuação
                with estado.lock:
                    estado.achados[i] = vez
                    estado.jogadores[vez]["pontos"] += i + 1
                    item = nome_item(i)
                    acabou = len(estado.achados) == total
                broadcast("ACERTO", vez, nome, i + 1, item, placar())
                if acabou:
                    return "Acharam os 10 itens!"
            else:
                with estado.lock:
                    estado.tentados.add(chave)
                broadcast("ERRO", vez, nome, texto)

        # passa a vez (variável "vez" circula entre os jogadores)
        with estado.lock:
            estado.vez = ids[(ids.index(estado.vez) + 1) % len(ids)]


def escolher_lista():
    print("\nListas:")
    for i, l in enumerate(LISTAS, 1):
        print(f"  {i:2}. {l['titulo']}")
    op = input("Escolha a lista (1-10, Enter = sortear): ").strip()
    if op.isdigit() and 1 <= int(op) <= len(LISTAS):
        return LISTAS[int(op) - 1]
    return random.choice(LISTAS)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    if not 2 <= n <= 8:
        print("Número de jogadores: de 2 a 8.")
        return

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, porta))
    srv.listen(n)
    print(f"[SERVIDOR] Porta {porta}. Esperando {n} jogador(es)...")

    while len(estado.jogadores) < n:
        sock, end = srv.accept()
        p = sock.makefile("r", encoding="utf-8").readline().rstrip("\n").split("|")
        nome = (limpar(p[1]) if len(p) > 1 and p[0] == "NOME" else "") or "Jogador"
        with estado.lock:
            jid = len(estado.jogadores) + 1
            estado.jogadores[jid] = {"nome": nome, "sock": sock, "pontos": 0}
        enviar(sock, "BEMVINDO", jid, n)
        broadcast("MSG", f"{nome} entrou ({jid}/{n})")
        print(f"[SERVIDOR] {nome} conectou de {end[0]} (id {jid})")
        threading.Thread(target=atender, args=(jid, sock), daemon=True).start()

    lista = escolher_lista()
    print(f"[SERVIDOR] Lista: {lista['titulo']}")
    motivo = partida(lista)

    revelada = ";".join(f"{i}={it.split('|')[0]}" for i, it in enumerate(lista["itens"], 1))
    broadcast("FIM", motivo, revelada, placar())
    print(f"[SERVIDOR] Fim: {motivo}  Placar: {placar()}")
    for j in estado.jogadores.values():
        j["sock"].close()
    srv.close()


if __name__ == "__main__":
    main()

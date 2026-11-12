"""
Comparação de palpites, simples como no Topzi:
ignora acentos, maiúsculas, pontuação e plural, e aceita apelidos ("SP", "BH").
Cada item da lista é "Nome|apelido|apelido"; "~palavra" vale se aparecer no palpite.
"""
import re
import unicodedata


def normalizar(texto):
    """'São Paulo!' -> 'sao paulo'"""
    t = unicodedata.normalize("NFD", str(texto))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def singular(texto):
    """'bananas' -> 'banana' (plural e singular valem o mesmo)"""
    return " ".join(re.sub(r"(oes|aes|es|s)$", "", w) if len(w) > 3 else w for w in texto.split())


def acha_item(itens, texto):
    """Devolve o índice (0 a 9) do item que o palpite acertou, ou None."""
    g = normalizar(texto)
    if not g:
        return None
    for i, item in enumerate(itens):
        for nome in item.split("|"):
            if nome.startswith("~"):                      # palavra-chave
                if f" {normalizar(nome[1:])} " in f" {g} ":
                    return i
            elif singular(normalizar(nome)) == singular(g):  # nome ou apelido
                return i
    return None

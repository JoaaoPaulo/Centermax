"""
TOP 10 - SERVIDOR
Trabalho 02 de Sistemas Operacionais: jogo com troca de mensagens e memória compartilhada.

O servidor guarda o ESTADO do jogo numa área de memória compartilhada
(objeto `Estado`) que é acessada por várias threads ao mesmo tempo:
  - uma thread por jogador conectado (recebe as mensagens daquele jogador);
  - a thread principal (conduz as rodadas).
O acesso a essa memória é protegido por um Lock (exclusão mútua) e uma
Condition (para a thread principal dormir até todos responderem).

Uso:  python servidor.py [num_jogadores] [porta]
      ex.: python servidor.py 3 5000
"""
import random
import socket
import sys
import threading

from temas import TEMAS

HOST = "0.0.0.0"
VIDAS_INICIAIS = 5


# ----------------------------------------------------------------------
# MEMÓRIA COMPARTILHADA
# ----------------------------------------------------------------------
class Estado:
    """Dados do jogo que todas as threads enxergam."""

    def __init__(self):
        self.lock = threading.Lock()               # exclusão mútua
        self.cond = threading.Condition(self.lock)  # espera/aviso entre threads
        self.jogadores = {}   # id -> {"nome", "sock"}
        self.vez = 1          # id do capitão da rodada
        self.rodada = 0
        self.vidas = VIDAS_INICIAIS
        self.pontos = 0
        self.numeros = {}     # id -> número secreto (1..10) da rodada
        self.respostas = {}   # id -> texto da resposta
        self.palpite = None   # id -> número chutado pelo capitão
        self.encerrado = False


estado = Estado()


# ----------------------------------------------------------------------
# TROCA DE MENSAGENS
# Toda mensagem é uma linha de texto:  CODIGO|campo1|campo2|...\n
# ----------------------------------------------------------------------
def limpar(txt):
    """Tira os caracteres que quebrariam o protocolo."""
    return txt.replace("|", "/").replace(";", ",").replace("=", "-").replace("\n", " ").strip()


def enviar(sock, *campos):
    msg = "|".join(str(c) for c in campos) + "\n"
    try:
        sock.sendall(msg.encode("utf-8"))
    except OSError:
        pass


def broadcast(*campos):
    with estado.lock:
        socks = [j["sock"] for j in estado.jogadores.values()]
    for s in socks:
        enviar(s, *campos)


# ----------------------------------------------------------------------
# THREAD DE CADA JOGADOR
# ----------------------------------------------------------------------
def atender(jid, sock):
    leitor = sock.makefile("r", encoding="utf-8")
    try:
        for linha in leitor:
            partes = linha.rstrip("\n").split("|")
            codigo = partes[0]

            if codigo == "RESP" and len(partes) >= 2:
                with estado.cond:  # entra na região crítica
                    if jid != estado.vez and jid not in estado.respostas:
                        estado.respostas[jid] = limpar(partes[1]) or "(em branco)"
                        estado.cond.notify_all()

            elif codigo == "PALPITE" and len(partes) >= 2:
                # formato: PALPITE|2=7;3=4  (jogador=numero)
                chute = {}
                for par in partes[1].split(";"):
                    if "=" in par:
                        a, b = par.split("=", 1)
                        if a.isdigit() and b.isdigit():
                            chute[int(a)] = int(b)
                with estado.cond:
                    if jid == estado.vez:
                        estado.palpite = chute
                        estado.cond.notify_all()
    except OSError:
        pass

    # jogador caiu: avisa a thread principal para encerrar
    with estado.cond:
        if not estado.encerrado:
            estado.encerrado = True
            estado.cond.notify_all()


# ----------------------------------------------------------------------
# LÓGICA DO JOGO (thread principal)
# ----------------------------------------------------------------------
def esperar(condicao):
    """Dorme até a condição ser verdadeira (ou o jogo acabar)."""
    with estado.cond:
        estado.cond.wait_for(lambda: condicao() or estado.encerrado)
        return not estado.encerrado


def jogar_rodada(tema, n):
    min_txt, max_txt = tema["min"], tema["max"]

    with estado.lock:
        estado.rodada += 1
        estado.respostas = {}
        estado.palpite = None
        outros = [j for j in estado.jogadores if j != estado.vez]
        sorteio = random.sample(range(1, 11), len(outros))
        estado.numeros = dict(zip(outros, sorteio))
        rodada, vez = estado.rodada, estado.vez
        capitao = estado.jogadores[vez]["nome"]

    # 1) avisa todo mundo de quem é a vez e qual o tema
    broadcast("RODADA", rodada, vez, capitao, tema["tema"], min_txt, max_txt)
    # 2) cada jogador recebe seu número secreto (só ele vê)
    for jid, num in estado.numeros.items():
        enviar(estado.jogadores[jid]["sock"], "NUM", num)

    # 3) espera todos (menos o capitão) responderem
    if not esperar(lambda: len(estado.respostas) == len(outros)):
        return False

    # 4) manda as respostas para todos, embaralhadas
    with estado.lock:
        itens = list(estado.respostas.items())
    random.shuffle(itens)
    lista = ";".join(f"{jid}={estado.jogadores[jid]['nome']}={txt}" for jid, txt in itens)
    broadcast("RESPOSTAS", lista)

    # 5) espera o palpite do capitão
    if not esperar(lambda: estado.palpite is not None):
        return False

    # 6) confere e pontua
    detalhes = []
    with estado.lock:
        for jid, real in estado.numeros.items():
            chute = estado.palpite.get(jid, 0)
            dif = abs(chute - real)
            if dif == 0:
                estado.pontos += 3
                res = "EXATO"
            elif dif <= 2:
                estado.pontos += 1
                res = "PERTO"
            else:
                estado.vidas -= 1
                res = "ERROU"
            detalhes.append(f"{estado.jogadores[jid]['nome']}={real}={chute}={res}")
        pontos, vidas = estado.pontos, estado.vidas
        # passa a vez para o próximo jogador (variável "vez")
        ids = sorted(estado.jogadores)
        estado.vez = ids[(ids.index(estado.vez) + 1) % len(ids)]

    broadcast("RESULTADO", ";".join(detalhes), pontos, vidas)
    return vidas > 0


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    if not 2 <= n <= 10:
        print("Número de jogadores deve ser entre 2 e 10.")
        return

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, porta))
    srv.listen(n)
    print(f"[SERVIDOR] Porta {porta}. Esperando {n} jogadores...")

    while len(estado.jogadores) < n:
        sock, end = srv.accept()
        leitor = sock.makefile("r", encoding="utf-8")
        linha = leitor.readline().rstrip("\n").split("|")
        nome = limpar(linha[1]) if len(linha) > 1 and linha[0] == "NOME" else "Anônimo"
        with estado.lock:
            jid = len(estado.jogadores) + 1
            estado.jogadores[jid] = {"nome": nome or f"Jogador{jid}", "sock": sock}
        enviar(sock, "BEMVINDO", jid, n)
        broadcast("MSG", f"{nome} entrou ({len(estado.jogadores)}/{n})")
        print(f"[SERVIDOR] {nome} conectou de {end[0]} (id {jid})")
        threading.Thread(target=atender, args=(jid, sock), daemon=True).start()

    temas = random.sample(TEMAS, len(TEMAS))
    for tema in temas:
        if not jogar_rodada(tema, n):
            break

    with estado.lock:
        pontos, vidas, motivo = estado.pontos, estado.vidas, estado.encerrado
    if motivo:
        broadcast("FIM", pontos, vidas, "Um jogador desconectou.")
    elif vidas <= 0:
        broadcast("FIM", pontos, vidas, "Acabaram as vidas!")
    else:
        broadcast("FIM", pontos, vidas, "Vocês completaram os 10 temas!")
    print(f"[SERVIDOR] Fim de jogo. Pontos: {pontos}  Vidas: {vidas}")

    for j in estado.jogadores.values():
        try:
            j["sock"].close()
        except OSError:
            pass
    srv.close()


if __name__ == "__main__":
    main()

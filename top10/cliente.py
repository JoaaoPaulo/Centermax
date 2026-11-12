"""
TOP 10 - CLIENTE (jogador)

Cada jogador roda um cliente. O cliente conversa com o servidor por socket,
trocando mensagens no formato  CODIGO|campo1|campo2|...
O cliente também guarda a variável "vez" (de quem é a vez de ser capitão),
atualizada pelas mensagens RODADA vindas do servidor.

Uso:  python cliente.py [ip_do_servidor] [porta]
      ex.: python cliente.py 127.0.0.1 5000
"""
import socket
import sys

LINHA = "=" * 50


def enviar(sock, *campos):
    sock.sendall(("|".join(str(c) for c in campos) + "\n").encode("utf-8"))


def ler_numero(prompt):
    while True:
        txt = input(prompt).strip()
        if txt.isdigit() and 1 <= int(txt) <= 10:
            return int(txt)
        print("  Digite um número de 1 a 10.")


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    nome = input("Seu nome: ").strip() or "Jogador"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, porta))
    leitor = sock.makefile("r", encoding="utf-8")
    enviar(sock, "NOME", nome)

    meu_id = 0
    vez = 0  # variável de turno, controlada pelas mensagens

    for linha in leitor:
        p = linha.rstrip("\n").split("|")
        cod = p[0]

        if cod == "BEMVINDO":
            meu_id = int(p[1])
            print(f"\nConectado! Você é o jogador {meu_id}. Esperando {p[2]} jogadores...")

        elif cod == "MSG":
            print(f"  * {p[1]}")

        elif cod == "RODADA":
            _, rodada, vez, capitao, tema, mn, mx = p
            vez = int(vez)
            print(f"\n{LINHA}\n RODADA {rodada}/10   |   Capitão: {capitao}")
            print(f" TEMA: {tema}")
            print(f"   1 = {mn}   ...   10 = {mx}\n{LINHA}")
            if vez == meu_id:
                print("Você é o CAPITÃO! Espere as respostas e adivinhe o número de cada um.")

        elif cod == "NUM":
            print(f"\n>>> Seu número secreto é: {p[1]} <<<")
            resp = input("Sua resposta (de acordo com o seu número): ")
            enviar(sock, "RESP", resp)
            print("Resposta enviada. Esperando os outros...")

        elif cod == "RESPOSTAS":
            itens = [x.split("=", 2) for x in p[1].split(";") if x]
            print("\nRESPOSTAS:")
            for jid, nm, txt in itens:
                print(f"  - {nm}: \"{txt}\"")
            if vez == meu_id:
                print("\nCapitão, qual o número (1-10) de cada um?")
                chutes = []
                for jid, nm, txt in itens:
                    n = ler_numero(f"  {nm} (\"{txt}\"): ")
                    chutes.append(f"{jid}={n}")
                enviar(sock, "PALPITE", ";".join(chutes))
            else:
                print("Esperando o capitão adivinhar...")

        elif cod == "RESULTADO":
            print("\nRESULTADO:")
            for item in p[1].split(";"):
                nm, real, chute, res = item.split("=")
                print(f"  {nm}: era {real}, capitão chutou {chute}  -> {res}")
            print(f"Pontos do time: {p[2]}   Vidas: {'<3 ' * int(p[3]) or '0'}")

        elif cod == "FIM":
            print(f"\n{LINHA}\n FIM DE JOGO! {p[3]}")
            print(f" Pontuação final do time: {p[1]}\n{LINHA}")
            break

    sock.close()


if __name__ == "__main__":
    main()

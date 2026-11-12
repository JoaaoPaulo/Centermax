"""
TOP 10 - CLIENTE (jogador)

Conversa com o servidor por socket, trocando mensagens  CODIGO|campo1|campo2|...
Guarda a variável "vez" (de quem é a vez), atualizada pelas mensagens VEZ;
só pede o palpite quando vez == meu_id.

Uso:  python cliente.py [ip_do_servidor] [porta]
      ex.: python cliente.py 127.0.0.1 5000
"""
import socket
import sys

LINHA = "=" * 56


def enviar(sock, *campos):
    sock.sendall(("|".join(str(c) for c in campos) + "\n").encode("utf-8"))


def mostrar_quadro(achados_txt, total):
    achados = dict(x.split("=", 1) for x in achados_txt.split(";") if x)
    for n in range(1, total + 1):
        print(f"  {n:2}. {achados.get(str(n), '?' * 6)}")


def mostrar_placar(txt, titulo="Placar"):
    linhas = [x.split("=") for x in txt.split(";") if x]
    linhas.sort(key=lambda x: -int(x[2]))
    print(f"{titulo}: " + "   ".join(f"{nm} {pts} pts" for _, nm, pts in linhas))


def pedir_palpite(sock):
    print("\n>>> SUA VEZ! Digite um palpite (ou /passar, /sair)")
    while True:
        txt = input("Palpite: ").strip()
        if txt == "/passar":
            enviar(sock, "PASSA")
        elif txt == "/sair":
            enviar(sock, "SAIR")
        elif txt:
            enviar(sock, "CHUTE", txt)
        else:
            continue
        return


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    porta = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

    nome = input("Seu nickname: ").strip() or "Jogador"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, porta))
    enviar(sock, "NOME", nome)

    meu_id, vez, total = 0, 0, 10

    for linha in sock.makefile("r", encoding="utf-8"):
        p = linha.rstrip("\n").split("|")
        cod = p[0]

        if cod == "BEMVINDO":
            meu_id = int(p[1])
            print(f"\nConectado! Você é o jogador {meu_id}. Esperando {p[2]} jogador(es)...")

        elif cod == "MSG":
            print(f"  * {p[1]}")

        elif cod == "LISTA":
            total = int(p[3])
            print(f"\n{LINHA}\n TOP {total}: {p[1]}\n Fonte: {p[2]}")
            print(f" O nº 1 vale 1 ponto ... o nº {total} vale {total} pontos.\n{LINHA}")

        elif cod == "VEZ":
            vez = int(p[1])
            print()
            mostrar_quadro(p[3], total)
            if vez == meu_id:
                pedir_palpite(sock)
            else:
                print(f"\nVez de {p[2]}...")

        elif cod == "DENOVO":
            print(f"  ! {p[1]}")
            pedir_palpite(sock)

        elif cod == "ACERTO":
            _, jid, nm, pos, item, plac = p
            quem = "Você" if int(jid) == meu_id else nm
            print(f"\n  ✔ {quem} acertou o nº {pos}: {item}  (+{pos} pontos)")
            mostrar_placar(plac)

        elif cod == "ERRO":
            quem = "Você" if int(p[1]) == meu_id else p[2]
            print(f"\n  ✘ {quem} chutou \"{p[3]}\": não está na lista.")

        elif cod == "PASSOU":
            print(f"\n  » {p[2]} passou a vez.")

        elif cod == "FIM":
            print(f"\n{LINHA}\n FIM DE JOGO! {p[1]}\n\n A lista completa era:")
            for item in p[2].split(";"):
                n, nm = item.split("=", 1)
                print(f"  {n:>2}. {nm}")
            print()
            mostrar_placar(p[3], " RESULTADO")
            print(LINHA)
            break

    sock.close()


if __name__ == "__main__":
    main()

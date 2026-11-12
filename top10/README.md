# Top 10 (terminal) - Trabalho 02 de Sistemas Operacionais

Jogo cooperativo para 2 a 10 jogadores, em Python, com **troca de mensagens via socket**
e **memória compartilhada protegida por exclusão mútua (Lock/Condition)**.

## Como jogar
1. Cada rodada tem um **capitão** (a "vez" passa de jogador em jogador).
2. Aparece um **tema** com uma escala, ex.: *"Um superpoder" - 1 = totalmente inútil ... 10 = o mais incrível*.
3. Cada jogador (menos o capitão) recebe um **número secreto de 1 a 10** e escreve uma resposta
   que combine com o número (se tirou 10, fala "voar"; se tirou 1, fala "espirrar glitter").
4. O capitão lê as respostas e chuta o número de cada um:
   - acertou em cheio: **+3 pontos**
   - errou por 1 ou 2: **+1 ponto**
   - errou por 3 ou mais: **o time perde 1 vida**
5. São **10 temas** (10 rodadas). O time começa com 5 vidas; se zerar, acaba o jogo.

## Como rodar
Precisa só de Python 3 (sem bibliotecas extras).

```bash
python servidor.py 3 5000        # 3 jogadores, porta 5000
python cliente.py 127.0.0.1 5000 # em outro terminal, um por jogador
```

Para gerar o executável (item "código com executável" do formulário):
```bash
pip install pyinstaller
pyinstaller --onefile servidor.py
pyinstaller --onefile cliente.py
```
Os `.exe` ficam na pasta `dist/`.

## Arquivos
| Arquivo | O que faz |
|---|---|
| `servidor.py` | Aceita os jogadores, guarda o estado na memória compartilhada e conduz as rodadas |
| `cliente.py` | Terminal de cada jogador: mostra o tema, pede resposta/palpite |
| `temas.py` | Os 10 temas |

## Protocolo de mensagens (notação própria)
Toda mensagem é uma linha de texto: `CODIGO|campo1|campo2|...`

| Direção | Mensagem | Significado |
|---|---|---|
| cliente -> servidor | `NOME\|Ana` | jogador se apresenta |
| servidor -> cliente | `BEMVINDO\|2\|3` | "você é o jogador 2, a partida tem 3" |
| servidor -> todos | `RODADA\|1\|2\|Beto\|Um superpoder\|inútil\|incrível` | rodada 1, **vez = 2** (capitão Beto), tema e escala |
| servidor -> um jogador | `NUM\|7` | número secreto só desse jogador |
| cliente -> servidor | `RESP\|voar` | resposta do jogador |
| servidor -> todos | `RESPOSTAS\|1=Ana=voar;3=Caio=ler mentes` | respostas embaralhadas |
| capitão -> servidor | `PALPITE\|1=8;3=6` | chute: jogador 1 = 8, jogador 3 = 6 |
| servidor -> todos | `RESULTADO\|Ana=7=8=PERTO;...\|4\|5` | resultado, pontos e vidas |
| servidor -> todos | `FIM\|15\|0\|Acabaram as vidas!` | fim de jogo |

A variável **`vez`** existe nos dois lados: no servidor (dono da verdade) e em cada cliente,
que a atualiza ao receber `RODADA`. O cliente compara `vez` com o próprio id para saber se é o capitão.
O servidor ignora `RESP` de quem é capitão e `PALPITE` de quem não é.

## Memória compartilhada e exclusão mútua
- O servidor cria **uma thread por jogador** (função `atender`) e a thread principal roda o jogo.
- Todas compartilham o objeto `Estado` (vez, rodada, pontos, vidas, números sorteados, respostas, palpite).
- Toda leitura/escrita nesse objeto acontece dentro de `with estado.lock` / `with estado.cond`
  (**região crítica**), então duas threads nunca mexem nele ao mesmo tempo
  (ex.: dois jogadores respondendo no mesmo instante).
- A thread principal usa `estado.cond.wait_for(...)` para **dormir** até todos responderem;
  cada thread de jogador, ao gravar a resposta, faz `notify_all()` para acordá-la.
  Isso evita espera ocupada (loop gastando CPU).
- Se um jogador desconecta, a thread dele marca `encerrado = True` e acorda a principal, que finaliza o jogo.

## Respostas prontas para o formulário
- **Nome do jogo:** Top 10
- **Linguagem:** Python 3 (socket + threading)
- **Explicação:** jogo cooperativo: a cada rodada um capitão; os outros recebem um número secreto de 1 a 10
  e respondem um tema de acordo com a intensidade do número; o capitão tenta adivinhar os números.
  10 temas, 5 vidas, o time soma pontos.
- **Como e quais informações são trocadas:** via socket TCP, mensagens de texto `CODIGO|campos` (tabela acima):
  nome, id, início de rodada com a vez/capitão e o tema, número secreto, respostas, palpite do capitão,
  resultado e fim de jogo.
- **Exclusão mútua:** o estado do jogo fica numa memória compartilhada entre as threads do servidor,
  protegida por `threading.Lock`; uma `threading.Condition` faz a thread principal esperar as respostas
  sem espera ocupada, e as threads dos jogadores a acordam com `notify_all()`.

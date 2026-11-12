# Top 10 (terminal) - Trabalho 02 de Sistemas Operacionais

O modo **Top 10** do Topzi, em terminal, para jogar em rede (2 a 8 jogadores), feito em **Python**.

## Como funciona o jogo
1. O servidor escolhe uma das **10 listas** (ex.: *"As 10 capitais brasileiras mais populosas"*).
2. Os itens começam escondidos (`??????`). Um jogador de cada vez dá **um palpite**.
3. Acertou? Ganha **o número do item em pontos** (o nº 1 é o óbvio e vale 1; o nº 10 é o difícil e vale 10).
   Errou? Passa a vez sem ponto. Também dá para digitar `/passar`.
4. Chute que já foi achado ou que já foi errado não conta: o jogador chuta de novo.
5. Acaba quando acham os 10 itens ou quando todo mundo passa a vez seguido. Quem tiver mais pontos vence.

Palpites ignoram acentos, maiúsculas e plural, e aceitam apelidos ("SP", "BH", "Rio").

## Como rodar (só precisa de Python 3)
Terminal 1 (servidor), para 2 jogadores na porta 5000:
```bash
python servidor.py 2 5000
```
Terminal 2 e 3 (um por jogador):
```bash
python cliente.py 127.0.0.1 5000
```
Quando os dois entrarem, o servidor pergunta a lista (1 a 10, ou Enter para sortear).
Para jogar em PCs diferentes na mesma rede, troque `127.0.0.1` pelo IP do PC do servidor.

```bash

## Arquivos
| Arquivo | O que faz |
|---|---|
| `servidor.py` | Recebe os jogadores, guarda o jogo na memória compartilhada e controla a vez |
| `cliente.py` | O terminal de cada jogador |
| `listas.py` | As 10 listas (tiradas do Topzi) |
| `palpite.py` | Confere se o palpite está na lista |

## Notação das mensagens (criada para este jogo)
Toda mensagem é uma linha de texto: `CODIGO|campo1|campo2|...`

| Quem manda | Mensagem | Significado |
|---|---|---|
| cliente → servidor | `NOME\|Ana` | o jogador entra com o nickname |
| servidor → cliente | `BEMVINDO\|1\|2` | "você é o jogador 1, a partida tem 2" |
| servidor → todos | `LISTA\|As 10 capitais...\|IBGE\|10` | a lista da partida |
| servidor → todos | `VEZ\|2\|Beto\|1=São Paulo;6=Belo Horizonte` | **vez = 2** (Beto) e os itens já achados |
| cliente → servidor | `CHUTE\|fortaleza` | o palpite de quem está na vez |
| cliente → servidor | `PASSA` / `SAIR` | passar a vez / sair |
| servidor → todos | `ACERTO\|2\|Beto\|4\|Fortaleza\|1=Ana=3;2=Beto=4` | Beto achou o nº 4 (+4) e o placar |
| servidor → todos | `ERRO\|2\|Beto\|aracaju` | o chute não está na lista |
| servidor → todos | `PASSOU\|2\|Beto` | Beto passou a vez |
| servidor → um | `DENOVO\|"aracaju" já foi chutado...` | chute repetido: o mesmo jogador tenta de novo |
| servidor → todos | `FIM\|motivo\|1=São Paulo;2=Rio...\|placar` | fim, lista completa e placar |

**A variável `vez`** existe nos dois processos, como o enunciado pede: o servidor guarda e passa
para o próximo jogador a cada jogada; cada cliente atualiza a sua cópia quando chega `VEZ|...`
e só pede o palpite se `vez == meu_id`. O servidor ignora mensagens de quem não está na vez.

## Memória compartilhada e exclusão mútua
- O servidor abre **uma thread por jogador** (função `atender`), e a thread principal conduz a partida.
- Todas as threads usam a **mesma memória**: o objeto `Estado` (vez, itens achados, chutes errados,
  pontos, a jogada recebida).
- Todo acesso a essa memória fica dentro de `with estado.lock:` / `with estado.cond:` (**região crítica**):
  só uma thread mexe nela por vez, então dois jogadores mandando mensagem ao mesmo tempo não
  bagunçam os dados.
- A thread principal espera a jogada com `estado.cond.wait_for(...)` (**dorme, sem gastar CPU**);
  a thread do jogador grava a jogada e chama `notify_all()` para acordá-la.
- Se alguém desconecta, a thread dele marca `encerrado = True` e a partida termina para todos.

## Conferência com o enunciado
| O que o trabalho pede | Onde está |
|---|---|
| Jogo para pelo menos 2 usuários | o servidor exige de 2 a 8 jogadores |
| Comunicação entre processos por socket (cliente/servidor) | `socket` TCP em `servidor.py` e `cliente.py` |
| Controle do jogo por códigos nas mensagens | códigos `VEZ`, `CHUTE`, `ACERTO`... (tabela acima) |
| Variável "vez" nos dois processos, controlada por mensagens | `estado.vez` no servidor e `vez` no cliente |
| Notação própria para as mensagens | `CODIGO\|campos`, com `;` e `=` para listas |
| Memória compartilhada entre os usuários | objeto `Estado`, usado por todas as threads |
| Exclusão mútua | `threading.Lock` e `threading.Condition` |
| Linguagem permitida | Python (está na lista do enunciado) |
| Não precisa de interface bonita | é só terminal |

## Respostas prontas para o formulário
- **Nome do jogo:** Top 10
- **Linguagem:** Python 3 (`socket` e `threading`)
- **Explicação:** jogo de adivinhar listas. Sai uma lista de 10 itens em ordem e os jogadores, um de cada vez,
  chutam itens. Acertar o item nº X vale X pontos (o mais óbvio vale 1, o mais difícil vale 10). Errar passa a vez.
  Vence quem somar mais pontos quando a lista acabar. São 10 listas (países, capitais, heróis, animes,
  games, McDonald's, folclore, redes sociais, desenhos e clubes europeus).
- **Como e quais informações são trocadas:** por socket TCP, cliente e servidor trocam linhas de texto
  `CODIGO|campos`. O cliente manda o nickname (`NOME`), o palpite (`CHUTE`) ou que passou (`PASSA`).
  O servidor manda a lista (`LISTA`), de quem é a vez (`VEZ`, com os itens já achados), o resultado de
  cada chute (`ACERTO` com pontos e placar, `ERRO`, `PASSOU`, `DENOVO`) e o fim (`FIM`).
  A variável `vez` existe no servidor e em cada cliente e é atualizada pela mensagem `VEZ`.
- **Exclusão mútua:** o estado do jogo fica numa memória compartilhada entre as threads do servidor
  (uma por jogador e a principal). Todo acesso a ela é feito dentro de um `threading.Lock`, então só uma
  thread mexe por vez. Uma `threading.Condition` faz a thread principal dormir até chegar a jogada de
  quem está na vez; a thread do jogador grava a jogada e a acorda com `notify_all()`.

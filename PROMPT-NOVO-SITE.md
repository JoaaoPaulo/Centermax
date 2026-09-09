# Prompt para remodelar esta landing page para outro estabelecimento

Cole o texto abaixo numa sessão nova do Claude Code, dentro deste repositório
(ou de uma cópia dele), trocando só o bloco **DADOS DE ENTRADA**.

O resto do prompt já carrega o método inteiro: como arrancar os dados reais do
Google Maps, como tirar a paleta e a logo das imagens da própria marca, o que
nunca inventar, e como conferir o resultado no navegador antes de entregar.

---

```
Transforme a landing page deste repositório no site de outro estabelecimento.
A base técnica continua a mesma: HTML, CSS e JavaScript puros, sem build, sem
npm install. O que muda é a marca, o conteúdo e a identidade visual inteira.

## DADOS DE ENTRADA

- Nome do estabelecimento: {{NOME}}
- Link do Google Maps: {{COLE O LINK COMPLETO DO GOOGLE MAPS}}
- Ramo/segmento: {{ex.: pizzaria, clínica veterinária, academia}}
- Site atual, se houver: {{URL OU "não tem"}}
- Instagram / Facebook: {{@perfil OU "não sei"}}
- Onde vai ser publicado: {{URL da Vercel ou do GitHub Pages}}

Se algum campo acima estiver vazio ou errado, descubra sozinho a partir do
Google Maps. Não me pergunte antes de tentar.

## PASSO 1 — LEVANTAR OS DADOS REAIS

Nada de conteúdo genérico. Tudo que for para a página precisa vir de uma fonte
real. Sua fonte principal é o próprio perfil do Google Maps, que é público e
acessível mesmo quando o site oficial está bloqueado.

Como extrair o perfil (funciona sem chave de API):

1. Baixe a página do lugar com um user-agent de navegador de verdade:
   curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
   (KHTML, like Gecko) Chrome/126.0 Safari/537.36" -H "Accept-Language: pt-BR" \
   "https://www.google.com/maps/place/.../data=!4m2!3m1!1s0xAAAA:0xBBBB?hl=pt-BR"
   (o par 0xAAAA:0xBBBB é o CID, está dentro do link que eu colei)

2. Nesse HTML existe um <link href="/maps/preview/place?...&pb=..."> logo no
   início do <head>. Extraia esse href, aplique html.unescape e busque
   "https://www.google.com" + href com o mesmo user-agent.

3. A resposta é JSON com um prefixo )]}' — corte tudo antes do primeiro '['.
   Ali estão: nome completo, endereço, telefone, categoria, site, horários,
   nota e número de avaliações, acessibilidade e a descrição escrita pelo
   próprio dono. Salve o JSON formatado e vasculhe campo por campo; a
   descrição do proprietário costuma ser ouro para o texto institucional.

4. Fotos: procure no JSON as URLs de lh3.googleusercontent.com. Baixe cada uma
   trocando o sufixo de tamanho (=w232-h86-k-no) por algo grande, tipo
   =w1600-h1200-k-no. A resolução nativa aparece no link original como
   !7i<largura>!8i<altura> — não adianta pedir mais que isso.

5. Place ID, para o schema.org e para os links do mapa: converta o CID com
   base64url(0x0A 0x12 0x09 + CID_A little-endian + 0x11 + CID_B little-endian).

Complemente com busca na web pelo nome do estabelecimento, pelo perfil do
dono/profissional e por diretórios do ramo. Registre a fonte de cada dado.

Armadilhas conhecidas, para não perder tempo:
- Wix, Instagram e Facebook costumam estar bloqueados pelo proxy de saída.
  O tradutor do Google (translate.goog) também. Não insista: vá pelo Maps.
- Street View estático e Places API devolvem 403 sem chave de API.
- google.com/search redireciona para consentimento via curl. Use a ferramenta
  de busca da web em vez de raspar o Google.

## PASSO 2 — TIRAR A IDENTIDADE VISUAL DA PRÓPRIA MARCA

Não escolha cores por gosto. Meça as cores reais:

- Baixe o banner/capa e a foto de perfil do Google. Quase sempre a logo, o
  slogan e as cores da marca estão ali dentro.
- Com Pillow (pip install Pillow), recorte e amplie a região da logo e do
  slogan, olhe as imagens e conte o histograma de cores para achar os valores
  exatos em hexadecimal. Guarde o arquivo original em assets/img/ como
  referência e explique no README de onde cada cor saiu.
- Redesenhe a logo como SVG limpo em assets/img/logo-mark.svg, com viewBox
  0 0 240 240. Use fill="currentColor" nas partes monocromáticas para o
  emblema funcionar em fundo claro e escuro sem precisar de dois arquivos.
  Duplique esse mesmo desenho num <symbol> no topo do index.html.
- Gere o favicon.svg com a marca sobre um quadrado arredondado na cor
  principal.
- Escolha as fontes do Google Fonts que mais se aproximem do logotipo real e
  justifique a escolha no README.

Renderize a logo isolada num HTML de teste e tire print antes de aplicar no
site. Compare com o original e ajuste até ficar reconhecível.

## PASSO 3 — REGRAS DE HONESTIDADE (as mais importantes)

- Nunca invente avaliação, depoimento, prêmio, número de clientes ou anos de
  experiência.
- Nunca use foto de banco de imagens fingindo ser o local, a equipe ou o
  produto. Se não houver foto real, a seção simplesmente não existe.
- Galeria e avaliações devem sumir sozinhas quando as listas do
  assets/js/data.js estiverem vazias, e reaparecer quando forem preenchidas.
- Serviços que você não conseguiu confirmar podem entrar como o conjunto
  padrão do ramo, mas precisam estar listados no README como NÃO CONFIRMADOS,
  com instrução de como apagar o cartão.
- Se o ramo for regulado (saúde, jurídico, financeiro), respeite os limites de
  publicidade da profissão: nada de promessa de resultado, nada de antes e
  depois sem autorização, e registro profissional quando existir.
- No fim, me diga explicitamente o que é confirmado e o que é presumido.

## PASSO 4 — A PÁGINA

Uma página só, seções comentadas em maiúsculas no HTML, textos em português do
Brasil, tom natural e específico do negócio (nada de "soluções sob medida" e
outros clichês de agência).

Estrutura sugerida, adapte ao ramo:
1. Cabeçalho fixo que muda de fundo ao rolar, com drawer no mobile
2. Topo com o slogan real, CTA principal e cartão de endereço/horário/telefone
3. Faixa de destaques com 4 números ou fatos verdadeiros
4. Seção institucional com o texto do próprio estabelecimento
5. Grade de serviços/produtos com ícones SVG desenhados por você
6. Uma seção dedicada ao carro-chefe do negócio, explicado em etapas
7. Perguntas frequentes em acordeão nativo (<details>), uma aberta por vez
8. Galeria e avaliações (escondidas se vazias)
9. Contato: endereço, horários, telefones e mapa do Google incorporado
10. Chamada final e rodapé

Requisitos técnicos:
- Responsivo de 320px a 1920px, sem rolagem horizontal em nenhuma largura
- Acessível: navegação por teclado, aria-*, skip link, foco visível, contraste
  suficiente e respeito a prefers-reduced-motion
- SEO: title, description, Open Graph, canonical, robots.txt, sitemap.xml e
  dados estruturados do @type certo (Restaurant, Dentist, HealthAndBeautyBusiness,
  AutoRepair, LocalBusiness...) com endereço, horários e geo
- FAQPage no schema, espelhando as perguntas da página
- Botão flutuante de WhatsApp com mensagem pré-preenchida
- Nenhuma dependência: sem framework, sem bundler, sem CDN de JavaScript

## PASSO 5 — CONFERIR NO NAVEGADOR ANTES DE ENTREGAR

Não me entregue nada sem ter olhado a página renderizada.

- Suba um servidor local (npx http-server -p 8123 -s .)
- Use o Playwright que já está instalado (require de
  /opt/node22/lib/node_modules/playwright, Chromium em /opt/pw-browsers).
  NÃO rode "playwright install".
- Tire print da página inteira em 1440px e em 390px e olhe cada pedaço.
- ATENÇÃO: passe reducedMotion:'reduce' ao criar a página, senão as animações
  de entrada deixam tudo abaixo da dobra invisível no print e você vai achar
  que a página está quebrada.
- Teste de verdade: acordeão abrindo um por vez, menu mobile abrindo e
  fechando, cabeçalho colando ao rolar, seções vazias escondidas, zero erro no
  console e scrollWidth igual a innerWidth no mobile.
- O iframe do mapa sai em branco no print porque o sandbox bloqueia o Google.
  Isso é esperado, não tente consertar.

Ao editar HTML em lote com regex, cuidado com .*? não guloso: ele atravessa
blocos inteiros e apaga cartões no meio do caminho. Prefira reescrever a seção
inteira a fazer substituições cirúrgicas em série. Depois conte as tags de
abertura e fechamento e valide os blocos application/ld+json com json.loads.

## PASSO 6 — DOCUMENTAÇÃO E ENTREGA

- Reescreva o README.md e o PHOTOS.md para o novo estabelecimento, incluindo a
  tabela de dados a conferir, o aviso sobre o que não foi confirmado e o passo
  a passo de como adicionar fotos e avaliações.
- Atualize o scripts/importar-google.py com o CID e as coordenadas novas.
- Apague as imagens do estabelecimento antigo.
- Commit em português, descritivo, explicando o que veio de fonte real.
- Push para a branch de trabalho.
- Antes de dizer que está no ar: confirme qual é a branch de produção. Este
  repositório pode não ter main, e a Vercel publica a partir da branch padrão.
  Se a branch de trabalho não for a de produção, me avise e pergunte antes de
  empurrar para outra branch.
```

---

## Se for para um repositório novo, do zero

Acrescente no começo do prompt:

```
Comece copiando a estrutura deste repositório como ponto de partida:
index.html, favicon.svg, robots.txt, sitemap.xml, assets/css/styles.css,
assets/js/data.js, assets/js/main.js e scripts/importar-google.py.
O main.js pode ser reaproveitado quase inteiro — carrossel, lightbox, menu,
acordeão e reveal já estão prontos e não dependem do ramo. Renomeie só os
globais CM_GALERIA e CM_AVALIACOES para as iniciais da marca nova.
```

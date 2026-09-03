# Centermax Odontologia — site

Site da **Centermax Odontologia**, Av. Mandacaru, 1799 — Loja 02, Maringá/PR.
HTML, CSS e JavaScript puros. Sem build, sem dependências, sem `npm install`.

> O repositório continua se chamando `DonChacon` por causa da publicação já
> existente na Vercel. Só o conteúdo do site mudou.

**Publicado em:** https://don-chacon-5rph.vercel.app/

---

## Como ver o site no seu computador

Basta abrir o `index.html` no navegador. Para o mapa e as fontes carregarem
direito, prefira subir um servidor local:

```bash
python3 -m http.server 8000
# depois abra http://localhost:8000
```

## Como publicar

A Vercel republica sozinha a cada push. O arquivo
`.github/workflows/deploy.yml` também publica uma cópia no GitHub Pages —
se você não usa o Pages, pode apagar esse arquivo sem quebrar nada.

---

## O que você vai querer editar

### 1. Fotos da clínica

**O site ainda não tem nenhuma foto da clínica.** O perfil no Google Maps só
tem o banner de campanha, que já está em `assets/img/`. Enquanto não houver
fotos, a seção *Galeria* fica escondida sozinha — ninguém vê uma seção vazia.

Para ligá-la, salve as fotos em `assets/img/galeria/` e liste em
`window.CM_GALERIA`, dentro de `assets/js/data.js`. O passo a passo está em
**[PHOTOS.md](PHOTOS.md)**.

### 2. Avaliações de pacientes

Mesma coisa: `window.CM_AVALIACOES` começa vazio e a seção *Avaliações* fica
escondida. Assim que você colar a primeira avaliação, ela aparece.

```js
{ nome: 'Fulano de Tal', data: 'há 2 meses', texto: 'Texto exato da avaliação.' },
```

Deixe `nome: ''` para exibir apenas "Avaliação verificada · Google".
**Use só avaliações reais**, copiadas do Google ou enviadas pelo paciente com
autorização.

### 3. Textos, especialidades e horários

Estão direto no `index.html`, cada bloco comentado com o nome da seção
(`HERO`, `A CLÍNICA`, `ESPECIALIDADES`, `IMPLANTES`, `DÚVIDAS`, `VISITE`).

---

## Confira estes dados antes de divulgar

Tudo que segue veio do perfil da clínica no Google Maps e de buscas públicas.
Vale conferir com a recepção antes de mandar o link para os pacientes.

| Campo | Valor no site |
|---|---|
| Endereço | Av. Mandacaru, 1799 — Loja 02, Vila Santa Izabel, Maringá/PR, 87080-000 |
| Telefone fixo | (44) 3040-4171 |
| WhatsApp | (44) 99940-4171 |
| Segunda a sexta | 9h — 12h e 14h — 18h |
| Sábado | 9h — 12h |
| Domingo | Fechado |
| No mercado desde | 2017 |
| Instagram | [@centermaxodontologia](https://www.instagram.com/centermaxodontologia/) |
| Facebook | [centermaxodonto](https://www.facebook.com/centermaxodonto/) |

**Atenção às especialidades.** O Google confirma implantes dentários, prótese
fixa, lentes de contato dental e facetas. As outras quatro da grade
(clareamento, ortodontia, tratamento de canal, prevenção/periodontia e
cirurgia) são o conjunto padrão de uma clínica desse porte e **não estão
confirmadas**. Se a clínica não faz alguma delas, apague o `<article
class="card">` correspondente no `index.html`.

O mesmo vale para a resposta sobre convênios nas *Dúvidas frequentes*: ela
manda o paciente perguntar no WhatsApp justamente por não sabermos a lista.

Onde trocar, se algo mudou: os telefones estão no `index.html` (busque por
`5544999404171` e `554430404171`) e os horários na seção `VISITE` e no bloco
`application/ld+json` do `<head>`.

---

## Estrutura

```
index.html                 página inteira, seções comentadas
favicon.svg                ícone da aba
assets/
  css/styles.css           identidade visual, layout e responsividade
  js/data.js               ← fotos e avaliações (edite aqui)
  js/main.js               carrosséis, lightbox, menu, FAQ, animações
  img/logo-mark.svg        emblema da clínica, vetorizado
  img/banner-original.jpg  banner do Google, guardado como referência da marca
  img/sorrisos.jpg         recorte do banner usado na seção "A clínica"
  img/galeria/             fotos da galeria (vazio por enquanto)
scripts/importar-google.py importa fotos e avaliações do Google Maps
.github/workflows/deploy.yml
```

## O que a página tem

- Topo em azul da marca com o slogan real da clínica e cartão de contato fixo
- Menu que muda de fundo ao rolar, com versão mobile em drawer
- Faixa de destaques (desde 2017, implantes, dias de atendimento, acessibilidade)
- Seção institucional com o texto oficial da clínica e a missão em destaque
- Grade de 8 especialidades com ícones desenhados à mão
- Seção dedicada ao implante dentário, explicado em 4 etapas
- Perguntas frequentes em acordeão, com dados estruturados `FAQPage`
- Galeria e avaliações que aparecem sozinhas quando o `data.js` for preenchido
- Horários, contato e mapa do Google incorporado
- Botão flutuante de WhatsApp com mensagem pré-preenchida
- SEO: meta tags, Open Graph, `sitemap.xml`, `robots.txt` e dados estruturados
  `Dentist` (schema.org) com endereço, horários e acessibilidade
- Acessibilidade: navegação por teclado, `aria-*`, skip link, foco visível
  e respeito a `prefers-reduced-motion`

## Sobre as cores e a logo

Nada aqui foi inventado: o azul escuro `#00669b` é o do slogan "A atenção certa
para o seu sorriso!" e o azul claro `#34a7e0` é o do coração dentro da logo.
Os dois foram medidos direto no banner oficial da clínica, que está guardado em
`assets/img/banner-original.jpg`.

O emblema em `assets/img/logo-mark.svg` é a logo redesenhada em vetor: as duas
figuras humanas que formam a silhueta de um dente, com o coração no vazio entre
elas. Sendo vetor, fica nítido em qualquer tela e acompanha a cor do texto ao
redor. Se um dia aparecer o arquivo vetorial oficial, é só substituir mantendo
o mesmo nome.

# Don Chacon Barber Club — Landing page

Landing page da **Barbearia Don Chacon**, Av. Cerro Azul, 1990 — Maringá/PR.
HTML, CSS e JavaScript puros. Sem build, sem dependências, sem npm install.

**Publicada em:** https://joaaopaulo.github.io/DonChacon/ (após ativar o GitHub Pages, veja abaixo)

---

## Como ver o site no seu computador

Basta abrir o arquivo `index.html` no navegador. Para o mapa e as fontes
carregarem corretamente, prefira subir um servidor local:

```bash
python3 -m http.server 8000
# depois abra http://localhost:8000
```

## Como publicar (GitHub Pages)

1. No repositório, vá em **Settings → Pages**.
2. Em *Build and deployment → Source*, escolha **GitHub Actions**.
3. Faça merge desta branch na `main`. O workflow `.github/workflows/deploy.yml`
   publica o site sozinho a cada push.

---

## O que você precisa editar

Quase tudo que muda com o tempo está em **um único arquivo**: `assets/js/data.js`.

### 1. Trocar ou acrescentar fotos

As fotos do site são as do próprio perfil da barbearia no Google Maps, já
escolhidas e otimizadas. Para acrescentar ou substituir alguma, jogue o arquivo
em `assets/img/galeria/` e liste em `window.DC_GALERIA`. O passo a passo está em
**[PHOTOS.md](PHOTOS.md)**.

### 2. Adicionar avaliações do Google

As quatro avaliações do site vieram do perfil no Google Maps e são reais. Para
acrescentar outras, edite `window.DC_AVALIACOES` em `assets/js/data.js`. Use
**somente avaliações de 5 estrelas**. Cada entrada é assim:

```js
{ nome: 'Fulano de Tal', data: 'há 2 meses', texto: 'Texto exato da avaliação.' },
```

Deixe `nome: ''` se preferir exibir apenas "Avaliação verificada · Google".
O carrossel se ajusta sozinho à quantidade de avaliações.

### 3. Ajustar textos, serviços e horários

Estão direto no `index.html`, cada bloco comentado com o nome da seção
(`HERO`, `SOBRE`, `SERVIÇOS`, `GALERIA`, `AVALIAÇÕES`, `VISITE`).

Os serviços listados são os padrões de uma barber shop e **não têm preços**.
Se quiser exibir a tabela de valores, é só acrescentar dentro de cada `<article class="card">`.

---

## Estrutura

```
index.html                 página inteira, seções comentadas
favicon.svg                ícone da aba
assets/
  css/styles.css           identidade visual, layout e responsividade
  js/data.js               ← fotos e avaliações (edite aqui)
  js/main.js               carrosséis, lightbox, menu, animações
  img/logo-mark.svg        emblema oficial, vetorizado
  img/logo-original.jpg    logo original do Google, para referência
  img/hero/                fundos do topo
  img/galeria/             fotos da galeria
scripts/importar-google.py importa fotos e avaliações do Google Maps
.github/workflows/deploy.yml
```

## O que a página tem

- Topo com slideshow de fundo, efeito Ken Burns e navegação por pontos
- Menu fixo que muda de fundo ao rolar, com versão mobile em drawer
- Faixa de destaques (nota, ano de fundação, dias de funcionamento, endereço)
- Seção institucional com colagem de fotos reais e selo *Est. 2018*
- Faixas em xadrez preto e branco, o mesmo piso do salão
- Grade de 8 serviços
- Carrossel de galeria com arraste, setas, pontos e lightbox com teclado
- Carrossel de avaliações 5 estrelas com autoplay que pausa no hover
- Horários, contato e mapa do Google incorporado com filtro escuro
- Botão flutuante de WhatsApp com mensagem pré-preenchida
- SEO: meta tags, Open Graph, `sitemap.xml`, `robots.txt` e dados
  estruturados `HairSalon` (schema.org) com endereço, horários e nota
- Acessibilidade: navegação por teclado, `aria-*`, skip link, foco visível
  e respeito a `prefers-reduced-motion`

## Dados do estabelecimento usados na página

| Campo | Valor |
|---|---|
| Endereço | Av. Cerro Azul, 1990 — Jardim Novo Horizonte, Maringá/PR, 87010-055 |
| Telefone / WhatsApp | (44) 98435-3833 |
| Segunda | 13h — 19h |
| Terça a sexta | 10h — 19h |
| Sábado | 09h — 15h |
| Domingo | Fechado |
| Nota no Google | 4,8 |
| Instagram | [@barbeariadonchacon](https://www.instagram.com/barbeariadonchacon/) |
| Facebook | [DonChaconBarberClub](https://www.facebook.com/DonChaconBarberClub/) |

Confira esses dados antes de publicar — se algo mudou, o telefone está no
`index.html` (busque por `5544984353833`) e os horários na seção `VISITE`.

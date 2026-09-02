# Como colocar as fotos reais no site

As imagens que aparecem hoje são **painéis gráficos temporários** que eu desenhei
na paleta da barbearia (preto, dourado, textura). Elas existem para o layout não
ficar quebrado. Troque pelas fotos reais quando puder — leva uns 10 minutos.

---

## Passo 1 — Baixar as fotos do Google Maps

1. Abra o perfil da barbearia no Google Maps e clique em **Fotos**.
2. Abra a foto que você quer, clique com o botão direito e escolha
   **Salvar imagem como…**.
3. Repita para as melhores 8 a 12 fotos. Priorize, nesta ordem:
   - fachada e letreiro (viram fundo do topo);
   - salão aberto, com as cadeiras à vista;
   - barbeiro trabalhando, corte em andamento;
   - detalhes: navalha, poste, produtos, parede decorada;
   - cortes finalizados.

Evite fotos escuras, tremidas ou com pessoas em close sem autorização.

## Passo 2 — Preparar os arquivos

- **Galeria:** retrato, cerca de 1200 × 1500 px.
- **Topo (hero):** paisagem, cerca de 1920 × 1280 px.
- Salve em `.jpg` com qualidade ~80%, ou converta para `.webp`.
  Cada arquivo deve ficar abaixo de ~300 KB para o site abrir rápido.
- Nomes sem espaço nem acento: `fachada.jpg`, `salao-01.jpg`, `barba-navalha.jpg`.

Se quiser comprimir sem instalar nada, use https://squoosh.app.

## Passo 3 — Colocar no repositório

Copie os arquivos para:

- `assets/img/galeria/` — fotos da galeria
- `assets/img/hero/` — fundos do topo

## Passo 4 — Listar em `assets/js/data.js`

```js
window.DC_GALERIA = [
  { src: 'assets/img/galeria/fachada.jpg',       alt: 'Fachada da Barbearia Don Chacon em Maringá' },
  { src: 'assets/img/galeria/salao-01.jpg',      alt: 'Salão e cadeiras da Don Chacon Barber Club' },
  { src: 'assets/img/galeria/barba-navalha.jpg', alt: 'Barba feita na navalha' }
  // ...continue
];

window.DC_HERO = [
  'assets/img/hero/fachada-noite.jpg',
  'assets/img/hero/salao.jpg'
];
```

O texto do `alt` descreve a foto para quem usa leitor de tela e ajuda no Google.
Escreva de verdade, não repita "foto".

Salve, atualize a página e pronto — os carrosséis se ajustam sozinhos à
quantidade de imagens.

## Passo 5 — Apagar os painéis temporários

Depois que todas as fotos reais estiverem no lugar, pode apagar os arquivos
`.svg` de `assets/img/galeria/` e `assets/img/hero/`. Não apague
`assets/img/logo-mark.svg` nem `favicon.svg`.

---

## Sobre a logo

O emblema em `assets/img/logo-mark.svg` (navalhas cruzadas em círculo dourado)
é um desenho que fiz para a marca. **Se você tiver o arquivo original da logo da
Don Chacon**, substitua:

1. Salve a logo como `assets/img/logo-mark.svg` (ideal) ou `.png` com fundo
   transparente, quadrada.
2. Se usar `.png`, troque a extensão nas 3 chamadas dentro do `index.html`
   (busque por `logo-mark.svg`).
3. Atualize também o `favicon.svg` se quiser o ícone da aba igual.

O nome "Don Chacon / Barber Club" no cabeçalho é texto, não imagem — ele fica
nítido em qualquer tela e você muda direto no `index.html`.

---

## Atalho: importar tudo automaticamente do Google

O script `scripts/importar-google.py` puxa as fotos, a fachada em Street View e
as avaliações de 5 estrelas direto da API do Google, e já reescreve o
`assets/js/data.js` sozinho.

```bash
export GOOGLE_MAPS_API_KEY="sua-chave"
python3 scripts/importar-google.py
```

Para gerar a chave: acesse o [Google Cloud Console](https://console.cloud.google.com/),
crie um projeto, ative **Places API (New)** e **Street View Static API** em
*APIs e serviços → Biblioteca*, e crie uma chave em *Credenciais*. O uso desse
volume cabe no crédito mensal gratuito.

Depois de rodar, confira o site e apague os arquivos `.svg` de placeholder que sobrarem.

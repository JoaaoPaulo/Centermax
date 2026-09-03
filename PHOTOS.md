# Fotos e logo

## O estado hoje

O site **não tem fotos da clínica**. O perfil da Centermax no Google Maps só
publicou um banner de campanha, e é dele que saem as duas imagens em uso:

| Onde | Arquivo |
|---|---|
| Seção "A clínica" | `assets/img/sorrisos.jpg` — recorte do banner, sem o texto e sem a logo |
| Referência da marca | `assets/img/banner-original.jpg` — o banner inteiro, como veio do Google |
| Emblema | `assets/img/logo-mark.svg` |

`assets/img/galeria/` está vazia de propósito. Enquanto `window.CM_GALERIA`
estiver vazio no `assets/js/data.js`, a seção *Galeria* não aparece no site —
melhor não ter galeria do que ter uma com foto de banco de imagens fingindo ser
o consultório.

## Acrescentar as fotos de verdade

1. Fotografe a fachada, a recepção, o consultório e a equipe. Celular recente
   serve bem; procure luz do dia e evite flash direto.
2. Salve em `assets/img/galeria/` como `.jpg` ou `.webp`, cerca de
   1600 × 1200 px, abaixo de ~400 KB. Nome de arquivo sem espaço nem acento.
3. Abra `assets/js/data.js` e acrescente uma linha em `window.CM_GALERIA`:

```js
{ src: 'assets/img/galeria/recepcao.jpg', alt: 'Recepção da Centermax Odontologia' },
```

Pronto: a seção aparece sozinha, com carrossel, setas e lightbox.

O `alt` é lido por quem usa leitor de tela e conta para o Google. Descreva a
cena de verdade, não escreva apenas "foto".

Para comprimir sem instalar nada, use <https://squoosh.app>.

### Uma observação sobre fotos de pacientes

Antes e depois de tratamento e qualquer foto em que apareça o rosto de um
paciente só podem ir para o site com autorização por escrito. O Código de Ética
Odontológica também restringe a divulgação de imagens com finalidade de
promoção — vale confirmar com o CRO-PR o que pode ser publicado.

## Sobre o emblema

`assets/img/logo-mark.svg` é a logo da clínica redesenhada em vetor: duas
figuras humanas que, juntas, formam a silhueta de um dente, com um coração
azul no vazio entre elas. O traço preto usa `currentColor`, então o emblema
fica branco no fundo azul e escuro no fundo claro sem precisar de dois arquivos.

O original em bitmap está dentro de `assets/img/banner-original.jpg`, no canto
inferior direito. Se um dia aparecer o arquivo vetorial oficial da agência,
basta substituir o `logo-mark.svg` mantendo o mesmo nome — e repetir os mesmos
caminhos dentro do `<symbol id="cm-mark">`, no topo do `index.html`, que é a
cópia usada pela página.

O nome "Centermax / Odontologia" no cabeçalho é texto, não imagem. A fonte é a
Poppins, escolhida por ser a geométrica mais próxima da usada no logotipo.

## Importar de novo do Google

O script `scripts/importar-google.py` refaz a importação de fotos e avaliações
pela API oficial do Google. Precisa de uma chave criada no
[Google Cloud Console](https://console.cloud.google.com/) com **Places API (New)**
e **Street View Static API** ativadas:

```bash
export GOOGLE_MAPS_API_KEY="sua-chave"
python3 scripts/importar-google.py
```

Ele grava as fotos em `assets/img/galeria/`, puxa a fachada do Street View e
reescreve as listas do `assets/js/data.js`. Confira o resultado antes de
publicar: o Street View pode ter pego a rua errada.

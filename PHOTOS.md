# Fotos e logo

As imagens do site são as fotos reais do perfil da **Barbearia Don Chacon** no
Google Maps, já selecionadas, redimensionadas e com texto alternativo escrito.
Nada aqui é placeholder.

| Onde | Arquivos |
|---|---|
| Fundo do topo | `assets/img/hero/` — fachada à noite, fachada com LED, área de convivência |
| Galeria | `assets/img/galeria/` — 12 fotos entre salão, fachada, equipe e cortes |
| Emblema | `assets/img/logo-mark.svg` |
| Logo original | `assets/img/logo-original.jpg`, guardada como referência |

## Trocar ou acrescentar uma foto

1. Salve o arquivo em `assets/img/galeria/`. Use `.jpg` ou `.webp`, cerca de
   1200 × 1500 px em retrato, abaixo de ~400 KB. Nome sem espaço nem acento.
2. Abra `assets/js/data.js` e acrescente uma linha em `window.DC_GALERIA`:

```js
{ src: 'assets/img/galeria/nome-do-arquivo.jpg', alt: 'Descrição curta da foto' },
```

O `alt` é lido por quem usa leitor de tela e conta para o Google. Descreva a cena
de verdade, não escreva apenas "foto".

Os carrosséis se ajustam sozinhos à quantidade de imagens. Para o topo, o array é
o `window.DC_HERO`, no mesmo arquivo.

Para comprimir sem instalar nada, use <https://squoosh.app>.

## Sobre o emblema

`assets/img/logo-mark.svg` é a logo oficial da barbearia redesenhada em vetor: o
círculo, o "D" com a seta dupla e o "C" formado pelos traços de máquina. Sendo
vetor, fica nítida em qualquer tela e acompanha a cor do texto ao redor, então
funciona igual no fundo preto e no branco.

O original em bitmap está em `assets/img/logo-original.jpg`. Se um dia aparecer o
arquivo vetorial oficial da agência, basta substituir o `logo-mark.svg` mantendo
o mesmo nome.

O nome "Don Chacon / Barber Club" no cabeçalho é texto, não imagem. A fonte usada
é a Jost, escolhida por ser a mais próxima da geométrica do logotipo original.

## Importar de novo do Google

O script `scripts/importar-google.py` refaz a importação de fotos e avaliações
pela API oficial do Google. Precisa de uma chave criada no
[Google Cloud Console](https://console.cloud.google.com/) com **Places API (New)**
e **Street View Static API** ativadas:

```bash
export GOOGLE_MAPS_API_KEY="sua-chave"
python3 scripts/importar-google.py
```

/* ==========================================================================
   Don Chacon Barber Club — dados editáveis do site
   Altere apenas este arquivo para trocar fotos e avaliações.
   ========================================================================== */

/* --------------------------------------------------------------------------
   1) GALERIA
   Coloque as fotos em assets/img/galeria/ e liste aqui.
   Formatos aceitos: .jpg .webp .png .svg
   Recomendado: 1200x1500px (retrato) ou 1600x1200 (paisagem), até ~300 KB.
   -------------------------------------------------------------------------- */
window.DC_GALERIA = [
  { src: 'assets/img/galeria/01-navalha.svg',  alt: 'Navalha e acabamento na Don Chacon Barber Club' },
  { src: 'assets/img/galeria/02-tesoura.svg',  alt: 'Corte na tesoura, Barbearia Don Chacon Maringá' },
  { src: 'assets/img/galeria/03-pente.svg',    alt: 'Finalização e styling masculino' },
  { src: 'assets/img/galeria/04-cadeira.svg',  alt: 'Cadeira de barbeiro clássica no salão' },
  { src: 'assets/img/galeria/05-poste.svg',    alt: 'Poste de barbearia, fachada Don Chacon' },
  { src: 'assets/img/galeria/06-frasco.svg',   alt: 'Produtos e cosméticos masculinos' },
  { src: 'assets/img/galeria/07-maquina.svg',  alt: 'Máquina e degradê na Don Chacon' },
  { src: 'assets/img/galeria/08-bigode.svg',   alt: 'Barba desenhada e aparada' }
];

/* --------------------------------------------------------------------------
   2) HERO — imagens de fundo que passam automaticamente
   -------------------------------------------------------------------------- */
window.DC_HERO = [
  'assets/img/hero/hero-1.svg',
  'assets/img/hero/hero-2.svg',
  'assets/img/hero/hero-3.svg'
];

/* --------------------------------------------------------------------------
   3) AVALIAÇÕES — somente 5 estrelas, copiadas do Google Maps.
   Para adicionar: abra o perfil no Google, copie o texto e o nome do autor
   e cole um novo objeto no formato abaixo. Deixe "nome" vazio ('') se quiser
   exibir apenas "Avaliação verificada no Google".

     { nome: 'Fulano de Tal', data: 'há 2 meses', texto: 'Texto da avaliação.' },
   -------------------------------------------------------------------------- */
window.DC_AVALIACOES = [
  {
    nome: '',
    data: '',
    texto: 'Vim a Maringá para um casamento e precisei dar um trato no visual, fui na Barbearia Don Chacon e fui muito bem atendido. Quem me atendeu foi o Leo (carioca), atencioso do começo ao fim, ótimo papo e o corte ficou excelente.'
  },
  {
    nome: '',
    data: '',
    texto: 'Ambiente agradável, ótimos profissionais e atendimento nota dez. Um novo conceito de barber shop em Maringá.'
  }
];

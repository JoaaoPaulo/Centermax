/* ==========================================================================
   Don Chacon Barber Club — interações
   ========================================================================== */
(function () {
  'use strict';
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- ano no rodapé ---------------- */
  var ano = $('#ano'); if (ano) ano.textContent = new Date().getFullYear();

  /* ---------------- header fixo ---------------- */
  var hdr = $('#hdr');
  var onScroll = function () { hdr.classList.toggle('is-stuck', window.scrollY > 40); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------------- menu mobile ---------------- */
  var burger = $('#burger'), nav = $('#nav');
  var closeNav = function () {
    nav.classList.remove('is-open');
    hdr.classList.remove('is-navopen');
    document.body.classList.remove('no-scroll');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Abrir menu');
  };
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    hdr.classList.toggle('is-navopen', open);
    document.body.classList.toggle('no-scroll', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  });
  $$('#nav a').forEach(function (a) { a.addEventListener('click', closeNav); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  /* ---------------- link ativo na navegação ---------------- */
  var links = $$('#nav a');
  var secs  = links.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
  if ('IntersectionObserver' in window && secs.length) {
    var navObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secs.forEach(function (s) { navObs.observe(s); });
  }

  /* ---------------- reveal ao rolar ---------------- */
  var revealables = $$('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var revObs = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en, i) {
        if (!en.isIntersecting) return;
        setTimeout(function () { en.target.classList.add('in'); }, i * 90);
        obs.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(function (el) { revObs.observe(el); });
  }

  /* ---------------- hero: slideshow de fundo ---------------- */
  (function heroSlides() {
    var box  = $('#heroBg'), dots = $('#heroDots');
    var imgs = window.DC_HERO || [];
    if (!box || !imgs.length) return;

    var slides = imgs.map(function (src, i) {
      var d = document.createElement('div');
      d.className = 'slide' + (i === 0 ? ' on' : '');
      d.style.backgroundImage = 'url("' + src + '")';
      box.appendChild(d);

      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', String(i === 0));
      b.setAttribute('aria-label', 'Imagem ' + (i + 1));
      b.addEventListener('click', function () { go(i); });
      dots.appendChild(b);
      return d;
    });

    var cur = 0, timer;
    function go(n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('on', i === cur); });
      $$('button', dots).forEach(function (b, i) { b.setAttribute('aria-selected', String(i === cur)); });
      restart();
    }
    function restart() {
      clearInterval(timer);
      if (!reduced && slides.length > 1) timer = setInterval(function () { go(cur + 1); }, 6500);
    }
    if (slides.length < 2) dots.style.display = 'none';
    restart();
  })();

  /* ---------------- carrossel genérico ---------------- */
  function makeCarousel(track, dotsBox, opts) {
    opts = opts || {};
    var items = function () { return Array.prototype.slice.call(track.children); };
    var dots = [];

    function build() {
      if (!dotsBox) return;
      dotsBox.innerHTML = '';
      dots = items().map(function (_, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'Ir para o item ' + (i + 1));
        b.setAttribute('aria-selected', String(i === 0));
        b.addEventListener('click', function () { scrollToIndex(i); });
        dotsBox.appendChild(b);
        return b;
      });
    }

    function currentIndex() {
      var mid = track.scrollLeft + track.clientWidth / 2, best = 0, bd = Infinity;
      items().forEach(function (el, i) {
        var c = el.offsetLeft + el.offsetWidth / 2;
        var d = Math.abs(c - mid);
        if (d < bd) { bd = d; best = i; }
      });
      return best;
    }

    function sync() {
      var fits = track.scrollWidth <= track.clientWidth + 2;
      track.classList.toggle('is-centered', fits);
      if (track.parentElement) track.parentElement.classList.toggle('is-centered', fits);
      var n = currentIndex();
      dots.forEach(function (b, i) { b.setAttribute('aria-selected', String(i === n)); });
    }

    function scrollToIndex(i) {
      var el = items()[i];
      if (!el) return;
      track.scrollTo({ left: el.offsetLeft - (track.clientWidth - el.offsetWidth) / 2, behavior: reduced ? 'auto' : 'smooth' });
    }

    function step(dir) {
      var n = currentIndex() + dir;
      var len = items().length;
      scrollToIndex((n + len) % len);
    }

    var raf;
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(sync);
    }, { passive: true });

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); step(-1); }
    });

    /* arrastar com o mouse no desktop */
    var down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false; sx = e.clientX; sl = track.scrollLeft;
      track.style.scrollBehavior = 'auto';
    });
    track.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (Math.abs(dx) > 4) moved = true;
      track.scrollLeft = sl - dx;
    });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(function (ev) {
      track.addEventListener(ev, function () {
        if (!down) return;
        down = false;
        track.style.scrollBehavior = '';
        if (moved) scrollToIndex(currentIndex());
      });
    });
    track.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);

    /* autoplay opcional */
    var auto;
    function play() {
      if (reduced || !opts.autoplay || items().length < 2) return;
      stop();
      auto = setInterval(function () { step(1); }, opts.autoplay);
    }
    function stop() { clearInterval(auto); }
    if (opts.autoplay) {
      track.addEventListener('pointerenter', stop);
      track.addEventListener('pointerleave', play);
      track.addEventListener('focusin', stop);
      document.addEventListener('visibilitychange', function () { document.hidden ? stop() : play(); });
    }

    return { build: build, sync: sync, step: step, go: scrollToIndex, play: play, stop: stop };
  }

  /* ---------------- galeria ---------------- */
  var galApi = null;
  (function galeria() {
    var track = $('#galTrack'), dotsBox = $('#galDots');
    var fotos = window.DC_GALERIA || [];
    if (!track || !fotos.length) return;

    fotos.forEach(function (f, i) {
      var fig = document.createElement('figure');
      fig.className = 'gal';
      fig.dataset.i = String(i);
      fig.setAttribute('role', 'button');
      fig.setAttribute('tabindex', '0');
      fig.setAttribute('aria-label', 'Ampliar: ' + (f.alt || 'foto'));
      var img = document.createElement('img');
      img.src = f.src;
      img.alt = f.alt || 'Foto da Barbearia Don Chacon';
      img.loading = i < 2 ? 'eager' : 'lazy';
      img.decoding = 'async';
      fig.appendChild(img);
      track.appendChild(fig);
    });

    galApi = makeCarousel(track, dotsBox, { autoplay: 4200 });
    galApi.build();
    galApi.sync();
    galApi.play();

    $$('[data-gal]').forEach(function (b) {
      b.addEventListener('click', function () { galApi.stop(); galApi.step(b.dataset.gal === 'next' ? 1 : -1); galApi.play(); });
    });

    /* lightbox */
    var lb = $('#lb'), lbImg = $('#lbImg');
    var idx = 0, lastFocus = null;

    function open(i) {
      idx = (i + fotos.length) % fotos.length;
      lbImg.src = fotos[idx].src;
      lbImg.alt = fotos[idx].alt || '';
      lastFocus = document.activeElement;
      galApi.stop();
      lb.hidden = false;
      document.body.classList.add('no-scroll');
      $('#lbClose').focus();
    }
    function close() {
      lb.hidden = true;
      galApi.play();
      document.body.classList.remove('no-scroll');
      if (lastFocus) lastFocus.focus();
    }

    track.addEventListener('click', function (e) {
      var fig = e.target.closest('.gal');
      if (fig) open(Number(fig.dataset.i));
    });
    track.addEventListener('keydown', function (e) {
      var fig = e.target.closest('.gal');
      if (fig && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); open(Number(fig.dataset.i)); }
    });

    $('#lbClose').addEventListener('click', close);
    $('#lbPrev').addEventListener('click', function () { open(idx - 1); });
    $('#lbNext').addEventListener('click', function () { open(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') open(idx + 1);
      if (e.key === 'ArrowLeft') open(idx - 1);
    });
  })();

  /* ---------------- avaliações ---------------- */
  var depoApi = null;
  (function depoimentos() {
    var track = $('#depoTrack'), dotsBox = $('#depoDots');
    var avs = window.DC_AVALIACOES || [];
    if (!track) return;

    if (!avs.length) {
      track.closest('.sec').hidden = true;
      return;
    }

    avs.forEach(function (a) {
      var nome = (a.nome || '').trim();
      var inicial = nome ? nome.trim().charAt(0).toUpperCase() : '★';

      var art = document.createElement('article');
      art.className = 'quote';
      art.innerHTML =
        '<div class="quote__stars" role="img" aria-label="5 de 5 estrelas">★★★★★</div>' +
        '<p class="quote__txt"></p>' +
        '<div class="quote__who">' +
          '<span class="quote__av" aria-hidden="true"></span>' +
          '<span class="quote__name"><b></b><span></span></span>' +
        '</div>';
      $('.quote__txt', art).textContent = a.texto || '';
      $('.quote__av', art).textContent = inicial;
      $('.quote__name b', art).textContent = nome || 'Avaliação verificada';
      $('.quote__name span', art).textContent = (a.data ? a.data + ' · ' : '') + 'Google';
      track.appendChild(art);
    });

    var api = depoApi = makeCarousel(track, dotsBox, { autoplay: 6000 });
    api.build();
    api.sync();
    api.play();

    $$('[data-depo]').forEach(function (b) {
      b.addEventListener('click', function () { api.stop(); api.step(b.dataset.depo === 'next' ? 1 : -1); api.play(); });
    });
  })();

  /* ---------------- reajuste ao redimensionar ---------------- */
  var rt;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { if (galApi) galApi.sync(); if (depoApi) depoApi.sync(); }, 180);
  });
})();

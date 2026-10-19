/* ===========================================================================
   Thème CPOO — agenda rappelé à chaque transition + pied de page.
   Source de vérité : tools/theme/cpoo-agenda.js (copié dans chaque deck par
   « make theme »). NE PAS ÉDITER la copie.

   Convention, côté slides.md — sur la diapositive qui ouvre une partie :

       <!-- .slide: data-section="Diagramme de classes" class="section-divider" -->
       ## Diagramme de classes

   Le script collecte ces diapositives dans l'ordre, construit le plan, et
   l'affiche sur chaque intercalaire avec la partie courante mise en avant.
   Chaque diapositive ordinaire reçoit un pied de page « cours · partie · n/N ».
   Rien à maintenir à la main : ajouter une partie, c'est ajouter un marqueur.
   =========================================================================== */
(function () {
  // « `Machin` » dans un titre de partie : on rend le code au lieu d'afficher
  // les accents graves bruts dans le plan et le pied de page.
  function poserTexte(el, texte) {
    const echappe = String(texte)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    el.innerHTML = echappe.replace(/`([^`]+)`/g, '<code>$1</code>');
  }

  function initCpooTheme(opts) {
    opts = opts || {};
    const cours = opts.cours || document.title || '';

    function build() {
      const deck = document.querySelector('.reveal .slides');
      if (!deck) return;

      // 1) les intercalaires, dans l'ordre du deck
      const dividers = Array.from(deck.querySelectorAll('section[data-section]'));
      const titres = dividers.map(s => s.getAttribute('data-section'));

      // 2) l'agenda sur chaque intercalaire
      dividers.forEach((sec, i) => {
        sec.classList.add('section-divider');
        if (sec.querySelector('.agenda')) return;
        const ol = document.createElement('ul');
        ol.className = 'agenda';
        titres.forEach((t, j) => {
          const li = document.createElement('li');
          poserTexte(li, t);
          if (j === i) li.className = 'courant';
          else if (j < i) li.className = 'fait';
          ol.appendChild(li);
        });
        sec.appendChild(ol);
      });

      // 3) pied de page : cours · partie courante · numéro
      //    (la partie d'une diapositive = le dernier intercalaire rencontré)
      const top = Array.from(deck.children).filter(el => el.tagName === 'SECTION');
      let courante = '';
      let n = 0;
      const total = top.length;
      top.forEach(sec => {
        n += 1;
        if (sec.hasAttribute('data-section')) courante = sec.getAttribute('data-section');
        // sous-diapositives verticales : même pied de page que leur parente
        const cibles = sec.querySelector('section') ?
          Array.from(sec.querySelectorAll(':scope > section')) : [sec];
        cibles.forEach(cible => {
          if (cible.querySelector(':scope > .cpoo-footer')) return;
          if (cible.classList.contains('titre')) return;
          const f = document.createElement('div');
          f.className = 'cpoo-footer';
          const g = document.createElement('span');
          g.textContent = cours;
          const d = document.createElement('span');
          d.className = 'sec';
          poserTexte(d, courante);
          const p = document.createElement('span');
          p.textContent = n + '/' + total;
          f.append(g, d, p);
          cible.appendChild(f);
        });
      });

      // 3 bis) la première diapositive porteuse d'un h1 est la page de titre
      const premiere = top[0];
      if (premiere && premiere.querySelector('h1') && !premiere.classList.contains('titre')) {
        premiere.classList.add('titre');
        const f = premiere.querySelector(':scope > .cpoo-footer');
        if (f) f.remove();
      }

      // 4) marquer les diapositives porteuses d'une figure (mise en page flex)
      deck.querySelectorAll('section').forEach(sec => {
        if (sec.querySelector(':scope > img, :scope > p > img, :scope > .mermaid'))
          sec.classList.add('has-figure');
      });
    }

    if (window.Reveal && Reveal.isReady && Reveal.isReady()) build();
    else if (window.Reveal) Reveal.on('ready', build);
    else document.addEventListener('DOMContentLoaded', build);
  }
  window.initCpooTheme = initCpooTheme;
})();

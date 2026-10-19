/* Theme boot (taken from the CPOO decks, tools/theme) for this reveal-md deck.
   reveal-md injects the front-matter "scripts:" AFTER reveal.js but BEFORE
   Reveal.initialize(): we can neither call initCpooTheme right away (the Markdown
   is not split into slides yet), nor listen to "ready" (no instance yet).
   So we wait until reveal is ready. */
(function () {
  var COURS = 'REP · Feature models and UVL';
  var essais = 0;
  var t = setInterval(function () {
    essais += 1;
    if (window.Reveal && Reveal.isReady && Reveal.isReady() && window.initCpooTheme) {
      clearInterval(t);
      initCpooTheme({ cours: COURS });
    } else if (essais > 300) {          // 30 s: give up silently
      clearInterval(t);
    }
  }, 100);
})();

module.exports = async (page) => {
  // Many pages embed live third-party content (Disqus, podcast art, a
  // GitHub-stars iframe, an external "404 cat" image) that legitimately
  // varies between loads and has nothing to do with our own CSS/JS. Block
  // everything cross-origin so captures only reflect our own site.
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    if (req.url().startsWith('http://localhost')) {
      req.continue();
    } else {
      req.abort();
    }
  });

  // animate.css/WOW.js-driven reveals and CSS transitions (e.g. the
  // slimscroll-wrapped sidebar) land at different points mid-animation
  // depending on capture timing. Force every animation/transition to its
  // end state immediately, before the page's own stylesheets even apply,
  // so captures are deterministic instead of a race against JS timing.
  await page.evaluateOnNewDocument(() => {
    const style = document.createElement('style');
    style.textContent = `
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
        scroll-behavior: auto !important;
      }
    `;
    document.documentElement.appendChild(style);
  });
};

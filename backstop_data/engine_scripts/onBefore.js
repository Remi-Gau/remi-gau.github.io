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
        animation-name: none !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
        scroll-behavior: auto !important;
      }
      /* animation-name:none above (not just duration:0) matters: Chrome
         sizes a container's scrollable-overflow off an animated element's
         full keyframe range (e.g. animate.css's fadeInRight translating
         off-screen), not its current computed transform — so even a
         zero-duration, fully-settled transform-based animation can
         intermittently inflate the full-page screenshot's width depending
         on exactly when WOW.js's reveal happens to run relative to
         capture. Suppressing animation-name entirely avoids the keyframes
         ever being considered, independent of that timing. */
      html, body {
        overflow-x: clip !important;
      }
    `;
    document.documentElement.appendChild(style);
  });
};

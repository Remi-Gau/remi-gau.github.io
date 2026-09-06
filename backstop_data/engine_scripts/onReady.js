module.exports = async (page) => {
  // WOW.js hides .wow elements (inline style) until a real scroll event
  // reveals them — that never happens during an automated full-page
  // capture, so every capture would show them stuck hidden regardless of
  // any real visitor's experience. Force them visible for a deterministic,
  // content-complete screenshot.
  await page.evaluate(() => {
    document.querySelectorAll('.wow').forEach((el) => {
      el.style.visibility = 'visible';
    });
  });

  // The hero carousel (static/js/carousel.js) auto-advances every 2s. If a
  // capture lands mid-transition, Bootstrap briefly positions the outgoing
  // and incoming slides side-by-side via transform, which inflates the
  // page's measured scrollable width even though nothing is visibly wrong
  // — an intermittent, capture-timing-dependent false diff. Pause it.
  await page.evaluate(() => {
    document.querySelectorAll('.carousel').forEach((el) => {
      const instance = window.bootstrap && window.bootstrap.Carousel.getInstance(el);
      if (instance) instance.pause();
    });
  });

  // animate.css's transform-based classes (fadeInRight, zoomIn, etc.) can
  // leave a page's measured scrollable width intermittently inflated even
  // once fully settled and even with animation-name forced to none via
  // CSS in onBefore.js (a Chromium quirk in how scrollable-overflow gets
  // computed for a transformed box, not reliably suppressed by cascade
  // alone). Actually removing the classes from the DOM — rather than just
  // neutralizing them via CSS — has proven the one thing that reliably
  // avoids it.
  await page.evaluate(() => {
    document.querySelectorAll('[class*="animate__"]').forEach((el) => {
      el.className = el.className.replace(/animate__\S+/g, '').trim();
    });
    // Force a synchronous layout recalculation so Chrome's internal layout
    // metrics (which Puppeteer's fullPage screenshot reads via CDP) are
    // guaranteed fresh as of the class removal above, not a stale value
    // computed before it.
    void document.body.offsetHeight;
  });
};

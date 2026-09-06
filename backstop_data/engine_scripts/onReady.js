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
};

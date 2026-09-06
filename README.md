# https://remi-gau.github.io/

Based on https://github.com/jarrekk/Jalpc

## Testing Locally

To test your site locally, you’ll need

    - ruby
    - the github-pages gem

### Installing ruby

There are lots of different ways to install ruby.

In Mac OS X, older versions of ruby will already be installed. But I use the
Ruby Version Manager (RVM) to have a more recent version. You could also use
Homebrew.

In Windows, use RubyInstaller. (In most of this tutorial, I’ve assumed you’re
using a Mac or some flavor of Unix. It’s possible that none of this was usable
for Windows folks. Sorry!) Installing the github-pages gem

Run the following command:

```bash
gem install github-pages
```

This will install the github-pages gem and all dependencies (including jekyll).
Later, to update the gem, type:

```bash
gem update github-pages
```

### Testing your site locally

You'll also need [Node.js](https://nodejs.org/) to build the site's CSS/JS
bundle (see below). Install dependencies once with `npm install`, then to
build and serve the site:

```bash
npm run build
bundle exec jekyll serve
```

(`make serve` does both for you.) Now open your browser and go to
http://localhost:4000/site-name/

## Compress CSS and JS files

`static/assets/{app,blog,i18}-*.min.{css,js}` are **build output, not
committed to the repo** — `npm run build` generates them fresh from
`package.json`'s pinned versions (Bootstrap, jQuery, etc.) every time, using
[UglifyJS](https://github.com/mishoo/UglifyJS) and
[clean-css](https://github.com/jakubpawlowicz/clean-css). This runs locally
(above), in the [deploy workflow](.github/workflows/jekyll.yml), and in the
[visual regression workflow](.github/workflows/visual-regression.yml) — so
bumping a front-end dependency in `package.json` takes effect everywhere
automatically, with no separate "rebuild and commit the bundle" step to
remember (and no risk of the committed bundle silently drifting out of sync
with `package.json`, which is what happened before this was set up this way).

Customized CSS lives in the `_sass` folder, a [Jekyll
feature](https://jekyllrb.com/docs/assets/). If you want to add or remove
which CSS/JS files get bundled, edit `build/build.js` and
`build/files.conf.js`, then run `npm run build` — the `<link>`/`<script>`
tags in `_includes/head.html` and `_includes/index_head.html` are
automatically rewritten to point at the newly generated files.

## Visual regression testing

[BackstopJS](https://github.com/garris/BackstopJS) takes screenshots of key
pages at a few viewport sizes and diffs them against a reference set, so you
can tell whether bumping a front-end dependency (Bootstrap, jQuery,
animate.css, etc.) changed how the site actually renders.

The pages/viewports checked are configured in [backstop.json](backstop.json).
`backstop_data/bitmaps_reference/` is not committed — it's regenerated
on demand, both locally and in CI (see below).

### Locally, before bumping a dependency

1. Build and serve the site: `npm run build && bundle exec jekyll serve`
   (must be reachable at `http://localhost:4000`).
2. Capture the baseline: `npm run backstop:reference`.

After bumping the dependency and rebuilding/re-serving the site:

1. Run `npm run backstop:test`. This captures new screenshots, compares
   them against the baseline from step 2, and opens an HTML report showing
   any visual diffs.
2. If the diffs are expected/desired, great. If not, you've caught a visual
   regression — fix it before merging.

### On every pull request

[.github/workflows/visual-regression.yml](.github/workflows/visual-regression.yml)
builds the site from both `main` and the PR branch, serves them side by side,
and runs the same BackstopJS scenarios to diff the PR's render against
`main`'s — no committed baseline needed, since `main` *is* the baseline for
that run. The check fails if anything visually changed, and the diff report
(with images) is uploaded as a workflow artifact you can download and open.

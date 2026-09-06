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

To construct and test your site locally, go into the directory and type

```bash
bundle exec jekyll serve
```

Now open your browser and go to http://localhost:4000/site-name/

## Compress CSS and JS files

All CSS and JS files are compressed at `/static/assets`.

I use [UglifyJS2](https://github.com/mishoo/UglifyJS2), [clean-css](https://github.com/jakubpawlowicz/clean-css) to compress CSS and JS files, customized CSS files are at `_sass` folder which is feature of [Jekyll](https://jekyllrb.com/docs/assets/). If you want to custom CSS and JS files, you need to do the following:

1. Install [NPM](https://github.com/npm/npm) then install **UglifyJS2** and **clean-css**: `npm install -g uglifyjs; npm install -g clean-css`, then run `npm install` at root dir of project.
2. Compress script is **build.js**
3. If you want to add or remove CSS/JS files, just edit **build/build.js** and **build/files.conf.js**, then run `npm run build` at root dir of project, link/src files will use new files.

OR

Edit CSS files at `_sass` folder.

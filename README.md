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

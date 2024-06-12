---
layout: post
title: "A primer to 3... Hum, no! Four documentation frameworks!!!!"
date: "2024-03-09"
tags: [tuto]
categories: []
---

If "untested code is broken code" then "undocumented code is no code at all".
You may have created the most useful tool but if you have no documentation explaining how to use it,
then it is almost as if you had not written any code.

<!-- more -->

Here I will show how to get started with several documentation frameworks:

- [jekyll + github pages](#jekyll--github-pages)
- [mkdocs + read the docs](#mkdocs--read-the-docs)
- [sphinx + read the docs](#sphinx--read-the-docs)
- [jupyter book + github pages](#sphinx--read-the-docs)

**Table of content**

* TOC
{:toc}

---

## Relevant links

- The awesome [Write the docs](https://www.writethedocs.org/). Make sure to check out their slack workspace!

## Jekyll + GitHub pages

Jekyll is a static website generator based on ruby.
Static websites: HTML + CSS but no database.

**Use case:**
Serve the markdown content of repo as a website.

**Advantages:**
- integrate REALLY easily with github
- easy way to get started with html / css
- lots of templates to choose from for personal website, events...
- can use the [liquid templating language](https://shopify.github.io/liquid/)

**Not covered:**
local set up: installing ruby + jekyll and serving the website

<div class="admonition">
   <div class="admonition-title">
      <p>Setting up jekyll</p>
   </div>
   <div class="admonition-content">
      <p><a href="https://s-canchi.github.io/2021-04-30-jekyll-conda/"
            target="_blank"
            title="install jekyll with conda">This post</a>
         explains how to set up jekyll if you already have conda on your computer.
      </p>
   </div>
</div>

**Examples:**

<!-- TODO add links -->

- most of the brainhack local site events
- bids website
- this website

### Ingredients

- have a github repo with some markdown in it

Don't know what to write?

- [Lorem ipsum](https://www.lipsum.com/)
- [Wisdom of chopra]( http://wisdomofchopra.com/)

Note you can mix markdown and HTML.

### Recipe

1. add a `config.yml` file in the root of the repo with the theme for your website.

   For example

   ```yml
   theme: jekyll-theme-minimal
   ```

   The themes supported by github pages [are listed on this page](https://pages.github.com/themes/).
   You can also preview what they will look like.


2. Got to the `Settings` tab of the repo, then to the `Pages` menu,
   then under the `Branch` section choose the default branch of your repo
   and then save.
   This should trigger the build and deploy of the website.

3. Browse your website at this URL: https://`your-github-username`.github.io/`your-repo-name`.

   The github action to build the website will be triggered by any new push to the default branch.

   You can always monitor the github action in the `Actions` tab of the repo.

### Outcome

- Repo: [https://github.com/Remi-Gau/jekyll-primer](https://github.com/Remi-Gau/jekyll-primer)
- Website: [https://remi-gau.github.io/jekyll-primer/](https://remi-gau.github.io/jekyll-primer/)

### Reuse templates

There are a LOT of available jekyll templates:

- [https://github.com/topics/jekyll-theme](https://github.com/topics/jekyll-theme)

### Create your own academic site in less than 5 minutes

1. Create a new repo using the template https://github.com/academicpages/academicpages.github.io
   but name it `YOUR-GITHUHB-USERNAME.github.io`.
2. Deploy using github pages.
3. Start editing the `.config.yml`.

### Relevant links

- [jekyll documentation](https://jekyllrb.com/)
- [Setting up a GitHub Pages site with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)

## Mkdocs + read the docs

Mkdocs is a python package to help create documentation website from markdown files.

**Use case:**
Create some official looking documentation website from markdown.

**Advantages:**
- integrate easily with github
- integrate easily with read the docs (allow easy preview on pull requests)
- easy to work with locally
- many extensions and plugins
- the use of macros makes it a very powerful framework

**Inconvenients:**
- less flewibility in terms of looks

**Examples:**

<!-- TODO add links -->

- BIDS specification
- neurobagel documentation

### Ingredients

- have a github repo with some markdown in it
- python to serve locally

### Recipe

1. Clone your repo.

2. Install mkdocs.

   ```bash
   pip install mkdocs
   ```

3. Create minimal config.

   ```bash
   mkdocs new .
   ```

   Will create a `mkdocs.yml` in the root of the repo
   and a `doc/index.md` which will be the landing page of the website.


4. Serve locally.

   ```bash
   mkdocs serve
   ```

   You can then browse the documentation as a website at `http://127.0.0.1:8000/`

   Updating an markdown file, should automatically update the website.

   Kill the serve with `ctrl + c`.

5. Change the default theme.

   Install mkdocs-material

   ```bash
   pip install mkdocs-material
   ```

   Add it to the `mkdocs.yml` that should now look like this.

   ```yml
   site_name: My Docs
   theme:
      name: material
   ```

   Serve the website again and check the difference.

   ```bash
   mkdocs serve
   ```

See the [next section](#serve-to-read-the-docs) to see how to use Read The Docs to deploy your doc.

### Relevant links

- https://www.mkdocs.org/
- https://squidfunk.github.io/mkdocs-material/

### Serve to Read The Docs

1. Add a `requirements.txt` in the root of the repo.

   Content:

   ```
   mkdocs
   mkdocs-material
   ```

2. Add a `.readthedocs.yaml` in the root of the repo.

   Content

   ```yml
   version: 2
   build:
      os: ubuntu-22.04
      tools:
         python: "3.11"

   # Build documentation with Mkdocs
   mkdocs:
      configuration: mkdocs.yml

   # Dependencies required to build your docs
   python:
      install:
      - requirements: requirements.txt
   ```

3. Commit and push.

   ```bash
   git add --all
   git commit -m 'add requirements and RTD config'
   git push
   ```

4. Log in to read the docs: [https://readthedocs.org/accounts/login](https://readthedocs.org/accounts/login).

5. Find the repo below `Import a Repository` or go for the `Import Manually` option.

   If the latter, fill in the `Name`, `Repository URL` and `Default branch` fields and click `Next`

6. Click on `Build Version`.

   Once the build is completed, you should be able to see the website at:

   https://`REPO_NAME`.readthedocs.io/en/latest/

7. Make sure a preview of the doc is done on every pull request.

   Go to the `Admin` tab, tick the box below `Build pull requests for this project:` and click `Save`

#### Relevant links

- [https://docs.readthedocs.io/en/stable/](https://docs.readthedocs.io/en/stable/)


### Outcome

- Repo: [https://github.com/Remi-Gau/mkdocs-primer](https://github.com/Remi-Gau/mkdocs-primer)
- Website: [https://mkdocs-primer.readthedocs.io/en/latest/](https://mkdocs-primer.readthedocs.io/en/latest/)


## Intermission: dead links and spelling

Quick tip to avoid dead links and spelling mistakes in your documentation.

### pre-commit and codespell

You can use the [pre-commit](https://pre-commit.com/) git-hook framework to automatically run [codespell](https://github.com/codespell-project/codespell)
to check the content of your repository for spelling mistakes.

1. Create a `.pre-commit-config.yaml` in your repository with the following content:

   ```yml
   # See https://pre-commit.com for more information
   # See https://pre-commit.com/hooks.html for more hooks

   repos:

   # Checks for spelling errors
   -  repo: https://github.com/codespell-project/codespell
      rev: v2.3.0
      hooks:
      -   id: codespell
   ```

1. Install pre-commit and install the git hooks

   ```bash
   pip install pre-commit
   pre-commit install
   ```

This will make sure that codespell is run every time you commit
to make you only commit "clean" content.

You may need to add a [config file for codespell](https://github.com/codespell-project/codespell?tab=readme-ov-file#using-a-config-file) that looks like this:

```text
[codespell]
skip = .git
ignore-words-list = list,of,words,separated,by,commas
builtin = clear,rare
```

### markdown check links

If the framework that you use does not have any build in way to check
if the links in your documentation are valid,
you can use a [github action](https://github.com/gaurav-nelson/github-action-markdown-link-check/) that runs [markdown-link-check](https://github.com/tcort/markdown-link-check)
on the content of your markdown files.

Create a `.github/workflows/check_md_links.yml` with the following content

```yml
name: Check markdown links

on:
    push:
        branches: [main]

jobs:
    markdown-link-check:
        runs-on: ubuntu-latest
        steps:
        -   uses: actions/checkout@master
        -   uses: gaurav-nelson/github-action-markdown-link-check@v1
            with:
                use-quiet-mode: yes
                use-verbose-mode: yes
                # extra config file to ignore some links
                config-file: md_link_check_config.json
                # folder containing your doc
                folder-path: docs
                # extra files to validate
                file-path: ./README.md
```

The configuration file would look like this.

```json
{
  "ignorePatterns": [
    {
      "pattern": "^https://doi.org\/"
    },
  ],
  "timeout": "20s",
  "retryOn429": true
}
```

## Sphinx + read the docs

Sphinx is a python package to help create documentation website from files written using restructured text / markdown.

**Use case:**
Create a documentation website for a python code base.

**Advantages:**
- autodoc functionality renders the doc strings of python code
- possible to work with markdown files using the MyST plugin.
- integrate easily with read the docs (allow easy preview on pull requests)
- support other languages than python (e.g Matlab / Octave).
- easy to work with locally
- many extensions and plugins
- a decent selection of themes

**Inconvenients:**
- the restructured text syntax is less forgiving than that of markdown

**Examples:**
- pretty much the doc website of any python package


### Ingredients

- have a github repo with some python code in it
- python to serve locally

### Recipe

1. Install sphinx.

   ```bash
   pip install sphinx
   ```

2. Initial set up.

   ```bash
   mkdir docs
   cd docs
   sphinx-quickstart
   ```

   Respond to the questions in the prompt.

   ```
   ├── docs
   │   ├── make.bat
   │   ├── Makefile
   │   └── source
   │       ├── conf.py
   │       ├── index.rst
   │       ├── _static
   │       └── _templates
   └── README.md
   ```

3. Build the doc.

   ```bash
   make html
   ```

4. View the doc.

   Open `docs/build/html/index.html`

5. Use MySt to render a markdown file.

   Install myst.

   ```bash
   pip install myst-parser
   ```

   Add `"myst_parser"` to the list of extensions in `docs/source/conf.py`.

   ```python
   extensions = ["myst_parser"]
   ```

   Add a markdown file in the `source` directory of the doc.

   ```
   ├── docs
   │   ├── make.bat
   │   ├── Makefile
   │   └── source
   │       ├── conf.py
   │       ├── index.rst
   │       ├── markdown_is_possible.md    <---
   │       ├── _static
   │       └── _templates
   └── README.md
   ```

   And add it into the `docs/source/index.rst` file.

   ```rst

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      markdown_is_possible.md

   ```

6. Change the theme.

   Install the furo theme.

   ```bash
   pip install furo
   ```

   Change html_theme in `docs/source/conf.py`.

   ```python
   html_theme = "furo"
   ```

   Rebuild the doc to check the new theme.

7. Auto-document your python code.

   Add a python module `src/some_python_code.py`

   ```
   ├── docs
   │   ├── make.bat
   │   ├── Makefile
   │   └── source
   │       ├── conf.py
   │       ├── index.rst
   │       ├── markdown_is_possible.md
   │       ├── modules
   │       │   └── api.rst
   │       ├── _static
   │       └── _templates
   ├── src
   │   └── some_python_code.py    <---
   └── README.md
   ```

   Add some code in it with a few functions.

   ```python
   def foo() -> None:
      """Public function should appear in the doc.

      Return ``None``.
      """
      return None

   def _bar():
      """Private function should not appear in the doc."""
      ...
   ```

   Modify `docs/source/conf.py` so that the python code is in its path
   when ti runs, by adding the following lines:

   ```python
   import os
   import sys

   sys.path.insert(0, os.path.abspath("../.."))
   ```

   Also add the `"sphinx.ext.autodoc"` extension to autodocument code
   to list of active extensions in `docs/source/conf.py`.

   ```python
   extensions = ["myst_parser", "sphinx.ext.autodoc",]
   ```

   Now create a `.rst` file in the `doc/source` where the doc of your code
   will be rendered.

   ```
   ├── docs
   │   ├── make.bat
   │   ├── Makefile
   │   └── source
   │       ├── conf.py
   │       ├── index.rst
   │       ├── markdown_is_possible.md
   │       ├── modules
   │       │   └── api.rst    <---
   │       ├── _static
   │       └── _templates
   ├── src
   │   └── some_python_code.py
   └── README.md
   ```

   And add in it the sphinx directive to autodocument the code:

   ```rst

   api
   ===

   .. sphinx directives to auto doc code

   .. automodule:: src.some_python_code
      :members:
      :undoc-members:
      :show-inheritance:

   ```

   Rebuild the doc to check the new theme.

### Serve to Read The Docs

1. Add a `requirements.txt` in the root of the repo.

   Content:

   ```
   sphinx
   furo
   myst-parser
   ```

2. Add a `.readthedocs.yaml` in the root of the repo.

   Content

   ```yml
   version: 2
   build:
      os: ubuntu-22.04
      tools:
         python: "3.11"

   # Build documentation with sphinx
   sphinx:
      configuration: docs/source/conf.py

   # Dependencies required to build your docs
   python:
      install:
      - requirements: requirements.txt
   ```

3. The rest of the process is the same [as for MkDocs](#serve-to-read-the-docs).

### Outcome

Repo: [https://github.com/Remi-Gau/sphinx-primer](https://github.com/Remi-Gau/sphinx-primer)
<!-- Website: [https://mkdocs-primer.readthedocs.io/en/latest/](https://mkdocs-primer.readthedocs.io/en/latest/) -->

### Relevant links

- [Sphinx documentation](https://www.sphinx-doc.org/en/master/)


## Jupyter book + Github pages

**Use case:**

Create a documentation website for project containing Markdown documents and Jupyter notebooks.

**Advantages:**

- easy to work with locally
- easy way to integrate executable code in your documentation

**Examples:**

<!-- TODO add links -->

- The Turing way

### Ingredients

- have a github repo with some markdown in it
- python to serve locally

### Recipe

1. Install jupyter book.

   ```bash
   pip install -U jupyter-book
   ```

1. Create a book template

   ```bash
   jupyter book jupyter-book-primer
   ```

1. Move into the directory that was created and build the book

   ```bash
   cd  jupyter-book-primer
   jupyter book build .
   ```

1. Browse the book that was created by opening the landing page
   `_build/html/index.html`.

1. Turn into a repository, gitignore the `_build` and commit all the created
   content

   ```bash
   echo _build > .gitignore
   git add --all
   git commit -m 'initial commit'
   ```

1. Add a Github repo as remote and push to github

   ```bash
   git remote add origin <URL_OF_REMOTE>
   git push --set-upstream origin main
   ```

### Serve via GitHub pages

1. Add a github workflow to serve the book via github pages

   On your repository go to `Settings` -> `Pages`, and for `Source` choose
   `GitHub Actions`.

   Create a file `.github/workflows/deploy.yml` with the following content.

   ```yml
   name: deploy-book

   # Run this when the master or main branch changes
   on:
   push:
      branches:
         - main

   # This job installs dependencies, builds the book, and pushes it to `gh-pages`
   jobs:
   deploy-book:
      runs-on: ubuntu-latest
      permissions:
         pages: write
         id-token: write
      steps:
         - uses: actions/checkout@v3

         # Install dependencies
         - name: Set up Python 3.11
         uses: actions/setup-python@v4
         with:
            python-version: 3.11

         - name: Install dependencies
         run: |
            pip install -r requirements.txt

         # Build the book
         - name: Build the book
         run: |
            jupyter-book build .

         # Upload the book's HTML as an artifact
         - name: Upload artifact
         uses: actions/upload-pages-artifact@v2
         with:
            path: "_build/html"

         # Deploy the book's HTML to GitHub Pages
         - name: Deploy to GitHub Pages
         id: deployment
         uses: actions/deploy-pages@v2
   ```

1. Commit and push the file:

   ```
   git add .github
   git commit -m "add build and deploy workflow"
   git push
   ```

Github should then take over and serve your documentation.

#### Relevant links

More info in [the jupyter book documentation](https://jupyterbook.org/en/stable/publish/gh-pages.html).

### Outcome

- Repo: [https://github.com/Remi-Gau/jupyter-book-primer](https://github.com/Remi-Gau/jupyter-book-primer)

- Website: [https://remi-gau.github.io/jupyter-book-primer](https://remi-gau.github.io/jupyter-book-primer)

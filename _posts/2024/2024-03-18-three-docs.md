---
layout: post
title: "primer to 3 documentation framworks"
date: "2024-03-18"
tags: [tuto]
categories: []
---

This post contains 3 primers on how to set up some basic documentation with:

- jekyll + github pages
- mkdocs + read the docs
- sphinx + read the docs

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

**Examples:**
- most of the brainhack local site events
- bids website
- this website

### Ingredients

- have a github repo with some markdown in it

Don't know what to write?

- Lorem ipsum: https://www.lipsum.com/
- Wisdom of chopra: http://wisdomofchopra.com/

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

![alt text](https://private-user-images.githubusercontent.com/6961185/311474995-f6d0bf22-3797-4706-b3c9-31853128715c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTAwMjkxMDAsIm5iZiI6MTcxMDAyODgwMCwicGF0aCI6Ii82OTYxMTg1LzMxMTQ3NDk5NS1mNmQwYmYyMi0zNzk3LTQ3MDYtYjNjOS0zMTg1MzEyODcxNWMucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDMxMCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDAzMTBUMDAwMDAwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9M2NjMmFhZGI1ZmQxYjg4NzQzYjcxYzRiYmFkZTdiZWI3MjMzNzMwZWUxYjNlY2UwYzI4YTNmMWVkNmVjYzA4YSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.ZuTTQmUnr9tkJCCAQMBemMMjwhxb5UhOvjWSFOnzBY4)

3. Browse your website at this URL: https://`your-github-username`.github.io/`your-repo-name`.

The github action to build the website will be triggered by any new push to the default branch.

You can always monitor the github action in the `Actions` tab of the repo.

### Re-use templates

There are a LOT of available jekyll templates:

- https://github.com/topics/jekyll-theme

### Create your own academic site in less than 5 minutes

1. Create a new repo using the template https://github.com/academicpages/academicpages.github.io but name it `YOUR-GITHUHB-USERNAME.github.io`.
2. Deploy using github pages.
3. Start editing the `.config.yml`.

### Relevant links

- [jekyll documentation](https://jekyllrb.com/)
- [Setting up a GitHub Pages site with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)

## Mkdocs + read the docs

Mkdocs is a python package to help create documentation website from markdown files.

**Use case:**
Create some official looking docuentation website from markdown.

**Advantages:**
- integrate easily with github and read the docs
- easy to work with locally
- many extensions and plugins
- the use of macros makes it a very powerful framework

**Inconvenients:**
- less flewibility in terms of looks

**Examples:**
- BIDS specification
- neurobagel documentation

### Ingredients

- have a github repo with some markdown in it
- python to serve locally

### Recipe

1. clone your repo

2. install mkdocs

```bash
pip install mkdocs
```

3. create minimal config

```bash
mkdocs new .
```

Will create a `mkdocs.yml` in the root of the repo
and a `doc/index.md` which will be the landing page of the website.


4. serve locally

```bash
mkdocs serve
```

You can then browse the documentation as a website at http://127.0.0.1:8000/

Updating an markdown file, should automatically update the website.

Kill the serve with `ctrl + c`.

5. Change the default theme

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

### Relevant links

- https://www.mkdocs.org/
- https://squidfunk.github.io/mkdocs-material/

## Serve to Read the docs

1. add a `requirements.txt` in the root of the repo

Content:

```
mkdocs
mkdocs-material
```

2. add a `.readthedocs.yaml` in the root of the repo

Content

```yml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
    # You can also specify other tool versions:
    # nodejs: "16"

# Build documentation with Mkdocs
mkdocs:
   configuration: mkdocs.yml

# Dependencies required to build your docs
python:
   install:
   - requirements: requirements.txt
```

3. commit and push

```bash
git add --all
git commit -m 'add requirements and RTD config'
git push
```

4. log in to read the docs: https://readthedocs.org/accounts/login

5. Find the repo below `Import a Repository` or go for the `Import Manually` option

If the latter fill in the `Name`, `Repository URL` and `Default branch` fields and click `Next`

6. Click on `Build Version`

Once the build is completed, you should be able to see the wesbite at: https://`REPO_NAME`.readthedocs.io/en/latest/

7. Make sure a preview of the doc is done on every pull request

Go to the `Admin` tab, tick the box below `Build pull requests for this project:` and click `Save`

### Relevant links

- https://docs.readthedocs.io/en/stable/

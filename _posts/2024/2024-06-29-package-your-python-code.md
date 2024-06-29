---
layout: post
title: "Stop using notebooks and package your python code instead."
date: "2024-06-29"
tags: [how-to]
categories: []
---

If you are drowning in notebooks
and find that your codebase has turned into a copy-pasta induced spaghetti factory,
take 5 minutes to package your code to make it easier to reuse.

## Move the code you need to reuse

Move the code ou want to be able to import into a `src/YOUR_PACKAGE` folder
and add an empty `__init__.py` file into it.

For example you could do somethng like this.

```text
└── src
    └── my_package
        ├── __init__.py
        └── main.py
```

## Add pyproject.toml

Add a `pyproject.toml` file in the root of your project with this content.

```toml
[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[project]
# put your dependencies below instead of in your requirements.txt
dependencies = [
    "rich"
]
name = "my_package"
version = "0.1.0"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

So your project would look like:

```text
├── pyproject.toml
└── src
    └── my_package
        ├── __init__.py
        └── main.py
```

## Install your package

You can now `pip install` your project, most likely as an editable install.

```bash
pip install --editable .
```

## Check the install

Just to check that your package is there.

```bash
pip list
```

```
Package        Version Editable project location
-------------- ------- -------------------------
markdown-it-py 3.0.0
mdurl          0.1.2
my_package     0.1.0   /home/remi/github/tmp
pip            24.1.1
Pygments       2.18.0
rich           13.7.1
```

## Use your package

Now assuming that you have `greet` function `src/my_package/main.py`
You can do from within a python REPL:

```python
>>> from my_package.main import greet
>>> greet()
Bonjour le monde
```

## Extras

- [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
  is fast becoming the new python standard to centralize metadata and configurations in python projects.
  It can act as a control-room where you can set the parameters for all the formatting, linting testing tools you may use.
- This example uses [hatchling](https://hatch.pypa.io/latest/config/build/#build-system) to build the python package.
  It has a nice [hatch-vcs extension](https://pypi.org/project/hatch-vcs/)
  that uses git tags to keep track of the version of your package.
- The set up described here uses a [source layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- If you want to dive deeper, Chris Markiewicz has [an excellent post about this](https://effigies.gitlab.io/posts/python-packaging-2023/).

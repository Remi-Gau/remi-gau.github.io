---
layout: post
title: MATLAB clean code
date: "2022-03-31"
tags: []
categories: []
---

<div class="row" style="margin-bottom: 50px;">
    <div class="col-lg-8 col-lg-offset-4">
        <img width="50%"
             src="/static/assets/img/blog/cancer.jpeg">
    </div>
</div>

Recently, [Anibal Sólon](https://anibalsolon.com/) asked for tips about writing
clean MATLAB🔒 code.

So when a confirmed wizard asks you for a advices, you try to forget that you
feel like an apprentice sorcerer most of the time and you respond with some of
the things you learned along the way[^1]<sup>,</sup>[^2].

Also figured some other people could benefit so here is a post about this.

<div class="row">
<div class="col-lg-10 col-lg-offset-1"
     style="border: solid; margin-top:10px; margin-bottom:10px;  border-radius: 25px;">
    <h2>TL;DR</h2>
    <p> Here is a
        <a href="https://github.com/cpp-lln-lab/template_matlab_analysis">
            template github repo [WIP]
        </a>
        that has already a lot of things set up to get you started on your clean MATLAB🔒
        code journey.
    </p>
</div>
</div>

**TOC**

- [Oxymoronic](#oxymoronic)
- [Getting by](#getting-by)
  - [Code style](#code-style)
  - [miss_hit](#miss_hit)
  - [Only commit clean code](#only-commit-clean-code)
  - [Testing](#testing)
    - [Why tests matter](#why-tests-matter)
    - [Testing in practice](#testing-in-practice)
    - [Test automation](#test-automation)
  - [Documentation](#documentation)
  - [Demos](#demos)
  - [Containerize](#containerize)
  - [Dependency management](#dependency-management)
  - [Interoperability and open-source](#interoperability-and-open-source)
  - [Path management](#path-management)
- [Template](#template)
- [Examples and links](#examples-and-links)

## Oxymoronic

So clean MATLAB🔒 code, hey?

From most of the scientific MATLAB🔒 code I have
[written](https://github.com/Remi-Gau?tab=repositories&q=&type=source&language=matlab&sort=name)
in my life that "clean MATLAB🔒 code" feels a bit like a contradiction in terms.
A bit like [civil war](https://www.youtube.com/watch?v=_tsbFbKH0OQ),
[jumbo shrimp or military intelligence](https://youtu.be/mRdxdFDX3W0?t=113).

<br>

For most of my life, the MATLAB🔒 code I wrote:

- was made of a bunch of scripts so long you will get carpal tunnel syndrome
  before you are done scrolling through the first file,

- used indentation and spacing
  <span style="word-spacing: 1px;letter-spacing: -2.5px">that you would make
  sardines in a can feel claustrophobic</span>,[^3]

- had an average line-length that must have been a significant driver of the demand on
  the wide-screen market,

- HAd aVeryInconsistent Approach to_the_use of CaSeS

- used a simple but horrible algorithm to name variables,

```text
Name your first variable `a`, the second `b`...
When you reach the end of the alphabet go for `aa`, `ab`...
```

- was usually very
  [WET](https://github.com/dwmkerr/hacker-laws#the-dry-principle) due to an
  extensive use of copy-pasta (turning the whole code base into a spaghetti
  factory),

- sometimes forgot about
  [Kernighan's law](https://github.com/dwmkerr/hacker-laws#kernighans-law) and
  tried to be overly clever,

- was written as
  [throw away](http://ivory.idyll.org/blog/2015-how-should-we-think-about-research-software.html)
  code[^4],

- grew "organically" (like mold) with an ad-hochitecture approach to new
  feature implementation.

- had
  - more
    - nesting
      - than
        - a
          - successful
            - ponzy
              - scheme

<br>

My feeling towards most of my MATLAB🔒 code is pretty well summed up by one of
the intro sentence in [Patrick Mineault](https://twitter.com/patrickmineault)'s
excellent [The Good Research Code Handbook](https://goodresearch.dev/).

> "[I] hate my code and don’t want to work on it."

And to be clear I am not saying switching to Python, R, Julia (or any other language)
will automagically give you cleaner code.
One could easily browse github to find examples code written in other languages
that have some or all of the defects mentioned above - please don't actually do this:
don't code shame unless you are actually going some of your old code as an example.
But very often other languages either have tools or coding conventions
that help writing cleaner code.

## Getting by

MATLAB🔒 does not really have a lot of tools to help us mitigate this situation
in an easy and consistent manner. So the best we can do is mostly get by. Very
often by using tools written in Python.

### Code style

> "Code should be easy to understand.” <br> “Code should be written to minimize
> the time it would take for someone else to understand it.”

<p class="quote-ref">
    <a href="https://www.vitalsource.com/ie/products/the-art-of-readable-code-dustin-boswell-v9781449314217"
       target="_blank">
       The art of readable code
    </a>
</p>

And yet...

> “There is a tendency among some programmers, perhaps inspired by Shakespeare’s
> line: '_Brevity is the soul of wit_', to write MATLAB code that is terse and
> even obscure.”

<p class="quote-ref">
    <a href="https://fr.mathworks.com/matlabcentral/fileexchange/46056-matlab-style-guidelines-2-0"
       target="_blank">
       MATLAB🔒 Style Guidelines 2.0
    </a>
</p>

So start by choosing some code style and **stick to it**.

If you don't know where to start, pick the MATLAB🔒 style guidelines mentioned
above.

If you want a good intros for code style and quality, check the
[turing way website](https://the-turing-way.netlify.app/reproducible-research/code-quality.html)

<div class="row" style="margin-top: 20px;">
    <div class="col-lg-8 col-lg-offset-2">
        <img width="100%"
             src="/static/assets/img/blog/1728_TURI_Book sprint_19 readable code_040619.jpg">
    </div>
</div>

<p class="quote-ref">
    <a href="https://zenodo.org/record/3332808"
       target="_blank">
        Created by Scriberia for The Turing Way community.
    </a>
</p>

<!--
Variable names:
- don't use letters
- use english
 -->

### miss_hit

If you think that I spend my time manually making sure that all of my MATLAB🔒
code has the right number of spaces before and after every `+`, `-`, `=` signs,
then you over-estimate my patience.

To help me, I use the [`miss_hit` python package](https://misshit.org/).

`miss_hit` can check code style, do a certain amount of automatic code
reformatting and prevent the code complexity from getting out of hand by running
static code analysis.

Static analysis can is a way to measure and track software quality metrics
without additional code like tests.

If you are familiar with python[^5], `miss_hit` is a bit like a mix of `black`
and `flake8`.

If you have no idea what those are, think of `miss_hit` as a parent that would
tell you off when your room is too messy but will also help you tidy it up.

Install `miss_hit`:

```bash
$ pip3 install miss_hit
```

Style-check your program:

```bash
$ mh_style --fix path_to_folder_or_m_file
```

Make sure your code does not get too complex:

```bash
$ mh_metric --ci
```

I personally used this alias to just regularly run the whole of `miss_hit` on
any folder I am in.

```bash
mh='mh_style --fix && mh_metric --ci && mh_lint'
```

`miss_hit` is quite configurable, but you can usually stick with a lot of the
defaults.

### Only commit clean code

If you are as forgetful as I am, you may forget to run `miss_hit` before you
commit code to a repository.

Hopefully there are 3 easy steps you can do to make sure this does not happen by
relying on the [`pre-commit` python package](https://pre-commit.com/).

1. Install `pre-commit`

```bash
$ pip3 install pre-commit
```

2. Add file called `.pre-commit-config.yml` with following content

```yml
repos:
  - repo: local

    hooks:
      - id: mh_style
        name: mh_style
        entry: mh_style
        args: [--process-slx, --fix]
        files: ^(.*\.(m|slx))$
        language: python
        additional_dependencies: [miss_hit_core]

      - id: mh_metric
        name: mh_metric
        entry: mh_metric
        args: [--ci]
        files: ^(.*\.(m|slx))$
        language: python
        additional_dependencies: [miss_hit_core]

      - id: mh_lint
        name: mh_lint
        entry: mh_lint
        files: ^(.*\.(m|slx))$
        language: python
        additional_dependencies: [miss_hit]
```

3. Run the following command to install the `pre-commit` "hooks"

```bash
$ pre-commit install
```

Additionally you can also run `pre-commit run -a` to let `pre-commit` check all
of the files in your repo after installing it.

I would also suggest to set [pre-commit CI](https://pre-commit.ci/) to let it
fix your code automatically on Github.

### Testing

> "Untested code is broken code."

<p class="quote-ref">
    <a href="https://youtu.be/xOKPKiAhey4?t=540"
       target="_blank">
       Fernando Perez, at NeuroHackademy 2018
    </a>
</p>

In general try to write tests for the code you are about to write.

For a short intro to testing,
[check the turing way](https://the-turing-way.netlify.app/reproducible-research/testing.html)

#### Why tests matter

If you are unclear as to why tests matter to clean code, let me try an analogy.

Imagine you live in a fully functional house: it does all the things one could
reasonably expect a house to do. But you would like to redesign it because even
if you can cook, eat, sleep, wash, relax in it... the set up is not optimum
("Why is the oven in the garage?", "Should the dishwasher be in the bedroom?").

The problem is that to redesign will require moving some bearing walls: so
redesigning the house may at any moment turn your fully functional house into a
pile of bricks. To make things worse, none of your friends can host you while
you are redesigning your house: so you have to live in it while the work is
happening. This means that most of the functionalities of the house should be
retained (because you happen to consider that eating and washing up are not just
luxuries that one can simply do away with).

Wouldn't it be great if you had some monitoring system that:

- defined what are the expected functionalities of your house,
- warned you when your house starts losing functionality ?

Now let's go back to clean code.

Have you ever told yourself the following?

> I want to share the code that my results are based on. I will clean it when we
> are closer to submitting the paper.

But despite your best intentions, you never got to it. It is not that you are
lazy, but cleaning up often require changes so drastic ("tearing down a bearing
wall"), that the code start producing results that are different from the ones
in the paper that is already on its way to the printing press. Those differences
could be substantial ("You had a house. Here, have a pile of bricks!") or much
less so ("The garage door does not open anymore."), but either way you have no
way of knowing and anyone now running this code would get different results from
the one in your paper.

So what a suite of tests for your code does:

- it says what your code should be doing by defining what results it is expected
  to produce
- it will throw an alarm if any of the code stops working as expected.

With a good test suite you can almost carelessly change your code and be
confident that if something stops working you will know about it.

#### Testing in practice

To make your life easier for writing and running tests I would recommend using
the [MOxUnit testing framework](https://github.com/MOxUnit/MOxUnit). Works with
both MATLAB🔒 and Octave🔓. It has a companion toolbox
([MOcov](https://github.com/MOcov/MOcov)) to get a code coverage estimate after
running your tests[^6].

Don't expect something like `pytest`, but it gets the job done pretty well.

To install it on Linux or Mac.

```bash
$ git clone https://github.com/MOxUnit/MOxUnit.git
$ cd MOxUnit
$ make install
```

To install it on Windows see
[here](https://github.com/MOxUnit/MOxUnit#installation).

A typical test filename must start with `test_` and a typical test file will
look like this:

```matlab
function test_suite=test_sum_of_squares

    try % assignment of 'localfunctions' is necessary in Matlab >= 2016
        test_functions=localfunctions();
    catch % no problem; early Matlab versions can use initTestSuite fine
    end
    initTestSuite();

end

function test_sum_of_squares_basic

    % given
    a = 2;
    b = 3;

    % when
    result = sum_of_squares([a, b])

    % then
    expected = 13;
    assertEqual(result, expected);

end
```

See
[here for more info on defining tests](https://github.com/MOxUnit/MOxUnit#defining-moxunit-tests).

You can then:

- run each `.m` file individually,
- call `moxunit_runtests` from the MATLAB🔒 command line to run all tests in a
  folder,
- use `MOcov` to run all your tests by doing something as described below.

If your project is structured like this:

```bash
├──run_tests.m
├── src   # This is where your source code is
└── tests # This is where your tests are
```

And `run_tests.m` could simply contain:

```matlab
folder_to_cover = fullfile(pwd, 'src');
test_folder = fullfile(pwd, 'tests');
coverage_report = fullfile(pwd, 'coverage_html');

success = moxunit_runtests( testFolder, ...
                            '-verbose', '-recursive', '-with_coverage', ...
                            '-cover', folderToCover, ...
                            '-cover_xml_file', 'coverage.xml', ...
                            '-cover_html_dir', coverage_report);

if success
    system('echo 0 > test_report.log');
else
    system('echo 1 > test_report.log');
end

```

#### Test automation

No point in having tests and not running them regularly. It'd be like believing
that owning a tooth brush but not using it, is enough to keep cavities away.

Best way to automate running your suite of tests is to do it via Github
continuous integration.

This is done by adding some specific `.yml` files in a `.github/workflows`
folder in your repository.

If your code runs on Octave🔓, then you can just use the
[Moxunit Github action](https://github.com/joergbrech/moxunit-action) that can
give you
[code coverage with codecov](https://github.com/joergbrech/moxunit-action#ci-non-beginner-user).

A typical `.yml` file for to run this action would look something like
[this](https://github.com/agahkarakuzu/eda_organized/blob/master/.github/workflows/moxunit.yml).

If your code does not run on Octave🔓, then you can still run your tests using
the [MATLAB🔒 Github actions](https://github.com/matlab-actions/overview)
provided that your Github repository is public[^7].

The project set up like this:

```bash
├── .github
│   └── workflows
│       ├── run_matlab_tests.m
│       └── run_matlab_tests.yml
├──run_tests.m
├── src   # This is where your source code is
└── tests # This is where your tests are
```

Your `run_matlab_tests.yml` would define the following workflow:

```yml
name: tests and coverage with matlab

on:
  push:
    branches: ["master", "main", "dev"]
  pull_request:
    branches: ["*"]

jobs:
  tests:
    runs-on: Ubuntu-latest

    steps:
      - name: Install MATLAB
        uses: matlab-actions/setup-matlab@v1.0.1
        with:
          release: R2020a

      - name: Shallow clone of your repo
        uses: actions/checkout@v3
        with:
          submodules: true
          fetch-depth: 0

      - name: Install Moxunit and MOcov
        run: |
          git clone https://github.com/MOxUnit/MOxUnit.git --depth 1
          git clone https://github.com/MOcov/MOcov.git --depth 1

      - name: Run MATLAB command
        uses: matlab-actions/run-command@v1.0.1
        with:
          command:
            cd(fullfile(getenv('GITHUB_WORKSPACE'), '.github', 'workflows'));
            run run_matlab_tests;

      - name: Check for failure
        run: |
          cat test_report.log | grep 0
          bash <(curl -s https://codecov.io/bash)

      - name: Code coverage
        uses: codecov/codecov-action@v1
        with:
          file: coverage.xml
          flags: matlab
          name: codecov-umbrella
          fail_ci_if_error: true
```

And this workflow would call the `run_matlab_tests.m` script.

```matlab
root_dir = getenv('GITHUB_WORKSPACE');

addpath(fullfile(root_dir, 'MOcov', 'MOcov'));

cd(fullfile(root_dir, 'MOxUnit', 'MOxUnit'));
run moxunit_set_path();

cd(fullfile(root_dir));

run run_tests();
```

### Documentation

Write the documentation of your code by reusing the comment you have put in your
code especially the "help" section of each function.

This can be done using the
[Sphinx](https://www.sphinx-doc.org/en/master/index.html) and its
[extension for MATLAB🔒](https://github.com/sphinx-contrib/matlabdomain).

As very well described in the
[[The Good Research Code Handbook]](https://goodresearch.dev/docs.html#publish-docs-on-readthedocs),
setting and building the basic doc is a 4 commands affair and it is also
possible to fairly easily serve the documentation on
[read the docs](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html)
and make sure that it builds with every new pull request without failing.

A typical set up for Sphinx will look something like this.

```bash
docs
├── Makefile              # contains recipes to help you build the doc
├── source
│   ├── conf.py           # config file for the doc
│   └── index.rst
└── src
    └── sum_of_squares.m
```

To work with MATLAB the `conf.py` would have to include the following lines:

```python
# -- General configuration
extensions = [
    'sphinxcontrib.matlab',
    'sphinx.ext.autodoc',
    'sphinx_copybutton']
matlab_src_dir = os.path.dirname(os.path.abspath('../../src'))
primary_domain = 'mat'
}
```

And the `index.rst` could simply just contain this to render the content of the
help of `sum_of_squares.m` in the final documentation (as an HTML page, as a
PDF...)

```bash
My doc
******

.. automodule:: src

.. autofunction:: sum_of_squares

```

The only "inconvenient" of this is that Sphinx uses
[restructuredText](https://docutils.sourceforge.io/rst.html) as a markup
language which is less forgiving than markdown in its syntax[^8].

### Demos

Documenting your code is usually not enough so make sure that you also include
demos to show how to use your code base.

If you use Octave you can also create those demos in jupyte notebooks and even
run those demos in the cloud using binder.

<!-- explain -->

### Containerize

### Dependency management

MATLAB🔒 has not "built-in" way to install and import external toolboxes. If
your code that relies on some external library, add it to your repository:

- as a git sub-module if that external code exist on Github or Gitlab,
- in a separate folder from your own code if it only exists on Matlab exchange
  (or somewhere else).

Do not expect your users (most of them are just you in 1, 2, 6, 12 and 18
months) to know which version of each library. And even if you do list those in
your README[^9], it is annoying to have to go and get them manually.

### Interoperability and open-source

Try to to write MATLAB🔒 code as if future users will only have access to
Octave🔓. So usually avoid some the fanciest and latest MATLAB🔒 features.

That also usually means relying on libraries that themselves are Octave🔓
compatible. If you are in neuroimaging, try to make good use of SPM as it is
almost 100% Octave🔓 compatible (though SPM toolboxes themselves might not be
😢😠).

### Path management

Create a simple script / function in the root of your repository to add all the
relevant subfolders of your project to the MATLAB🔒 path.

## Template

There is a
[template github repo WIP](https://github.com/cpp-lln-lab/template_matlab_analysis)
that has already a lot of this set up.

## Examples and links

If you want actual examples of all this.

- [BIDS-matlab](https://github.com/bids-standard/bids-matlab) for a light
  version.
- [CPP_SPM](https://github.com/cpp-lln-lab/CPP_SPM) for a larger code base.
- check the [demo repo](https://github.com/agahkarakuzu/eda_organized) and the
  accompanying video by [Agah Karakuzu](https://agahkarakuzu.github.io/) that
  helped me get started with a lot of this.

<div class="row" style="margin-top: 20px; margin-bottom: 20px;">
    <div class="col-lg-8 col-lg-offset-2">
        <iframe width="560"
                height="315"
                src="https://www.youtube.com/embed/AWfrlKTLkqw"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
        </iframe>
    </div>
</div>

---

[^1]: As far as I know all the tips provided here work fine with Octave🔓.
[^2]: I have not tested all of those tips on Windows.
[^3]:
    We did find this hard to read and yet we regularly do it in your code. Code
    is not written on paper (anymore). Not adding spaces or skipping lines will
    not save trees.

[^4]:
    Which very often makes me feel that the "throw-away" prefix should be
    appended to the results and the paper that are based on such code.

[^5]: If so, why are you reading this post?
[^6]:
    Code coverage tells which part of your code has been executed when you ran
    the tests. It does not necessarily tell you if the code did what was
    expected but it can at least tell that it ran without crashing.

[^7]: I think that they won't run on private repos.
[^8]:
    I have not yet checked, if it is possible to use the more user friendly
    [MyST](https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html) to
    write Sphinx doc for this.

[^9]:
    You DO have a README that says how to install and use your code, right?
    RIGHT?

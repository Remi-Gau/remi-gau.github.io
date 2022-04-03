---
layout: post
title: MATLAB clean code
date: "2022-03-31"
tags: []
categories: []
---

Recently, the great[Anibal Sólon](https://anibalsolon.com/) asked for tips about
writing clean MATLAB code.

So when someone that you consider as being

So Matlab quality code hey... In brief. Use the python package miss_hit for
static code analysis and code formating (it does some of it partially
automatically a la black)

https://florianschanda.github.io/miss_hit/style_checker.html

For tests I like the moxunit test suite https://github.com/MOxUnit/MOxUnit

Can run with both Matlab and Octave.

Don't expect something like pytest but it gets the job done pretty well.

Also has its own github action that can give you code coverage.

https://github.com/joergbrech/moxunit-action

For dependency management. It they are on github or gitlab, sub module them. If
they only exist on Matlab exchange, add them as libraries with your code.

    By the way miss hit works with pre-commit.

I would also be tempted to say to code like your user will only have access to
Octave. So avoid some the fanciest and latest Matlab features.

That also usually means relying on spm for a lot of low level stuff because it
is almost 100% Octave compatible.

If you want examples of all this.

Check bids matlab for a light version.

Check cpp spm for a much larger code base.

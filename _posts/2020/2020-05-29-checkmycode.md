---
layout: post
title: "Hey MATLAB! Check my code!"
date: "2020-05-29 00:00"
tags: []
category: []
---

Taken from this
[twitter thread](https://twitter.com/RemiGau/status/1266388006329552898)

I created a MATLAB function to help me write good code.

A thread.

A lot of us (at least in neuroscience) learn MATLAB by aping scripts we have
borrowed from someone.

One day you were given some `.m` files, a tap on the shoulder and "good luck"
and you have been reverse engineering the wheel of what it means to write good
code since then.

One of the reason for this is that people, whose code we are learning from, are
as likely as you to have taken 'How to write good code 101' (i.e very unlikely
but don't feel bad those classes are usually not proposed in most neuroscience
departments anyway).

So we don't improve because we are rarely exposed to "good" code and bad habits
are passed down from one PhD generation to the next.

At an individual and at a lab level all of this is the fastest way to end with a
codebase of MATLAB scripts of 1000 lines or above that that have more loose ends
than a bowl of spaghetti.

<iframe src="https://giphy.com/embed/11uoNyauChZR16" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>

There is no official MATLAB guidestyle.

Well there is
[THIS](https://www.mathworks.com/MATLABcentral/fileexchange/46056-MATLAB-style-guidelines-2-0)

But nothing to check compliance and even less enforce it.

And sure there is the MATLAB linter but here again it can be hard to enforce

Because we all need pointers when it comes to make our codebase better, I wanted
to be able to type `check_my_code` into MATLAB and know if things were getting
out of hand and where I should focus my attention to start cleaning my code.

The idea for this is partly inspired by this "equivalent" in
[python](https://github.com/PyCQA/mccabe)

The good thing is that the MATLAB linter gives you the
[McCabe complexity of each function](https://www.mathworks.com/help/MATLAB/ref/mlint.html).

The [McCabe complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) of
a function is presents how many paths one can take while navigating through the
conditional statements of your function (`if`, `switch`, ...).

If it gets above 10 you enter the danger zone. If you are above 15 you want to
seriously consider [refactoring](https://en.wikipedia.org/wiki/Code_refactoring)
your code with sub-functions for example.

- [refactoring.com](https://refactoring.com/)
- [refactoring.guru](https://refactoring.guru/refactoring)

The function will also roughly check if there are enough comments in the files
to make sure things are not turning into a nightmare to debug or to read, for
others or
[for yourself in 6 months](https://www.tiktok.com/@delaina00moore/video/6827954886370495749).

I also wanted to find a way to automate this and make sure this function would
run regularly so that I would not "forget" to check the quality of my code.

I mean we don't brush our teeth only on the days before we go to the dentist: so
why do we say that we will clean our code when we are ready to submit our paper
(or after it has been published)? And then we wonder why our code stink.

Because setting up a continuous integration to do that with MATLAB is turning
out to be...

<iframe src="https://giphy.com/embed/jxcMNv8wJIlb6Jp9ER" width="480" height="260" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>

So I created a git hook template that just needs to be added into your local
repository that will check the quality of your code every time you push your
code.

Obviously you could also add extra checks into this hook to run your unit tests
to make sure you have not broken anything: not as good as real CI but hey...

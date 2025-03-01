---
layout: post
title: Let's talk about NARPS
date: '2019-09-06 14:58'
tags: []
category: []
---

So there is a new study in neuroimaging that has more authors than pages. It is called Neuroimaging Analysis Replication and Prediction Study ([NARPS](www.narps.info)).

It is the equivalent of the "_One data set, many analysts_" paper that came out a few years ago.

The idea is quite simple: give the same data to a bunch of people and tell them "go forth and analyze it". Well in this case, it was more "go forth and test those 9 hypothesis the way you would usually do it in your lab."

The idea behind that type of study is to get an idea of how analytical flexibility affects results in the real world. When scientist analyze their data they have to make bazillions of choices: how to preprocess the data, how to denoise it, what data to include/exclude, how to model it... In many cases each set of decision is justifiable but in the worst case scenario, this flexibility in terms of analysis can be used (more or less consciously) to find the result we want or to the find the result that will make a nice coherent story that will be easy to sell. In neuroimaging the number of analytical decisions we have to make is so vast that it is conceivable that with enough patience one could in theory find activation in almost any part of the brain. In practice though most researchers do

good to have many teams analyse the same data
 - less issues of getting it "wrong" especially when new to the field

- good to know that the work will be published no matter what you find. Gee that must be how people who do a registered report feel like. I mean imagine that: knowing that your effort will be rewarded without having to rely on the powers of the allmighty gods of analytical flexibility to find something worth publishing in your heap of data.

Sure the idea of having an "easy" paper out is attractive and I would be a hypocrite to deny that it did not play a role in me wanting to participate in this, but knowing your results will be out there and that if they are completely out of whack with the rest of the teams this might make you look like a big dumb doofy doof. So even for the most cynical out there there is still a push to do well unless they wanna burn any kind scientific street cred they might have.

- pre-reg can speed up your work
- so can using standard data structure
- but if followed "blindly", don't run robustness checks to see if results hold under different pipeline

- nice to have hypothesis for once

- incremental pre-reg: check behavior and quality control to refine your pipeline but without looking at activations.

- standard pipelines like fMRIprep remove many researchers DOF (but can open up other)

- should have run some other pipelines or do a mini-multiverse analysis but you still need a way to choose

- should have run analysis on a couple of subjects and then decide on one pipeline
-  - including model comparison with the MACS toolbox

- should have had a less stringent inferential approach (esp wrt volume for GLM: use union of all the ROIs)


Common points and differences between being part in many-analysis team project and more a traditional one team project.
- pre-registration might mean different things or might not be as necessary as the bias of different teams might compensate each other

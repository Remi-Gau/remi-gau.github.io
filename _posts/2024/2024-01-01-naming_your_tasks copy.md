---
layout: post
title: "How to name you files: task edition"
date: "2024-01-02"
tags: [BIDS, Don'ts and dos]
categories: []
redirect_from:
  - 2022/03/31/naming_your_tasks.html
---

While browsing datasets on openneuro I came across a couple of BIDS datasets
with tasks named things like:

- `['FlavorRun1', 'FlavorRun2', 'FlavorRun3', 'FlavorRun4']`
- `['run1', 'run2', 'run3', 'run4', 'run5', 'run6']`

I'd like to give a couple of hints to better ways to name your tasks
to have more useful filenames in the end.

## Using the right entity

The brain imaging data structure gives you basic bricks from which to build your filenames.
We call them `entities`.
In general, try to make use of those bricks to help you build your filenames.

In this case there is a [`run` entity](https://bids-specification.readthedocs.io/en/latest/appendices/entities.html#run) that you can use.

So don't do this:

```
sub-01/func/sub-01_task-FlavorRun1_echo-1_bold.nii.gz
```

But do this instead:

```
sub-01/func/sub-01_task-Flavor_run-1_echo-1_bold.nii.gz
```

## Filenames as signals to other users

BIDS aims to be both human and machine friendly.

In this way your filename should contain "signals" **to other users** about what the file contains.

With a file called:

```
sub-01/eeg/sub-01_task-run1_eeg.edf
```

you are going to be hard pressed to be able to known what the task was about.
**YOU**, as the person who acquired the dataset, may know what is in that that file,
but future users of that dataset will not.

But if the file is named:

```
sub-01/eeg/sub-01_task-MusicListening_run-1_eeg.edf
```

It will already be a lot easier to get an idea as to what participants were doing during this task.

## Metadata to the rescue

You may be tempted to go overboard and pack as much information as possible in the filenme as possible.

For example in [one of the bids examples](https://github.com/bids-standard/bids-examples/tree/master/ds006/sub-01/ses-post/func),
you can come across files with this kind of names:

```
sub-01/ses-post/func/sub-01_ses-post_task-livingnonlivingdecisionwithplainormirrorreversedtext_run-01_bold.nii.gz
```

In this case we know a lot about what was going on jut from the filename... If we can decypher it.

If you REALLY want to keep such a long task label, as least use CamelCase to make it easier to read.

```
sub-01/ses-post/func/sub-01_ses-post_task-LivingNonLivingDecisionWithPlainOrMirrorReversedText_run-01_bold.nii.gz
```

A better approach if you want to convey additional information about your data
is to use the the JSON sidecars to add extra-matadata.

Currently this file could look like this:

```
sub-01/ses-post/func/sub-01_ses-post_task-livingnonlivingdecisionwithplainormirrorreversedtext_run-01_bold.json
```

And contains this:

```json
{
  "TaskName": "living-nonliving decision with plain or mirror-reversed text",
  "RepetitionTime": 2.0
}
```

Better to name your file like this:

```
sub-01/ses-post/func/sub-01_ses-post_task-decision_run-01_bold.nii.gz
```

And pack the extra information in the the sidecar file.

```
sub-01/ses-post/func/sub-01_ses-post_task-decision_run-01_bold.json
```

```json
{
  "TaskName": "decision",
  "RepetitionTime": 2.0,
  "TaskDescription": "Subjects are presented with words in either plain text or mirror-reversed format, and are asked to judge whether the stimulus refers to a living or nonliving object. Items are presented in a mixed fashion and separated by whether each stimulus is a switch in presentation form from the previous trial.",
  "CogAtlasID": "https://www.cognitiveatlas.org/id/trm_5176cf9d3d512/",
  "Instructions": "Subjects were told to …"
}
```

Note that you can even link to aspecific task of the [cognitive atlas](https://www.cognitiveatlas.org/tasks/a/)
if the type of task you are using if indexed there.

You may complain that your favorite BIDS converter
does not allow you to easily add this extra metadata during the conversion process.
And that you are not to fond of the idea of modifying manually dozens of JSON files per subject
to add this information.

In this case, you can make use of the [BIDS inheritance principle](https://bids-specification.readthedocs.io/en/latest/common-principles.html#the-inheritance-principle)
and simmply add a single file in the root of your dataset:

```
task-decision_bold.json
```

with the metadata that applies to this task.

```json
{
  "TaskName": "decision",
  "RepetitionTime": 2.0,
  "TaskDescription": "Subjects are presented with words in either plain text or mirror-reversed format, and are asked to judge whether the stimulus refers to a living or nonliving object. Items are presented in a mixed fashion and separated by whether each stimulus is a switch in presentation form from the previous trial.",
  "CogAtlasID": "https://www.cognitiveatlas.org/id/trm_5176cf9d3d512/",
  "Instructions": "Subjects were told to …"
}
```

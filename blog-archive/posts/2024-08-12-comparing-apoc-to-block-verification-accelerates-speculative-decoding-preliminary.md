---
title: "Comparing APOC to “Block Verification Accelerates Speculative Decoding” (preliminary)"
date: 2024-08-12T20:30:12+00:00
modified: 2024-08-12T20:31:50+00:00
url: https://masharpe.wordpress.com/2024/08/12/comparing-apoc-to-block-verification-accelerates-speculative-decoding-preliminary/
tags: ["coupling", "llm", "paper", "research"]
categories: ["Uncategorized"]
---

# Comparing APOC to “Block Verification Accelerates Speculative Decoding” (preliminary)

While browsing speculative decoding papers today, I came across [“Block Verification Accelerates Speculative Decoding” (Sun et al. 2024)](https://arxiv.org/abs/2403.10444) from Google Research. This preprint contains the key ideas of all-prefix-optimal coupling (APOC), so here are my preliminary thoughts based on skimming (so errors are likely). More specifically, there are two versions of the preprint:

- 2024-03-15: In this version, their main algorithmic result is `BlockVerify`, which is essentially the same as what I’ve been calling APOC conditional sampling.
- 2024-07-25: In this version, the original algorithm has been renamed “greedy block verification” and demoted to Appendix C, since they present an alternative new algorithm “block verification”, which avoids creating a residual model, that reportedly has fewer mispredicts in empirical testing.

The situation makes me wish that I found a better way to broadcast my work, but likely the Google team was ahead at all points. While [my first blog post on APOC was posted 2024-03-05](2024-03-05-all-prefix-optimal-coupling-for-model-comparison.md), a few days before the March preprint was uploaded to arXiv, that blog post was much less well-developed in terms of material. In particular, at that point I only had a sketch of the unconditional sampling algorithm, and I hadn’t yet worked out the conditional sampling algorithm (which is trickier).

In the particular case of being able to efficiently apply APOC to speculative decoding, they were far ahead of me, since I only this morning realized that the draft model can be cheaply coupled to the residual model (since forward pass results of the draft model can be reused). That observation already appears in the March preprint:

> This doesn’t increase the number of calls to the large model and small model.

A more minor observation is that the motivating example they present in Section 2 of the July version [is also an example I’ve found useful](2024-06-27-two-useful-simple-counterexamples-of-string-coupling.md).

Although the key ideas of APOC are certainly in their preprints, more reading will be needed to understand the differences in detail. Thematically, I’ve been primarily interested in the application of APOC to comparing response distributions, whereas they restrict their attention solely to speculative decoding. That has likely led me to different minor results than theirs. However, the most interesting result is definitely APOC itself, so it’s disappointing to be scooped.

Still, despite my disappointment, I’m glad that the idea is out there being helpful. After all, I was making only slow progress on broadcasting it myself, and I wasn’t focused on speculative decoding. [For example, my demo currently only supports prompt engineering.](https://huggingface.co/spaces/masharpe/all-prefix-optimal-coupling-demo-1)

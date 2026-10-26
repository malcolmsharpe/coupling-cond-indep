---
title: "Approach for writing recent results"
date: 2024-10-11T22:24:10+00:00
modified: 2024-10-11T22:24:10+00:00
url: https://masharpe.wordpress.com/2024/10/11/approach-for-writing-recent-results/
tags: ["reflection", "research", "writing"]
categories: ["Uncategorized"]
---

# Approach for writing recent results

Over the past few months, starting [with this post on Feb 3](2024-02-03-method-for-comparing-creative-writing-models-more-easily-inspired-by-speculative-sampling.md), I have investigated the application of coupling to LLM-inspired problems. At some point, I need to write up the fruits of this research.

My goal is to upload a preprint to arXiv. To do that, I need an arXiv-ready preprint. To obtain an arXiv-ready preprint, I need to extensively edit and polish a rough draft. To write a rough draft, I need a key idea to anchor it.

My original pick for the key idea was going to be “APOC” (All-Prefix-Optimal Coupling, though “All-Prefix-Maximal Coupling (APMC)” would have been a better choice of name): the surprising fact that per-token maximal coupling does not maximally couple whole responses, yet with care it’s possible to simultaneously maximal couple every prefix of the response. However, this turned out to have already been shown by Sun et al 2024 with the name “Greedy Block Verification”. Moreover, it turned out to have been shown earlier in other contexts, such as by [Vollering 2016](https://arxiv.org/abs/1608.01511), and the key ideas seem to go back at least as far as [Griffeath 1975](https://link.springer.com/article/10.1007/BF00539434).

Despite the lack of novelty, in hindsight it would have been useful to write my take on APMC. It would have been good writing practice, and my point-of-view may have some slight novelty to it, although it’s hard to say for sure given the massive amount of Markov chain literature on couplings.

What actually happened is that, after a period of discouragement, I found refuge in a conjecture about [simultaneously maximal coupling of independent variables](2024-07-11-conjecture-non-crossing-family-optimal-coupling.md). I’ve searched many times to try to find this in the literature, and I have not, so it may actually be novel. If so, the reason would be that there is no independence between variables in the Markov chain setting, so there’s no reason for researchers in that area to consider this question.

It turns out that the solution to this conjecture involves an exceptionally beautiful gem of an algorithm, which I call the “maximal recoupling” (MRC) algorithm. It’s a tiny but non-obvious generalization of the classic maximal coupling algorithm, and remarkably does not seem to have been published before, as far as I can tell.

This time around, I’m resolved to write even if MRC turns out to be not novel, for the reasons I mentioned before: I need the writing practice, and my viewpoint might be novel even if the material isn’t. Moreover, I’ve looked hard enough to conclude that, if MRC is known, it’s not *well*-known.

As beautiful as MRC is, on its own it is not very motivated. Its motivation comes from simultaneously maximal coupling of independent varibles (SMC-I) or more generally Bayesian networks (SMC-BN). In turn, SMC-BN is motivated by SEDD LLMs. Just as APMC (or perhaps I should say SMC-AR, for “auto-regressive”) can allow spec dec and evaluation variance reduction for AR LLMs, SMC-BN may allow spec dec and evaluation variance reduction for SEDD LLMs.

But to include that motivation greatly expands the volume of material to write, to the point that I worry I would not finish even a rough draft, never mind an arXiv-ready preprint. For example, just [the pseudocode for the SMC-BN algorithm already amounts to about 100 lines](2024-10-08-full-pseudocode-for-sampling-from-a-simultaneous-maximal-coupling-of-bayesian-networks.md). The analysis is also quite extensive and has some remaining minor holes that would need time to plug. Worse, I dread it, because much of the material, while not entirely obvious, is not as interesting as MRC.

Thus, faced with the possibility of having nothing to show for my work up to now, and having asked for advice, I have decided to employ a “fun first” approach: I’ll write about the fun part (MRC), without being troubled by its lack of motivation. The initial versions can also omit needed background. This makes the goal feel more achievable, and if I do at least get a rough draft presenting MRC, I’ll have a useful artifact even if I move on from the project before completing the other parts of it.

Another benefit of restricting the scope to just MRC is to focus me on creating a high-quality presentation of that small amount of material. I’ll find it more rewarding to produce a clear and concise exposition of MRC alone than a sprawling mess for SMC-BN as a whole.

The first step is to begin assembling my notes on MRC specifically into a rough draft.

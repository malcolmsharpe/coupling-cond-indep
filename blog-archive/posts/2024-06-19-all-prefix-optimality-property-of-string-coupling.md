---
title: "All-prefix-optimality property of string coupling"
date: 2024-06-19T19:56:27+00:00
modified: 2024-06-19T19:56:27+00:00
url: https://masharpe.wordpress.com/2024/06/19/all-prefix-optimality-property-of-string-coupling/
tags: ["coupling", "llm", "research"]
categories: ["Uncategorized"]
---

# All-prefix-optimality property of string coupling

Two discrete distributions over the same finite set can be coupled so as to simultaneously maximize the probability of coinciding on every element. (See, for example, [Angel and Spinka 2021](https://arxiv.org/abs/1903.00632).) If the finite set consists of strings, then we can choose the coupling to also simultaneously maximize the probability of coinciding on every prefix value. We’ll call this latter simultaneous maximization property “all-prefix optimality”. It’s what APOC is constructed to achieve.

I discussed the all-prefix-optimality property in [my first post on APOC](2024-03-05-all-prefix-optimal-coupling-for-model-comparison.md), so consider this a revisiting with the notation I prefer now.

## Optimal coupling (general elements)

If X and Y are two random variables with different distributions over the same finite set, then for every element a of the set, we obviously have the upper bound

```
P[X = Y = a] <= min{P[X = a], P[Y = a]}
```

Less obvious is that there exists a coupling such that, for every a, the upper bound is achieved:

```
P[X = Y = a] = min{P[X = a], P[Y = a]}
```

Note that this coupling is in general non-unique.

This optimal coupling is used implicitly by speculative sampling for LLMs.

## All-prefix-optimality property

Now assume that the finite set consists of strings. For every string a in the set and length i, we obviously have the upper bound

```
P[X_{<i} = Y_{<i} = a_{<i}] <= min{P[X_{<i} = a_{<i}], P[Y_{<i} = a_{<i}]}
```

Surprisingly, there again exists a coupling that, for every a and i, achieves the upper bound:

```
P[X_{<i} = Y_{<i} = a_{<i}] = min{P[X_{<i} = a_{<i}], P[Y_{<i} = a_{<i}]}
```

Again, this all-prefix-optimal coupling is in general non-unique.

As far as I can tell, my posts on this blog are the first public description of all-prefix-optimal coupling.

## Discussion

If indeed all-prefix-optimal coupling was only recently discovered, why wasn’t it discovered earlier? The math involved is extremely elementary, and the result strikes me as at least a little interesting in isolation, even ignoring that it has applications to generative AI.

My guess is that, although the problem makes no explicit reference to GenAI, it didn’t arise naturally in the pre-GenAI era. If it weren’t for GenAI, you’d be unlikely to be sampling from string distributions, and, even if you were, the sampling might not proceed auto-regressively. Even once sampling auto-regressively from string distributions, for APOC to be useful, you additionally need those two distributions to be close to equal, which occurs in GenAI for many reasons (e.g. quantization, fine-tuning, prompt engineering, sampler configuration), but maybe it doesn’t appear elsewhere much.

Interestingly, even within the field of LLMs, I haven’t seen much public discussion of using coupled responses to compare models. A rare example is [Artefact2’s comparison of quantizations by reusing a seed](https://github.com/Artefact2/llm-eval).

It also remains possible that APOC actually doesn’t work. This will only be truly settled once I’ve created an implementation and compared its performance to the theoretical prediction.

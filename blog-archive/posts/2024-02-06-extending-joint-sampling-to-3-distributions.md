---
title: "Extending joint sampling to 3+ distributions"
date: 2024-02-06T19:37:00+00:00
modified: 2024-02-06T19:37:00+00:00
url: https://masharpe.wordpress.com/2024/02/06/extending-joint-sampling-to-3-distributions/
tags: ["llm", "sampling"]
categories: ["Uncategorized"]
---

# Extending joint sampling to 3+ distributions

Imagine we have several models that we want to jointly generate from, making their generations as similar as possible. For example, we might want to generate from several quantizations of a single model.

## A minimum-spanning-tree heuristic for joint sampling from 3+ distributions

The elemental operation required is to jointly sample from `k` discrete probability distributions over the same set, such that the samples are as similar as possible (in some sense). Speculative sampling does this [optimally](2024-02-05-optimality-of-speculative-sampling-style-resampling-one-token.md) for `k = 2`.

For `k >= 3`, let’s try making repeated use of the `k = 2` case. Suppose we start with some distribution, then repeatedly select an unsampled distribution, pairing it with one of the sampled distributions, applying the `k = 2` case. Once we’ve sampled all the distributions, we’ve obtained a tree, where the nodes are the distributions, and each edge connects distribitions that we applied the `k = 2` case to. Furthermore, the expected number of resamplings that occurred while building this tree is equal to half its cost, where each edge cost is equal to the L1 distance between the distributions it connects.

Minimizing the expected number of resamplings is a reasonable goal, which we can do by building the tree using Prim’s algorithm for minimum spanning tree (MST). The resulting heuristic has some nice properties:

- For `k = 2`, it reduces to the technique used in speculative sampling.
- Whenever two of the distributions are exactly equal, they will generate the same token with probability 1.

Although the heuristic involves an arbitrary choice of starting node, I conjecture that the implied joint distribution depends only on the final tree and not on the choice of starting node.

How would we expect the MST heuristic to behave in a practical case? For example, if we use an FP16 model along with several quantizations of it, I’d guess that each quant is typically most similar to the original model. (Whether this is true depends on how consistent quantization error is for different bitrates.) In that case, the tree will be a star centered on the FP16 model.

## Increasing stability further

Note that there is certainly better possible than this MST heuristic.

An easy improvement is to introduce dependence in the choice of whether-to-resample. In addition to sampling a token `x` according to `p(x)`, also sample a number `a` between 0 and `p(x)`. If `a < q(x)`, then use `(x, a)` as the token and number for the distribution `q`. Otherwise, sample `y` according to `max{0, q(y) - p(y)}` (normalized) and sample a number `b` between `p(y)` and `q(y)`. This resampling procedure gives the distribution over `y` and `b` as if you had sampled from `q` originally.

An extreme approach would be to optimize an arbitrary linear function of the joint distribution using a linear program with `n^k` variables, where `n` is the alphabet size. This however is going to become intractable quickly.

I suspect that there’s a compromise linear program with `n 2^k` variables, but I haven’t figured out the details to know whether it really works. The variables would be, for each token `x` and each set `A` of distributions,

```
P[every distribution in A samples x /\ every distribution in not-A samples not-x]
```

In any case, before pursuing these fancy generalizations, it makes sense to first verify that even the `k = 2` case produces usable results, which I have not yet done.

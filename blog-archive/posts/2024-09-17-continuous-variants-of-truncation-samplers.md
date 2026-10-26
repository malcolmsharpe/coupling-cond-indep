---
title: "Continuous variants of truncation samplers"
date: 2024-09-17T00:17:05+00:00
modified: 2024-09-17T00:17:05+00:00
url: https://masharpe.wordpress.com/2024/09/17/continuous-variants-of-truncation-samplers/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
archive_note: related post not in the author's core list
---

# Continuous variants of truncation samplers

To improve the quality of LLM outputs, particularly with often-glitchy open source finetunes, people often use truncation samplers to clamp the probabilities of unlikely tokens to zero. OpenAI-compatible APIs support Top-K and Top-P. Open source inference offers more options, and Min-P is particularly popular.

An odd property of the truncation samplers mentioned above (Top-K, Top-P, Min-P) is that they are all discontinuous as functions of probability vectors. i.e. There are raw probability vectors for which small perturbations cause large changes in the post-truncation-sampler probability vector.

You might wonder why we should care whether the samplers are continuous. Indeed, for practical inference, a discontinuous sampler is fine. But we may care about sample continuity when comparing similar models or similar sampling parameters using coupling, because all reasonable coupling methods will achieve 100% agreement in the equal distribution limit. At a point where the sampler is discontinuous, the equal distribution limit doesn’t apply, so the coupling might not achieve 100% agreement.

A couple specific use cases where it’s worth considering continuous samplers:

- When using coupling to compare a quantization to a reference model, with samplers applied.
- When tweaking sampler parameters and inspecting the change using coupling.

In this post, for each sampler, we’ll look at the causes of its discontinuity and propose a continuous variant, if possible.

## Top-K

The Top-K sampler takes a parameter k. It zeros all but the largest k probabilities, then renormalizes.

Top-K is discontinuous when the probabilities at rank k and rank k+1 are equal. Small perturbations can change that ranking, causing those two probabilities to jump between zero and nonzero.

There is no natural continuous variant of Top-K. To see why, consider when there are k+1 equal probabilities. There’s no way to decide which k of them to retain.

Luckily, Top-K is not popular, so lacking a continuous variant is not a big problem.

## Top-P

The Top-P sampler takes a parameter alpha. It accumulates probabilities from largest down until accumulating a total alpha, zeros the remainder, then renormalizes.

Top-P is discontinuous when the probabilities at the cutoff are equal. Small perturbations can change the ordering, flipping probabilities from one side of the cutoff to the other.

To make a continuous variant of Top-P, find the amount beta to subtract from every probability such that the remaining probability is exactly alpha, then renormalize. i.e. Beta is chosen so that

```
sum_i max{0, p_i - beta} = alpha
```

Beta can be found through a variety of methods, such as binary search.

Observe that this continuous variant doesn’t depend on the sorted order of the probabilities, so it doesn’t suffer from the discontinuity of ordinary Top-P.

## Min-P

The Min-P sampler takes a parameter alpha. It identifies the maximum probability p_max, zeros every probability smaller than alpha\*p_max, then renormalizes.

Min-P is discontinuous when a probability is equal to the cutoff. A small perturbation of that probability causes it to fluctuate between zero and nonzero.

To make a continuous variant of Min-P, simply subtract alpha\*p_max from every probability, then renormalize. i.e. Each probability p_i is replaced by

```
max{0, p_i - alpha*p_max}
```

This still zeros every probability below alpha\*p_max, but it changes other probabilities too.

Compared to ordinary Min-P, the large probabilities are slightly increased and the probabilities near the cutoff are moderately decreased, so we’d expect the overall effect to loosely resemble combining Min-P with a lowered temperature.

---
title: "Conjecture: in the auto-regressive case, SMCBN yields the same distribution as APOC"
date: 2024-10-09T21:03:30+00:00
modified: 2024-10-09T21:03:30+00:00
url: https://masharpe.wordpress.com/2024/10/09/conjecture-in-the-auto-regressive-case-smcbn-yields-the-same-distribution-as-apoc/
tags: ["conjecture", "coupling", "research"]
categories: ["Uncategorized"]
---

# Conjecture: in the auto-regressive case, SMCBN yields the same distribution as APOC

Although originally envisaged as a generalization of all-prefix-optimal coupling (APOC), [the simultaneously maximal coupling of Bayesian networks (SMCBN) sampling algorithm](2024-10-08-full-pseudocode-for-sampling-from-a-simultaneous-maximal-coupling-of-bayesian-networks.md) is rather different at first glance. For one thing, SMCBN involves a great deal of rejection sampling. Yet it seems likely that, in the auto-regressive case where they both apply, APOC and SMCBN are fundamentally the same method.

The first step towards verifying this idea is to check whether APOC and SMCBN yield the same distribution, in the auto-regressive case where SMCBN uses only the `ChainRule` construction, not the `TensorProduct` construction.

Thankfully, [we know conditions that fully characterize the APOC coupling](2024-06-21-specifying-apoc.md). One is the all-prefix-optimality property, which SMCBN obviously satisfies. The other two are symmetric conditional independence properties. [Recall that MRC is symmetric](2024-10-04-progress-towards-proving-properties-of-the-maximal-recoupling-algorithm.md), so it’s enough to check one of these two properties.

This property, stated in terms of one application of `ChainRule` then `MRC`, is, for all a,b,

```
Y_2 = b_2 ⫫ X = a | Y_1 = b_1 /\ X != Y

<=>

Phat[Y_2 = b_2 | X = a, Y_1 = b_1, X != Y]
    = Phat[Y_1 = b_1 | Y_1 = b_1, X != Y]
```

## Proof idea

The idea of the proof is clear, but it’s not yet rigorous enough to call the result a theorem rather than a conjecture.

A helpful observation is that when `ChainRule` and `MRC` are merged together, the loop body has the form of:

- Sample `b^{i+1}_1`, with probability depending on `b^i_1` only.
- Sample `b^{i+1}_2`, with probability depending on `b^{i+1}_1` only.
- Perhaps accept `b^{i+1}`, with probability depending on `b^{i+1}` only.

This can be reordered into equivalently:

- Sample `b^{i+1}_1`, with probability depending on `b^i_1` only.
- Perhaps accept `b^{i+1}_1`, with probability depending on `b^{i+1}_1` only.
- Sample `b^{i+1}_2`, with probability depending on `b^{i+1}_1` only, adjusted for the fact `b^{i+1}` accepted.

Thus, the walk that appeared to be on `b` is really a walk just on `b_1` only. This relies on the particular form of `ChainRule`–the same idea wouldn’t work with `TensorProduct`, because in that case the sampled `b^{i+1}` is influenced by both components of `b^i`.

With that observation in hand, we want to show that, if we know `X != Y` and `Y_1 = b_1`, then knowing `X = a` gives no additional information about `Y_2`.

- `X != Y` tells us that MRC returned from an iteration of its loop. Call this iteration k.
- So, in iteration k, `b^{k+1}_1 = b_1` was sampled from the maximal subcoupling.
- MRC then accepted `b^{k+1}_1`.
- Then, some unknown `b^{k+1}_2 = b_2` was sampled with probability proportional to `max{0, P[Y=b] - P[X=b]}`.

I don’t see any influence of `X=a` at this point, but proving that rigorously is tricky.

---
title: "Key subroutine for simultaneously maximal coupling"
date: 2024-10-01T17:29:14+00:00
modified: 2024-10-01T17:29:14+00:00
url: https://masharpe.wordpress.com/2024/10/01/key-subroutine-for-simultaneously-maximal-coupling/
tags: ["algorithm", "conjecture", "coupling", "research", "sampling"]
categories: ["Uncategorized"]
---

# Key subroutine for simultaneously maximal coupling

Yesterday, I had a breakthrough on the problem of sampling from simultaneously maximal couplings of Bayesian networks (SMCBN). The key step is sampling from a maximal coupling that is constructed to preserve subcouplings, and, in contrast to the complicated approaches I was exploring, I chanced on a beautifully simple solution that generalizes the standard algorithm for sampling from a maximal coupling.

This post shows that algorithm. I don’t know whether it’s original, since it’s so simple–but I need the writing practice, even if it turns out to be known. Also, although the algorithm is itself simple, proving the various properties of it is not as easy–they all remain conjectures. (So it’s still possible that the algorithm doesn’t work at all!)

## Maximal recoupling algorithm

We are given random variables X and Y that take values in the same finite set S. We are also given a joint distribution P of X and Y. Here is an algorithm to produce samples from a new joint distribution Phat:

**Algorithm (maximal recoupling).**

1. Sample a with probability `P[X=a]`.
2. With probability `min{1, P[Y=a]/P[X=a]}`, return `(a,a)`.
3. Let b_1 = a.
4. For i = 1, 2, …:
   1. Sample b_{i+1} with probability `P[Y = b_{i+1} | X = b_i]`.
   2. With probability `(1 / P[Y=b_{i+1}]) max{0, P[Y=b_{i+1}] - P[X=b_{i+1}]}`, return `(a, b_{i+1})`.

That’s all. Note that `1 - min{1, P[Y=b]/P[X=b]} = (1 / P[Y=b]) max{0, P[Y=b] - P[X=b]}`, so the two probability expressions in the algorithm arise from the same accept/reject criterion.

## Relationship to standard maximal coupling

The algorithm above is remarkably similar to the classic algorithm for maximal coupling, which I reproduce here:

**Algorithm (classic maximal coupling).**

1. Sample a with probability `P[X=a]`.
2. With probability `min{1, P[Y=a]/P[X=a]}`, return `(a,a)`.
3. Repeat:
   1. Sample b with probability `P[Y = b]`.
   2. With probability `(1 / P[Y=b]) max{0, P[Y=b] - P[X=b]}`, return `(a, b)`.

In fact, the classic algorithm is simply the special case where X and Y were initially independent.

## Conjectured properties of the maximal recoupling algorithm

Conjectured properties:

- Phat is a valid coupling of X and Y. (i.e. It preserves the given marginal distributions of X and Y.)
- Phat maximally couples X and Y.
- The algorithm terminates with probabilility 1.
- Moreover, in one execution of the algorithm, the expected number of loop iterations is 1.
- For every partition of S into equivalence classes [-]:
  - `Phat[ [X] = [Y] ] >= P[ [X] = [Y] ]`.
  - Moreover, if [X] and [Y] were maximally coupled by P, then the joint distribution of `([X], [Y])` is preserved.

Notice that all but the last pair of properties are well-known to hold for the classic maximal coupling algorithm.

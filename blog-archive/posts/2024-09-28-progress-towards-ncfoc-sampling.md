---
title: "Progress towards NCFOC sampling"
date: 2024-09-28T19:37:28+00:00
modified: 2024-09-28T19:37:28+00:00
url: https://masharpe.wordpress.com/2024/09/28/progress-towards-ncfoc-sampling/
tags: ["algorithm", "coupling", "research", "sampling"]
categories: ["Uncategorized"]
---

# Progress towards NCFOC sampling

In [a recent post](2024-09-23-general-lemma-for-simultaneously-maximal-coupling.md), I showed a proof for a lemma that, together with easy induction, proves NCFOC, and, more generally, SMCBN. The lemma sets up an LP and proves that every optimal solution of the LP satisfies the desired properties. But the original motivation for studying this problem was to create *algorithms* for coupling, and the lemma proof has two related problems in that regard:

- The proof only works for random variables that range over finite vocabularies, not infinite vocabularies.
- Even if the vocabulary is finite, the LP will typically be prohibitively large, making it impractical to solve.

So, to achieve practical algorithms, we need to find an alternative proof for the lemma. This may not be easy.

To aid progress towards the full lemma, let’s solve a simpler problem: altering the given joint distribution so that it maximally couples one particular specified element `a in Sigma`, while preserving any existing maximal couplings of index subsets.

## Solution

We’ll make use of the exchange move we used in the lemma, i.e.

```
(a,b) (c,a) => (a,a) (c,b)
```

The challenge is applying this exchange move efficiently.

We begin by sampling from the given joint. There are four cases (where b != a and c != a):

```
(a,a)
(a,b)
(c,a)
(c,b)
```

The cases `(a,a)` and `(c,b)` will be accepted as-is.

We’ll say that the case `(a,b)` *demands* Y=a and the case `(c,a)` *supplies* Y=a. The actual amount of Y=a moved around we’ll call the *flow*, where `flow = min{demand, supply}`. We have

```
demand = P[X=a] - P[X=a,Y=a]
supply = P[Y=a] - P[X=a,Y=a]
flow = min{P[X=a],P[Y=a]} - P[X=a,Y=a]
```

In case `(a,b)`, with probability `flow / demand`, replace Y=b with Y=a. (Otherwise, we keep Y=b.)

In case `(c,a)`, with probability `flow / supply`, we’ll replace Y=a. (Otherwise, we keep Y=a.) We sample the replacement b with probability `P[Y=b | Y != X, X=a]`. There are two reasonable options for the algorithm for sampling the replacement:

- Use rejection sampling by sampling b with probability `P[Y=b | X=a]` until b != a. To use this option, we’d need to check that the number of samples drawn isn’t too large.
- Assume that the given joint distribution supports directly sampling b with probability `P[Y=b | Y != X, X=a]`. This is in fact possible for the joint distributions of interest to us, but it does require a proof.

## Formulas for acceptance and rejection probabilities

I’m unsure of the usefulness of these formulas, but here they are for later reference:

```
flow / demand = (min{pX, pY} - pXY) / (pX - pXY)
1 - flow/demand = (pX - min{pX, pY}) / (pX - pXY)
```

And similarly for `flow / supply`.

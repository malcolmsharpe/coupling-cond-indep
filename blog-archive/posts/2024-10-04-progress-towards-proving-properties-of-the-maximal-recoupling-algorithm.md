---
title: "Progress towards proving properties of the maximal recoupling algorithm"
date: 2024-10-04T21:11:55+00:00
modified: 2024-10-04T21:11:55+00:00
url: https://masharpe.wordpress.com/2024/10/04/progress-towards-proving-properties-of-the-maximal-recoupling-algorithm/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Progress towards proving properties of the maximal recoupling algorithm

In my previous posts, I presented the [maximal recoupling algorithm](2024-10-01-key-subroutine-for-simultaneously-maximal-coupling.md) and [detailed its conjectured properties](2024-10-02-details-of-maximal-recouplings-effect-on-subcouplings.md). Today’s post presents progress towards proving the properties. The properties and their status:

- Coupling validity:
  - Marginal of X: obvious.
  - Marginal of Y: today.
- Coupling maximality: obvious.
- Termination: today.
- Efficiency: todo.
- Effect on subcouplings: todo.

## Marginal of Y

We must prove that the maximal recoupling algorithm preserves the marginal distribution of Y. We’ll use a symmetry approach: we’ll show that running MRC on (X,Y) and (Y,X) yield the same coupling, so, since the marginal distribution of X is obviously preserved, the marginal distribution of Y is preserved too.

The case where MRC returns equal values is obvious, so we only need analyze the loop. When MRC returns `(b_1, b_{k+1})`, we’ll say that its *trajectory* was `b_1, b_2, ..., b_{k+1}`. We will calculate the probability of a given trajectory per execution of MRC (which includes the case where the loop isn’t entered, so the sum of the probabilities can be less than 1).

First, note that if there is any `2 <= i <= k` such that `P[X = b_i] = 0` or `P[Y = b_i] = 0`, the probability of the trajectory is zero. Otherwise, its probability is given by

```
max{0, P[X = b_1] - P[Y = b_1]}
    * Prod_{i=1}^k P[Y = b_{i=1} | X = b_i]
    * Prod_{i=1}^{k-1} min{1, P[X = b_{i+1}] / P[Y = b_{i=1}]}
    * max{0, 1 - (P[X = b_{i+1}] / P[Y = b_{i+1}])}

= max{0, 1 - P[Y = b_1] / P[X = b_1]}
    * Prod_{i=1}^k P[Y = b_{i=1}, X = b_i]
    * Prod_{i=2}^k min{ 1 / P[X = b_i], 1 / P[Y = b_i] }
    * max{0, 1 - P[X = b_{k+1}] / P[Y = b_{k+1}]}
```

From this expression, it’s clear that it’s the same as the probability of the reverse trajectory `b_{k+1}, ..., b_1` when MRC is applied to (Y,X) instead, which proves the symmetry.

## Termination

To show termination, we’d like to analyze the trajectory `b_1, ..., b_{k+1}` as a Markov chain and show that it’s absorbing. However the transition probabilities implied by the loop don’t necessarily define an absorbing Markov chain: a simple example is if X and Y both are constant with the same value. Instead, we’ll show that, with probability 1, the initial state b_1 can only reach states that themselves can reach absorbing states.

To do that, consider a directed graph `G = (V,A)` where V is the (finite) set of values taken by X and Y and A consists of those arcs `i,j` for which the flow `w_{ij} = P[X = i, Y = j]` is nonzero. We’ll say `i in V` is

- A *source* if `sum_j w_{ij} > sum_j w_{ji}`. i.e. `P[X = i] > P[Y = i]`.
- A *sink* if `sum_j w_{ij} < sum_j w_{ji}`. i.e. `P[X = i] < P[Y = i]`.

Observe that the MRC loop takes a random walk in G, starting at a source and ending at a sink. It’s enough to show that for every source i and every node j reachable from i, there exists a sink k reachable from j.

Suppose otherwise: take a source i and node j reachable from i such that there is no sink reachable from j. Let J be the set of nodes reachable from j, including j itself. Then:

- J has no out-arcs, so its net outflow is non-positive.
- J has no sinks, so its net inflow is non-positive.
- Thus, J has zero net flow.
- Since J has zero net flow and no sinks, it has no sources, so `i not in J`.
- Since J has no out-arcs and zero net flow, J has no in-arcs.
- But then `i not in J` has no directed path to `j in J`, a contradiction.

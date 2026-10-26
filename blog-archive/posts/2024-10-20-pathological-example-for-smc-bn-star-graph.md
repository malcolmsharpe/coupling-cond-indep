---
title: "Pathological example for SMC-BN: star graph"
date: 2024-10-20T17:39:12+00:00
modified: 2024-10-20T17:39:12+00:00
url: https://masharpe.wordpress.com/2024/10/20/pathological-example-for-smc-bn-star-graph/
tags: ["coupling", "example", "research"]
categories: ["Uncategorized"]
---

# Pathological example for SMC-BN: star graph

A consequence of SMC-BN is that, when X and Y consist of n subvariables each, it’s always possible to simultaneously maximally couple n (non-empty) sets, and at best it’s possible to simultaneously maximally couple 2n-1 sets (in the case where the subvariables are all independent).

But there is a puzzling asymmetry, shown strongly when X and Y are Bayesian networks with respect to a star graph G. When the arcs of G point in towards the center, 2n-2 sets may be simultaneously maximally coupled. But when the arcs of G point out away from the center, only n sets may be simultaneously maximally coupled, no better than the general case!

That a arcs-from-center star graph performs so poorly is counterintuitive, because it *looks* like a restrictive condition: when conditioned on the center, all the leaves are conditionally independent.

Here’s an explicit example to show why this star graph is not favorable for SMC. Let

```
X_0 ~ Unif(\Z_n)
Y_0 ~ Unif(\Z_n)

For 1 <= i <= n-1,
    X_i = X_0
    Y_i = Y_0 + i (mod n)
```

Note that `\Z_n` means the integers mod n. Observe that both X and Y are Bayesian networks with respect to a star graph G where the center is 0 and the arcs point outwards from the center.

In words:

- For X, all subvariates are equal, with the value chosen at random from `\Z_n`.
- For Y, its subvariates are an increment cycle through all members of `\Z_n`, with the offset chosen at random.

For every i, `D_TVD(X_i, Y_i) = 0`, so every subvariable pair can be perfectly coupled in isolation. But there is always exactly one i such that `X_i = Y_i`, and all the others are not-equal. So at best only one subvariable pair can be simultaneously maximally coupled.

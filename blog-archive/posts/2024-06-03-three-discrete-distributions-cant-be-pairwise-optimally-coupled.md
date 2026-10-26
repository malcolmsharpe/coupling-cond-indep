---
title: "Three discrete distributions can’t be pairwise-optimally coupled"
date: 2024-06-03T19:38:41+00:00
modified: 2024-06-03T19:38:41+00:00
url: https://masharpe.wordpress.com/2024/06/03/three-discrete-distributions-cant-be-pairwise-optimally-coupled/
tags: ["coupling", "llm", "probability", "sampling"]
categories: ["Uncategorized"]
---

# Three discrete distributions can’t be pairwise-optimally coupled

In previous posts, I’ve presented a method All-Pairs-Optimal Coupling (APOC) for generating from two similar LLMs in a way that promotes similarity of the responses, which is useful for evaluation. The “optimal” in the name is justified by APOC matching the natural upper bound `P(X = Y = a) <= min{P(X = a), P(Y = a)}` for every prefix `a`.

It would be nice to extend APOC to generation from three or more LLMs while retaining the optimality property for each pair of LLMs. Unfortunately, this is not possible. It’s not the prefix complication that makes it impossible either, because it’s impossible even for sampling just one token.

The material below explains why and explores the consequences.

## Problem statement

Consider a finite set V and two discrete distributions P and Q over X. (For example, V could be the token vocabulary of an LLM.) We’ll simultaneously draw from P and Q and consider the expected non-equality cost `c(x,y) = { 0 if x = y; 1 if x != y }`.

Using an optimal coupling, the minimum cost is the total variation distance (TVD):

```
(1/2) sum_x |P(x) - Q(x)|
```

It’s natural to ask, given another distribution R, can we simultaneously couple all three distributions so that every pair is itself optimally coupled? (For 1D continuous distributions with cost being negative covariance, this is possible.)

The answer is not always.

## Counterexample

Let `V = {a,b,c}` and the distributions be

```
P: 50% a, 50% b,  0% c
Q: 50% a,  0% b, 50% c
R:  0% a, 50% b, 50% c
```

The TVD is 0.5 for every pair.

Suppose we had a three-way coupling of these distributions that is pairwise-optimal. Then it would need to have cases

```
50% (a,a,?)
50% (b,?,b)
50% (?,c,c)
```

since that’s the only way to achieve the pairwise optimality, but these are mutually-exclusive cases with total probability 150%, a contradiction.

## Implications for same-seed generation

APOC is tricky to implement. Even the simpler (but less effective) per-token coupling (PTC) method, inspired by speculative sampling, requires writing custom generation code. That presents a challenge for achieving adoption.

It’d be nicer to present a method that is easier to adopt. In practice, what’s currently used for coupling is generating with the same seed. In the field of variance reduction, this is known as Common Random Numbers (CRN). It would be nice to present a CRN-based method that performs as well as PTC or even APOC.

But the counterexample above shows that no CRN-based method can even match PTC. After all, a seed can be used for three or more generations just as easily as for two. If that seeded generation were optimal for two LLMs, then it would be pairwise-optimal for three or more LLMs, which we know is impossible.

As interesting context, as mentioned before, three (or more) 1D continuous distributions *can* be simultaneously coupled in a way that is pairwise-optimal for maximizing covariance. The specific way this works is a CRN method: generate a single number uniformly in [0,1) and use it with inverse transform sampling.

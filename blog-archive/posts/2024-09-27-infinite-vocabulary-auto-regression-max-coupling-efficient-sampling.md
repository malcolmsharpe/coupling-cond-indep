---
title: "Infinite-vocabulary auto-regression max coupling efficient sampling"
date: 2024-09-27T21:36:08+00:00
modified: 2024-09-27T21:36:08+00:00
url: https://masharpe.wordpress.com/2024/09/27/infinite-vocabulary-auto-regression-max-coupling-efficient-sampling/
tags: ["coupling", "research", "sampling"]
categories: ["Uncategorized"]
---

# Infinite-vocabulary auto-regression max coupling efficient sampling

In [my previous post](2024-09-25-efficient-sampling-when-extending-a-maximal-coupling-by-one-auto-regressive-random-variable.md), I presented an algorithm to sample from a maximal coupling of X and Y while preserving a given maximal coupling of X1 and Y1. However, that algorithm only applies when the range of X2 and Y2 is finite. What if instead the range of X2 and Y2 is infinite, either because their distributions are discrete over a countably infinite set, or because their distributions are continuous? Then we need the algorithm in this post.

We’ll see the sampling algorithm and calculate upper bounds on how many samples it draws from the given distributions. We need to be given the ability to sample from and evaluate likelihoods for the following distributions: X1,Y1; X2|X1; Y2|Y1. (Note that the ability to evaluate likelihoods is critical, which unfortunately means this algorithm can’t be used with distributions arising from diffusion models.)

**Algorithm.**

1. Sample `(a1, b1)` with probability `P[X1 = a1, Y1 = b1]`.
2. If `a1 = b1`:
   1. If `P[X1 = a1] <= P[Y1 = a1]`:
      1. Sample a2 with probability `P[X2 = a2 | X1 = a1]`.
      2. With probability `min{1, P[Y=a]/P[X=a]}`, set b2 = a2.
      3. Otherwise, sample b2 with weight `max{0, P[Y = b] - P[X = b]}`.
   2. Else (i.e. `P[Y1 = a1] < P[X1 = a1]`): similar.
3. Else (i.e. `a1 != b1`):
   1. Sample a2 with weight `max{0, P[X = a] - P[Y = a]}`.
   2. Sample b2 with weight `max{0, P[Y = b] - P[X = b]}`.
4. Return X=a and Y=b.

In four steps of this algorithm, we performed sampling of the form: sample a2 with weight `max{0, P[X=a] - P[Y=a]}`. Each of these sampling steps uses basic rejection sampling:

**Algorithm (rejection).**

1. Sample a2 with probability `P[X2=a2 | X1=a1]`.
2. With probability `min{1, P[Y=a]/P[X=a]}`, reject and go to step 1.
3. Otherwise, return X2=a2.

## Efficiency

Now, let’s analyze the efficiency of the algorithm. (We’ll leave the correctness proof for future posts.) We’ll just analyze how many samples we draw from the given conditional distributions X2|X1 and Y2|Y1. All the steps in the algorithm that do so:

- Non-residual a2 (2.1.1).
- Equal mode, residual b2 (2.1.3).
- Non-residual b2 (2.2.1).
- Equal mode, residual a2 (2.2.3).
- Split mode, residual a2 (3.1).
- Split mode, residual b2 (3.2).

Since these come in similar pairs, we only need to analyze three cases: non-residual, equal-mode residual, and split-mode residual.

### Non-residual

For non-residual a2, the expected number of samples is

```
sum_{a1 s.t. P[X1=a1] <= P[Y1=a1]} P[X1=a1]
```

Summing together with the similar formula for non-residual b2, the expected number of non-residual samplings is:

```
<= sum_{a1} min{P[X=a1], P[Y1=a1]} = 1 - TVD(X1, Y1)
```

### Rejection algorithm

For the other two cases, we’ll need to know the number of samples used by the rejection algorithm. As always with basic rejection sampling, this is is given by the reciprocal acceptance probability, and comes out to, for a2,

```
P[X1=a1] / sum_a2 max{0, P[X=a] - P[Y=a]}
```

### Equal-mode residual

Consider equal-mode residual b2, so `P[X1 = a1] <= P[Y1 = a1]`.

We first show that Y has more total residual than X:

```
sum_{a2}( max{0, P[X=a] - P[Y=a]} + min{P[X=a], P[Y=a]} )
    = sum_{a2} P[X=a]
    = P[X1=a1]
    <= P[Y1=a1]
    = sum_{a2} P[Y=a]
    = sum_{a2}( max{0, P[Y=a] - P[X=a]} + min{P[X=a], P[Y=a]} )

=> sum_{a2} max{0, P[X=a] - P[Y=a]} <= sum_{a2} max{0, P[Y=a] - P[X=a]}
```

- Probability of sampling `a1` and being in the case `a1 = b1`: `P[X1 = a1]`.
- Conditional on the previous, the probability of “set b2 = a2”:

```
sum_{a2} P[X2=a2 | X1=a1] min{1, P[Y=a]/P[X=a]}
    = P[X1=a1]^{-1} sum_{a2} min{P[X=a], P[Y=a]}
```

- Conditional on two points previous, the expected number of samples for b2:

```
(1 - P[X1=a1]^{-1} sum_{a2} min{P[X=a], P[Y=a]}) (P[Y1=a1] / sum_{a2} max{0, P[Y=a] - P[X=a]})
    = P[X1=a1]^{-1} sum_{a2} max{0, P[X=a] - P[Y=a]} (P[Y1=a1] / sum_{a2} max{0, P[Y=a] - P[X=a]})
    <= P[X1=a1}^{-1} P[Y1=a1]
```

So the (unconditional) expected number of samples is:

```
<= P[X1=a1] P[X1=a1]^{-1} P[Y1=a1]
    = P[Y1=a1]
```

By summing over the possibilites for a1, as well as summing with equal-mode residual a2, we get

```
<= sum_{a1} max{ P[X1=a1], P[Y1=a1] } = 1 + TVD(X1, Y1)
```

### Split-mode residual

Consider split-mode residual a2, so `P[X1 = a1] > P[Y1 = a1]`.

We’ll need the fact that

```
sum_{a2} max{0, P[X=a] - P[Y=a]}
    >= P[X1=a1] - P[Y1=a1]
```

So, in the whole algorithm, the expected number of samplings of a2 in the split-mode residual case is:

```
sum_{a1 s.t. P[X1=a1] > P[Y1=a1]} (P[X1=a1] - P[Y1=a1]) (P[X1=a1] / sum_{a2} max{0, P[X=a] - P[Y=a]})
    <= sum_{a1 s.t. P[X1=a1] > P[Y1=a1]} P[X1=a1]
```

So, together with b2, we get

```
<= sum_a1} max{P[X1=a1], P[Y1=a1]} = 1 + TVD(X1, Y1)
```

### Total

We got the following upper bounds:

- Non-residual: `1 - TVD(X1, Y1)`
- Equal-mode residual: `1 + TVD(X1, Y1)`
- Split-mode residual: `1 + TVD(X1, Y1)`

This totals to `3 + TVD(X1, Y1) <= 4`. (I suspect a tighter bound is possible, but in any case it is a small constant.)

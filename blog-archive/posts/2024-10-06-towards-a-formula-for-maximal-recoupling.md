---
title: "Towards a formula for maximal recoupling"
date: 2024-10-06T20:28:05+00:00
modified: 2024-10-06T20:28:05+00:00
url: https://masharpe.wordpress.com/2024/10/06/towards-a-formula-for-maximal-recoupling/
tags: ["coupling", "math", "research"]
categories: ["Uncategorized"]
---

# Towards a formula for maximal recoupling

A classic maximal coupling (CMC) can be written down with an explicit formula. Is this possible for maximal recoupling (MRC) too? This post presents an explicit formula for MRC, but it’s not very satisfactory.

CMC formula: For all a,b,

- If a=b, `Phat[X=a, Y=b] = min{ P[X=a], P[Y=b] }`.
- If a!=b, `Phat[X=a, Y=b] = (1/D) max{0, P[X=a] - P[Y=a]} max{0, P[Y=b]-P[X=b]}` where `D = TVD(X,Y)`.

MRC formula: For all a,b,

- If a=b, `Phat[X=a, Y=b] = min{ P[X=a], P[Y=b] }`.
- If a!=b,
  - If `P[X=a] <= P[Y=a]` or `P[Y=b] <= P[X=b]`, then `Phat[X=a, Y=b] = 0`.
  - Otherwise,

```
Phat[X=a, Y=b] =
    max{0, P[X=a] - P[Y=a]}
    max{0, P[Y=b] - P[X=b]}
    sum_{l >= 1} sum_v (
        prod_{i=0}^{l-1} P[X=v_i, Y=v_{i+1}]
        prod_{i=0}^l (max{P[X=v_i], P[Y=v_i])^{-1}
    )
```

where v is such that `v_0 = a`, `v_l = b`, and for all `1 <= i <= l-1`, `P[X = v_i] > 0` or `P[Y = v_i] > 0`.

The reason this is not quite satisfactory is that it’s summing over all trajectories of the MRC sampling algorithm. The formula for CMC doesn’t sum over the trajectories of the CMC sampling algorithm, so it’s simpler.

As mentioned in previous posts, when the MRC sampling algorithm is applied to the trivial coupling in which X and Y are independent, it reduces to the CMC sampling algorithm. We can observe that with this formula too. After substituting `P[X=v_i, Y=v_{i+1}] = P[X=v_i] P[Y=v_{i=1}]` and doing some algebra, the sum becomes

```
sum_{l >= 1} sum_v prod_{i=1}^{l-1} min{P[X=v_i], P[Y=v_i]}
    = sum_{l >= 1} prod_{i=1}^{l-1} sum_{v_i} min{P[X=v_i], P[Y=v_i]}
    = sum_{l >= 1} (sum_c min{P[X=c], P[Y=c]})^{l-1}
    = sum_{n=0}^{inf} (1 - D)^n
    = 1/D
```

so the formula as a whole matches the CMC formula we wrote down originally.

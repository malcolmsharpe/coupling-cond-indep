---
title: "Closed-form formula for maximal recoupling"
date: 2024-10-07T19:24:37+00:00
modified: 2024-10-14T21:56:53+00:00
url: https://masharpe.wordpress.com/2024/10/07/closed-form-formula-for-maximal-recoupling/
tags: ["coupling", "math", "research"]
categories: ["Uncategorized"]
---

# Closed-form formula for maximal recoupling

**Corrections (2024-10-14):**

- The assumption “assume reducibility” should have read “assume irreducibility”.
- The denominator of `A_{vw}` was previously incorrectly `sqrt(max{P[X=v], P[Y=w]})`. Now, `Pmax` has been introduced and the denominator changed to `sqrt(Pmax(v) Pmax(w))`.
- In the final formula, the exponent of `(P[X=a] P[Y=b])^{1/2}` has the wrong sign. It is now changed to `(P[X=a] P[Y=b])^{-1/2}`.

---

In [my previous post, I expressed a desire for a formula for maximal recoupling](2024-10-06-towards-a-formula-for-maximal-recoupling.md). Although I gave one there, it involved an infinite sum. It turns out that it’s quite easy to re-express in closed form using matrices.

For now, we need to assume irreducibility.

For convenience, for all v, let `Pmax(v) = max{P[X=v], P[Y=v]}`.

Define a matrix A by, for all v and w such that `Pmax(v) > 0` and `Pmax(w) > 0`,

```
A_{vw} = P[X=v, Y=w] / sqrt(Pmax(v) Pmax(w))
```

and other entries are zero.

Then we can simplify the sum from the previous post. Note that `a != b`, so `I_{ab} = 0`.

```
sum_{l >= 1} sum_v (
    prod_{i=0}^{l-1} P[X=v_i, Y=v_{i+1}]
    prod_{i=0}^l (max{P[X=v_i], P[Y=v_i])^{-1}
)
    = (P[X=a] P[Y=b])^{-1/2}
        sum_{l >= 1} sum_v prod_{i=0}^{l-1} A_{v_i v_{i+1}}
    = (P[X=a] P[Y=b])^{-1/2}
        sum_{l >= 1} (A^l)_{ab}
    = (P[X=a] P[Y=b])^{-1/2}
        sum_{l >= 0} (A^l)_{ab}
    = (P[X=a] P[Y=b])^{-1/2} ((I - A)^{-1})_{ab}
```

Bringing it all together, we derived: For all a,b,

- If a=b, `Phat[X=a, Y=b] = min{ P[X=a], P[Y=b] }`.
- If a!=b,
  - If `P[X=a] <= P[Y=a]` or `P[Y=b] <= P[X=b]`, then `Phat[X=a, Y=b] = 0`.
  - Otherwise,

```
Phat[X=a, Y=b] =
    max{0, P[X=a] - P[Y=a]}
    max{0, P[Y=b] - P[X=b]}
    (P[X=a] P[Y=b])^{-1/2}
    ((I - A)^{-1})_{ab}
```

where A was defined above.

There is an important (but non-impactful) TODO to resolve here regarding reducibility: `I + A + A^2 + ...` isn’t always convergent. The problem is caused when the underlying Markov chain is reducible and there’s a component with no source (and, because the graph is balanced, no sink either). This doesn’t create an actual problem, since, when indexing the matrix, every a is a source and every b is a sink, but for a rigorous treatment, it requires careful handling.

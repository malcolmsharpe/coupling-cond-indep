---
title: "More straightforward derivation for previous post"
date: 2024-05-15T16:43:17+00:00
modified: 2024-05-15T16:43:17+00:00
url: https://masharpe.wordpress.com/2024/05/15/more-straightforward-derivation-for-previous-post/
tags: ["entropy", "math", "probability"]
categories: ["Uncategorized"]
---

# More straightforward derivation for previous post

The formulas in my [previous post](2024-05-14-relative-surprisal-in-the-equal-distribution-limit.md) can be more straightforwardly derived using gradient, Hessian, and multivariate Taylor’s theorem. (I blame rustiness for not doing it this way in the first place.) Fixing p and letting q vary, here are the relevant equations:

```
F(q) := sum_i p_i (ln p_i - ln q_i)
grad F(q) = (-p_i/q_i)_i
grad F(p) = (-1)_i
grad^2 F(q) = Diag[ (p_i/q_i^2)_i ]
grad^2 F(p) = Diag[ (1/p_i)_i ]

G(q) := sum_i p_i (ln p_i - ln q_i)^2
grad G(q) = (-2 p_i/q_i (ln p_i - ln q_i))_i
grad G(p) = 0
grad^2 G(q) = Diag[ (2 p_i/q_i^2 (ln p_i - ln q_i + 1))_i ]
grad^2 G(p) = Diag[ (2/p_i)_i ]
```

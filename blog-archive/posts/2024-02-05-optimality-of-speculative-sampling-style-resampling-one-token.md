---
title: "Optimality of speculative-sampling-style resampling (one token)"
date: 2024-02-05T00:03:13+00:00
modified: 2024-02-05T00:03:13+00:00
url: https://masharpe.wordpress.com/2024/02/05/optimality-of-speculative-sampling-style-resampling-one-token/
tags: ["llm", "math", "sampling"]
categories: ["Uncategorized"]
---

# Optimality of speculative-sampling-style resampling (one token)

For two token probability distributions `p` and `q`, speculative sampling resamples with probability `(1/2) ||p - q||_1`. So, for `X ~ p` and `Y ~ q`, `P[X != Y] = (1/2) ||p - q||_1`. In this post, I sketch the proof that this is the minimum possible.

Observe the bound  
  `P[X = Y] = sum_x P[X = x /\ Y = x] <= sum_x min { p(x), q(x) }`.  
So  
  `P[X != Y] >= 1 - sum_x min { p(x), q(x) }`.  
Then some algebra, using the fact `(1/2)(a + b) - min{a, b} = (1/2)|a - b|`, proves the result.

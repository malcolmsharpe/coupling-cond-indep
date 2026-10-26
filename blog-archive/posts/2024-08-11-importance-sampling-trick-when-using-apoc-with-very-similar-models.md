---
title: "Importance-sampling trick when using APOC with very similar models"
date: 2024-08-11T16:50:15+00:00
modified: 2024-08-11T16:52:55+00:00
url: https://masharpe.wordpress.com/2024/08/11/importance-sampling-trick-when-using-apoc-with-very-similar-models/
tags: ["coupling", "llm", "research"]
categories: ["Uncategorized"]
---

# Importance-sampling trick when using APOC with very similar models

Suppose you want to estimate an anti-symmetric score (meaning `f(x,y) = -f(y,x)`, such as difference of reward) of two very similar models. Using APOC to reduce the variance is a good choice, and one effect will be that many response pairs are equal. By symmetry, equal pairs receive score 0.

If the score is expensive to compute, such as needing human labeling, then we can simply omit the equal pairs, since we don’t need a human to tell us that they are tied.

On the other hand, if the score is inexpensive to compute, such as whether the solution to an arithmetic problem is correct, then we’re wasting inference budget by generating so many equal pairs. In that case, we can use an importance-sampling-inspired trick.

The trick uses APOC conditional sampling. First we sample a response from model X. Then we calculate the probability that model Y would emit the same response, and apply that weight to score 0. Next, we take the branch where the responses are non-equal, with the resulting score correspondingly downweighted.

---
title: "Addendum to previous post"
date: 2024-09-26T19:18:01+00:00
modified: 2024-09-26T19:18:01+00:00
url: https://masharpe.wordpress.com/2024/09/26/addendum-to-previous-post/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Addendum to previous post

In the previous post, I neglected to use the assumption that X1 and Y1 are maximally coupled! This assumption is indeed necessary, because we must ensure that, during the sampling algorithm, whenever we sample using weights (i.e. unnormalized probabilities), the sum of weights is positive.

In step 2:

- `P[X1 = Y1 = a1]` is nonzero due to having sampled it in step 1.
- The sum of the weights is the numerator of the first probability, so we only enter that part if the weight sum is nonzero.

In step 3, the two halves are similar, so we’ll just address sampling a2. Because X1 and Y1 are maximally coupled and we sampled a1 for X1 and did not sample a1 for Y1, we know `P[X1=a1] > P[Y1=a1]`. Then the weight sum is:

```
sum_{a2} max{0, P[X=a] - P[Y=a]}
    >= sum_{a2} (P[X=a] - P[Y=a])
    = P[X1=a1] - P[Y1=a1]
    > 0
```

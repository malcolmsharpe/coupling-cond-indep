---
title: "Coupling can’t maximize both covariance and equality probability"
date: 2024-08-11T17:16:47+00:00
modified: 2024-08-11T17:16:47+00:00
url: https://masharpe.wordpress.com/2024/08/11/coupling-cant-maximize-both-covariance-and-equality-probability/
tags: ["coupling", "example", "probability"]
categories: ["Uncategorized"]
---

# Coupling can’t maximize both covariance and equality probability

Suppose we want to use APOC with more than two models, such as a full-precision model, an nf8 quant, and an nf4 quant. One approach is to generate from the full-precision model first, then use APOC conditional generation for each of the quants. It’s possible then to couple those conditional generations further. The first decision in a conditional generation is the choice of split point, and there are two ways we might imagine coupling the split point:

- We might try to make the two responses have the same split point, since that allows coupling the suffixes too.
- We might try to make the two responses have nearby split points, which reduces the variance of the difference of longest common prefix length.

But we can’t achieve both these goals simultaneously, in general.

Abstractly, we’re coupling two real-valued random variables. We may choose the coupling to maximize probability of equality (the first option) or to maximize covariance (the second option). Here’s a simple example showing that these two options can yield different couplings.

Let

```
X ~
    -1 wp 50%
    0 wp 50%
Y ~
    0 wp 50%
    +1 wp 50%
```

When coupling to maximize equality probability:

```
X,Y ~
    0,0 wp 50%
    -1,+1 wp 50%

P[X = Y] = 50%
E[XY] = -0.5
```

When coupling to maximize covariance:

```
X,Y ~
    -1,0 wp 50%
    0,+1 wp 50%

P[X = Y] = 0%
E[XY] = 0
```

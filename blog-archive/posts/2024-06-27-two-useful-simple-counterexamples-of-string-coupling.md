---
title: "Two useful simple counterexamples of string coupling"
date: 2024-06-27T17:54:15+00:00
modified: 2024-06-27T17:54:15+00:00
url: https://masharpe.wordpress.com/2024/06/27/two-useful-simple-counterexamples-of-string-coupling/
tags: ["coupling", "research"]
categories: ["Uncategorized"]
---

# Two useful simple counterexamples of string coupling

## Biased coinflips

This example shows PTOC < APOC even if the tokens are independent.

Let the alphabet be `{H,T}`, let the response length be `n=2`, and, for every i, let

```
P[X_i = H] = 3/4
P[Y_i = H] = 1/4
```

Let `X_1` and `X_2` be independent, and let `Y_1` and `Y_2` be independent too.

The whole-response distributions are

```
a    P[X=a]  P[Y=a]  min{P[X=a], P[Y=a]}
HH   9/16    1/16    1/16
HT   3/16    3/16    3/16
TH   3/16    3/16    3/16
TT   1/16    9/16    1/16
```

With PTOC, each token is optimally coupled to get `P[X_i = Y_i] = 1/2`, so `P[X = Y] = (1/2)^2 = 1/4`.

With APOC, however, `P[X = Y] = 1/16 + 3/16 + 3/16 + 1/16 = 1/2`. Interestingly, for this example, APOC happens to optimally couple the `i=1` token as well, which is not true in general, since APOC only optimizes prefixes.

## Impossibility of simultaneously optimally coupling every position

Let

```
X ~ Unif({aa, bb})
Y ~ Unif({ab, ba})
```

Position 0 can be optimally coupled with equality probability 1, and so can position 1, but this can’t be done simultaneously. Indeed,

```
P[X_1 = Y_1] = 1 - P[X_2 = Y_2]
```

## Open question

The second example relied on non-independence of the tokens. If the tokens are independent, it is always possible to simultaneously couple every position using PTOC, but this may not optimally couple the whole response, as seen in the first example.

The open question: if the tokens are independent, is it always possible to simultaneously couple *both* the whole response *and* every token position?

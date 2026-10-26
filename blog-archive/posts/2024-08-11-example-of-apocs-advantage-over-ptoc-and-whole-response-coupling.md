---
title: "Example of APOC’s advantage over PTOC and whole-response coupling"
date: 2024-08-11T19:52:31+00:00
modified: 2024-08-11T19:52:31+00:00
url: https://masharpe.wordpress.com/2024/08/11/example-of-apocs-advantage-over-ptoc-and-whole-response-coupling/
tags: ["coupling", "example", "research"]
categories: ["Uncategorized"]
---

# Example of APOC’s advantage over PTOC and whole-response coupling

The key idea of APOC is that all-prefix-optimal coupling is possible. More specifically, that means the first token and the whole response can be simultaneously optimally coupled. The example in this post shows that weaker coupling methods don’t necessarily achieve this.

Here’s an example where PTOC (which always optimally couples the first token) does not optimally couple the whole response, and optimal whole-response coupling does not necessarily optimally couple the first token.

```
X ~
    AA wp 1/5
    AB wp 2/5
    BB wp 2/5
Y ~
    AA wp 2/5
    BA wp 2/5
    BB wp 1/5
```

The first token distribution is

```
X_0 ~
    A wp 3/5
    B wp 2/5
Y_0 ~
    A wp 2/5
    B wp 3/5
```

- The first token optimal equality probability: 2/5 + 2/5 = 4/5.
- The whole-response optimal equality probability: 1/5 + 1/5 = 2/5.
- The whole-response equality probability achieved by PTOC: (2/5)(1/3) + (2/5)(1/3) = 4/15.

That shows that PTOC doesn’t optimally couple the whole response. To see that optimal whole-response coupling doesn’t necessarily optimally couple the first token, first observe the residual probabilities:

```
X residual:
    AB wp 2/5
    BB wp 1/5
Y residual:
    AA wp 1/5
    BA wp 2/5
```

For example, if these are sampled independently, then the first token won’t be optimally coupled.

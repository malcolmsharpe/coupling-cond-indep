---
title: "Crossing families of random variables can’t be simultaneously optimally coupled"
date: 2024-09-16T20:20:16+00:00
modified: 2024-09-16T20:20:16+00:00
url: https://masharpe.wordpress.com/2024/09/16/crossing-families-of-random-variables-cant-be-simultaneously-optimally-coupled/
tags: ["coupling", "example", "research"]
categories: ["Uncategorized"]
---

# Crossing families of random variables can’t be simultaneously optimally coupled

Consider random variables X1, X2, X3 independent and Y1, Y2, Y3 independent, where, for each i, Xi and Yi are members of the same set. The all-prefix-optimal coupling (APOC) construction shows that we may simultaneously optimally couple any auto-regressive family, such as `{{1}, {1,2}, {1,2,3}}`. The [non-crossing-family-optimal coupling (NCFOC) conjecture](2024-07-11-conjecture-non-crossing-family-optimal-coupling.md) says further that we may simultaneously optimally couple any non-crossing family, such as `{{1}, {2}, {3}, {1,2}, {1,2,3}}`. NCFOC is stronger than APOC, since auto-regressive families are non-crossing (though note that [the independence assumption is necessary](2024-06-27-two-useful-simple-counterexamples-of-string-coupling.md)).

But can we generalize further? Is the non-crossing assumption necessary? The computer search supporting the NCFOC conjecture found many crossing counterexamples, but they aren’t easy to understand.

In this post, we’ll see a simple example of a crossing family that cannot be simultaneously optimally coupled, thus establishing the tightness of the NCFOC conjecture.

## Example

Let

```
X1: 100% b
Y1: 50% a, 50% b

X2: 50% a, 50% b
Y2: 100% b

X3: 50% a, 50% b
Y3: 100% b
```

The (crossing) family F of sets is `{{1,2}, {1,3}}`.

Suppose that there is a simultaneous optimal coupling of F.

Consider first the set `{1,2}`. The unique optimal coupling of this set is

```
50%:
    X12 = ba
    Y12 = ab
50%:
    X12 = bb
    Y12 = bb
```

Thus, `X1=Y1=b <-> X2=b`.

Similarly, by considering `{1,3}`, we get `X1=Y1=b <-> X3=b`.

But then we can combine the two equivalences to conclude `X2=b <-> X3=b`, so `P[X23 = bb] = 0.5`. But by independence, `P[X23 = bb] = 0.25`, a contradiction.

## Discussion

In sampling from SEDD, there are several steps, and within each step there are several independent decisions. Though we can put those decisions in some arbitrary order to use APOC, it would have been nice if we could exploit the independence. The counterexample above shows that the independence can only be exploited in the first step, not subsequent steps.

---
title: "Details of maximal recoupling’s effect on subcouplings"
date: 2024-10-02T20:28:30+00:00
modified: 2024-10-02T20:28:30+00:00
url: https://masharpe.wordpress.com/2024/10/02/details-of-maximal-recouplings-effect-on-subcouplings/
tags: ["conjecture", "coupling", "example", "research"]
categories: ["Uncategorized"]
---

# Details of maximal recoupling’s effect on subcouplings

In [my previous post](2024-10-01-key-subroutine-for-simultaneously-maximal-coupling.md), I presented the maximal recoupling (MRC) algorithm, a (to my taste) delightfully elegant algorithm for modifying a coupling to become maximal while preserving any pre-existing maximal subcouplings. What makes MRC special, compared to standard maximal coupling, is the final pair of properties I conjectured in that post: the equality probability of every subcoupling improves; and maximal subcouplings are preserved without any change.

It’s then natural to ask whether, if a subcoupling was nearly maximal to begin with, it might change at most a little. To that end, I’ve unified the conjectured properties into a single one.

## Conjecture

Take a finite set E and random variables X and Y taking values in E. Then the MRC algorithm samples from a maximal coupling Phat of X and Y such that, for every partition of E into equivalence classes `[-]`, we have

```
TVD( ([X],[Y])_P, ([X],[Y])_Phat )
    <= 2 (Phat[[X] = [Y]] - P[[X] = [Y]])
```

In words, the change in distribution (as measured by total variation distance) is upper-bounded by twice the improvement of equality probability.

The two originally conjectured properties are recovered as follows:

- Since TVD is non-negative, the equality probability cannot decrease.
- If the equality probability was already maximum, then TVD must be zero.

## Proof idea

Imagine representing the original joint by a weighted directed graph G with node-set E and arc-set A. MRC decomposes G into a sum of paths and cycles.

- A cycle is replaced by self-loops. This increases TVD by `length * weight` and improves the equality probability by `length * weight`.
- A path is replaced by self-loops on the inner nodes and a shortcut arc from the start to the end. This increases TVD by at most `length * weight` and improves the equality probability by `(length - 1) * weight`.

So, the worst case is a length-2 path, where TVD increases by as much as `2 * weight` and the equality probability increases by only `weight`.

(Here’s a brief note on why we know the exact TVD increase for a cycle but for a path it’s merely upper-bounded. MRC only adds self-loops, never deletes them, so adding a self-loop always adds to TVD. But the path case adds an arc, and that same arc might have been deleted elsewhere, which cancels out, reducing the TVD.)

## Assorted facts

In the other direction, it’s immediate from the definition of TVD that

```
Phat[[X] = [Y]] - P[[X] = [Y]]
    <= TVD( ([X],[Y])_P, ([X],[Y])_Phat )
```

Now here are some facts that we’ll show with examples:

- Both bounds can hold with equality.
- Without MRC, the TVD can be 1 even if the equality probability doesn’t change.

### Example: delta_eq = TVD

X: uniform over a,b.  
Y: uniform over a,b.

Original coupling: uniform over (a,b), (b,a).

The unique maximal coupling: uniform over (a,a), (b,b).

The TVD from the original is 1, and delta_eq = 1.

### Example: TVD = 2 \* delta_eq

X: uniform over a,c.  
Y: uniform over a,b.

Original coupling: uniform over (a,b), (c,a).

Unique maximal coupling: uniform over (a,a), (c,b).

The TVD is 1, and delta_eq is 1/2.

(Since the maximal coupling is unique, it’s the only one that MRC can produce.)

### Example without MRC: TVD = 1, delta_eq = 0

X: constant a.  
Y: uniform over b,c.

Joint 1: uniform over (a,b), (a,c).  
Joint 2: uniform over (a,c), (a,b).

TVD is 1, and the equality probability is 0 in both cases, so delta_eq is 0.

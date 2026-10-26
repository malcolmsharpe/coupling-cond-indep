---
title: "Progress towards NCFOC sampling: loss-halving algorithm"
date: 2024-09-29T20:00:53+00:00
modified: 2024-09-29T20:00:53+00:00
url: https://masharpe.wordpress.com/2024/09/29/progress-towards-ncfoc-sampling-loss-halving-algorithm/
tags: ["algorithm", "coupling", "research", "sampling"]
categories: ["Uncategorized"]
---

# Progress towards NCFOC sampling: loss-halving algorithm

In [my previous post](2024-09-28-progress-towards-ncfoc-sampling.md), I discussed progress towards efficient sampling for NCFOC. Although that remains difficult, in this post I present further progress.

This post presents an algorithm that, if repeatedly applied, perhaps yields a proof of the [general simultaneously maximal coupling lemma](2024-09-23-general-lemma-for-simultaneously-maximal-coupling.md) that works for infinite vocabularies. (I say “perhaps” because there are critical details to work out regarding convergence.)

The algorithm is built around the same exchange idea as that lemma. We’ll define a loss that quantifies how far a coupling is from maximal and construct the algorithm so that it halves this loss while preserving the losses of subcouplings and the marginal distributions of maximal subcouplings. (Note that the lemma before *also* preserves the losses of subcouplings, though we didn’t observe so in its post. The reason to note it now is that it may be useful for recursion.)

## Preliminaries

Define the loss of a coupling to be

```
l_P(X,Y)
    = sum_a ( min{P[X=a], P[Y=a]} - P[X=a, Y=a] )
    = sum_a min{ P[X=a, Y!=a], P[X!=a, Y=a] }
```

Maximal couplings are exactly the zero-loss couplings.

Consider the exchange move

```
  1 2        1 2
X a c  =>  X a c
Y b a      Y a b
```

| Case | Initial mismatches | Final mismatches | Net |
| --- | --- | --- | --- |
| b!=a, c!=a | X=a,X=c,Y=b,Y=a | X=c,Y=b | -1(X=a), -1(Y=a) |
| b=a,c!=a | X=c,Y=a | X=c,Y=a | nop |
| b!=a,c=a | (similar) | (similar) | (similar) |
| b=a,c=a | none | none | nop |

No case increases the subcoupling loss. Observe that the first case reduces the subcoupling’s loss, so a maximal subcoupling can never experience that case. The other three cases do not change the distribution.

## Lemma and algorithm

**Lemma.** Take RVs X=(X1,…,Xn) and Y=(Y1,…,Yn) ranging over the same set Sigma^n (possibly infinite). Then Algorithm induces a coupling Phat of X and Y such that:

- The coupling loss is halved: `l_Phat(X,Y) <= (1/2) l_P(X,Y)`.
- Subcoupling loss does not increase: for every S subset of [n], `l_Phat(X_S, Y_S) <= l_P(X_S, Y_S)`.
- Maximal subcouplings are preserved: for every S subset of [n], if P maximally coupled X_S and Y_S, then `Phat[X_S = a, Y_S = b] = P[X_S = a, Y_S = b]` for all a,b in Sigma^n.

**Algorithm sketch.**

1. Couple (X,Y) with itself to get Ptilde of RVs (X^1, Y^1) and (X^2, Y^2) that maximizes `sum_a Ptilde[X^1=a, Y^1!=a, X^2!=a, Y^2=a]`. (Note that this maximum value is `l_P(X,Y)`.)
2. Sample from Ptilde. If not in exchange form, return one of the two values uniformly at random.
3. Otherwise, the sample has the form

```
  1 2
X a c
Y b a
```

where b!=a and c!=a.

4. Return
   - X=a,Y=a wp 1/2
   - X=c,Y=b wp 1/2

## Proof idea

That the algorithm has the desired effect on losses and maximal subcouplings is obvious enough from our case analysis of the exchange move.

So what remains is to check that Ptilde is a valid coupling of X and Y. This is obvious too, since the exchange doesn’t change that it’s a coinflip which side’s sample we pick, and both those samples are valid.

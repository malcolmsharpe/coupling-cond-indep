---
title: "Full pseudocode for sampling from a simultaneous maximal coupling of Bayesian networks"
date: 2024-10-08T19:46:28+00:00
modified: 2024-10-08T19:46:28+00:00
url: https://masharpe.wordpress.com/2024/10/08/full-pseudocode-for-sampling-from-a-simultaneous-maximal-coupling-of-bayesian-networks/
tags: ["algorithm", "coupling", "pseudocode", "research", "sampling"]
categories: ["Uncategorized"]
---

# Full pseudocode for sampling from a simultaneous maximal coupling of Bayesian networks

Given two Bayesian networks X and Y with respect to the same graph G and taking values in the same finite set E, certain families F of vertex sets may be simultaneously maximally coupled. The fully general characterization is that F is laminar and its disjoint sets are d-separated by the empty set. For computational purposes, though, it is more convenient to restrict to laminar F whose sets are ancestral–this is without loss of generality, since any G matching the general condition can be replaced by a G’ matching the specific condition. We may also assume that F is maximal, i.e. no additional sets can be added to F.

How do we sample from such a coupling? In recent posts, I’ve discussed the key subroutine, the [maximal recoupling (MRC) algorithm](2024-10-01-key-subroutine-for-simultaneously-maximal-coupling.md). Although MRC is the non-trivial idea, it’s nevertheless necessary to state and analyze the entire SMCBN algorithm as a whole. Having the entire algorithm is particularly important for efficiency analysis.

This post shows a first draft of the full pseudocode from SMCBN. The input is given as a tree representing a factorization via auto-regressive steps (i.e. the chain rule of probability) and independent combinations (i.e. tensor product). The first pass constructs an object graph of joint distributions. Then sampling occurs recursively.

```
# A factorization, structured as a tree.
adt Tree E =
    # One node in G.
    | Leaf (Marginal E) (Marginal E)
    # A multiplication of two factorizations.
    | Split (Tree E1) (Tree E2)  where E = E1 x E2
    # A factorization extended with another node via the chain rule.
    | Step (Tree E1) (ConditionalMarginal E1 E2) (ConditionalMarginal E1 E2)  where E = E1 x E2

# A distribution of one random variable.
rec Marginal E =
    # Given x, calculate P[X = x]
    L : E -> [0,1]
    # Sample x wp P[X = x]
    samp : () -> E

# A conditional distribution of one random variable.
rec ConditionalMarginal Ec E =
    # Given x1 x2, calculate P[X2 = x2 | X1 = x1]
    L : Ec -> E -> [0,1]
    # Given x1, sample x2 wp P[X2 = x2 | X1 = x1]
    samp : Ec -> E

# A joint distribution of two random variables.
rec Joint E =
    # Given x, calculate P[X = x]
    LX : E -> [0,1]
    # Given y, calculate P[Y = y]
    LY : E -> [0,1]
    # Sample x wp P[X = x]
    sampX : () -> E
    # Given x, sample y wp P[Y = y | X = x]
    sampY|X : E -> E

# Sample from a simultaneous maximal coupling of a given factorization.
Sample : Tree E -> (E,E)

Sample(t)
    1. j <- BuildJoint(t)
    2. x <- j.sampX()
    3. y <- j.sampY|X(x)
    4. Return (x,y)

# Simultaneously maximally couple a given factorization.
BuildJoint : Tree E -> Joint E

BuildJoint(Leaf mX mY) =
    LX(x) = mX.L(x)
    LY(y) = mY.L(y)
    sampX()
        1. Return mX.samp()
    sampY|X(x)
        # Classic maximal coupling
        1. With prob min{1, mY.L(x)/mX.L(x)}, return x.
        2. Repeat:
            1. y <- mY.samp()
            2. With prob min{1, mX.L(y)/mY.L(y)}, continue.
            3. Otherwise, return y.

BuildJoint(Split t1 t2)
    1. j1 <- BuildJoint(t1)
    2. j2 <- BuildJoint(t2)
    3. j <- TensorProduct(j1, j2)
    4. Return MaximalRecoupling(j)

BuildJoint(t, cmX, cmY)
    1. j <- BuildJoint(t)
    2. j' <- ChainRule(j, cmX, cmY)
    3. Return MaximalRecoupling(j')

# Independently combine two joint distributions.
TensorProduct : Joint E1 -> Joint E2 -> Joint (E1 x E2)

TensorProduct(j1, j2) =
    LX((x1, x2)) = j1.LX(x1) * j2.LX(x2)
    LY((y1, y2)) = j1.LY(y1) * j2.LY(y2)
    sampX()
        1. x1 <- j1.sampX()
        2. x2 <- j2.sampY()
        3. Return (x1, x2)
    sampY|X((x1, x2))
        1. y1 <- j1.sampY|X(x1)
        2. y2 <- j2.sampY|X(x2)
        3. Return (y1, y2)

# Maximally recouple a joint distribution.
MaximalRecoupling : Joint E -> Joint E

MaximalRecoupling(j) =
    LX(x) = j.LX(x)
    LY(y) = j.LY(y)
    sampX()
        1. Return j.sampX()
    sampY|X(x)
        1. With prob min{1, j.LY(x)/j.LX(x)}, return x.
        2. Repeat:
            1. y <- j.sampY|X(x)
            2. With prob min{1, j.LX(y)/j.LY(y)}:
                1. x <- y
                2. Continue.
            3. Otherwise, return y.

# Extend a joint distribution with the given conditional marginal distributions for X2|X1 and Y2|Y1.
ChainRule : Joint E1 -> ConditionalMarginal E2 -> ConditionalMarginal E2 -> Joint (E1 x E2)

ChainRule(j, cmX, cmY) =
    LX((x1, x2)) = j.LX(x1) * cmX.L(x1, x2)
    LY((y1, y2)) = j.LY(y1) * cmY.L(y1, y2)
    sampX()
        1. x1 <- j.sampX()
        2. x2 <- cmX.samp(x1)
        3. Return (x1, x2)
    sampY|X((x1,_))
        1. y1 <- j.sampY|X(x1)
        2. y2 <- cmY.samp(y1)
        3. Return (y1, y2)
```

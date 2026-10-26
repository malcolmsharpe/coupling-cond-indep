---
title: "Conjecture: the broadest generalization of APOC and NCFOC"
date: 2024-09-19T00:30:14+00:00
modified: 2024-09-19T00:30:14+00:00
url: https://masharpe.wordpress.com/2024/09/19/conjecture-the-broadest-generalization-of-apoc-and-ncfoc/
tags: ["conjecture", "coupling", "research"]
categories: ["Uncategorized"]
---

# Conjecture: the broadest generalization of APOC and NCFOC

Two methods for maximal coupling of a family of sets of nodes in a Bayesian network:

- All-prefix-optimal coupling: Applicable when the Bayesian network is complete. i.e. The BN represents an auto-regressive factorization. Every ancestral set is simultaneously maximally coupled, where “ancestral set” means a set that is closed under taking ancestors.
- Non-crossing-family-optimal coupling: Applicable when the Bayesian network is empty. i.e. The BN represents independence. Given a non-crossing family of sets, every set in the family is simultaneously maximally coupled.

I know a construction for APOC, but I don’t know a construction or even an existence proof for NCFOC, so it remains a conjecture.

If the NCFOC conjecture does turn out to be true, it naturally raises the question whether there is a generalization of APOC and NCFOC to general Bayesian networks. I now have a solid guess as to what that generalization might be, and this post presents the conjecture.

## Conjecture

Conjecture: Let X_1, …, X_N and Y_1, …, Y_N be random variables, each having the same Bayesian network structure. Let F be a family of sets of nodes that is non-crossing (i.e. for any two intersecting sets in F, one contains the other) and ancestral (i.e. every set in F contains the ancestors of each of its elements). Then there is a coupling of X and Y that is simultaneously maximal for every set in F. i.e. For every S in F and value a, `P[X_S = Y_S = a] = min{ P[X_S = a], P[Y_S = a] }`.

To see that this conjecture generalizes APOC and NCFOC, notice that, in the auto-regressive case, a family of ancestral sets is automatically non-crossing, and in the independent case, every family of sets is automatically ancestral.

## Proof strategy

My guess as to how to prove the conjecture is induction using three lemmas: one classic, one an variant of APOC, and one new for NCFOC.

Lemma 1 (classical maximal coupling). If X and Y are random variables, there exists a coupling such that, for every value a, `P[X = Y = a] = min{ P[X = a], P[Y = a] }`.

Lemma 2 (auto-regressive step). Let X_1, X_2, Y_1, Y_2 be random variables such that X_1 and Y_1 are maximally coupled. Then there exists a maximal coupling of X and Y that preserves the marginal distribution of (X_1, Y_1).

(Note: Preserving the marginal distribution of (X_1, Y_1) is critical to make the induction work. It wouldn’t be good enough to just ensure that X_1 and Y_1 remain maximally coupled.)

Lemma 3 (independent cross). Let X_1, X_2, Y_1, Y_2 be random variables such that X_1 and X_2 are independent, Y_1 and Y_2 are independent, X_1 and Y_1 are maximally coupled, and Y_1 and Y_2 are maximally coupled. Then there exists a maximal coupling of X and Y that preserves the marginal distributions of (X_1, Y_1) and (X_2, Y_2).

(Note: Again, preserving the marginal distributions is necessary for the induction.)

Lemma 1 is well-known to be true. Lemma 2 is a simple variant of APOC, so it would be quite surprising were it not true. Lemma 3 is as yet unproven.

Given these three lemmas, it’s intuitively clear how to prove the conjecture using induction.

## Evidence

Evidence for the conjecture’s truth:

- [APOC has a construction](2024-07-04-apoc-unconditional-sampling-conceptual-pseudocode.md).
- [NCFOC has been computationally tested in small random cases](2024-07-11-conjecture-non-crossing-family-optimal-coupling.md).

Evidence for the conjecture’s tightness:

- [A simple counterexample with a crossing family](2024-09-16-crossing-families-of-random-variables-cant-be-simultaneously-optimally-coupled.md).
- [A simple counterexample with a non-ancestral set](2024-06-27-two-useful-simple-counterexamples-of-string-coupling.md).

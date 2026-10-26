---
title: "Dominance hierarchy of string coupling methods"
date: 2024-06-14T17:18:25+00:00
modified: 2024-06-14T17:18:25+00:00
url: https://masharpe.wordpress.com/2024/06/14/dominance-hierarchy-of-string-coupling-methods/
tags: ["coupling", "probability", "research", "string", "theory"]
categories: ["Uncategorized"]
---

# Dominance hierarchy of string coupling methods

Suppose we have two discrete distributions over the same finite set of strings, with corresponding random variables X and Y. For example, X and Y might be responses from two different quantizations of an LLM.

We’d like to couple X and Y to maximize similarity. Precisely, we want methods that define a joint distribution `P[X=a /\ Y=b]` that for every length-i prefix `a_{<i}` maximizes the probability that X and Y share that prefix: `P[X_{<i} = Y_{<i} = a_{<i}]`. A method is said to dominate another if for every choice of distributions and prefix `a_{<i}`, the share-probability is no less. The dominance is strict if there exists a choice of distributions and prefix such that the share-probability inequality is strict.

Here are the methods that we’ll compare in this post:

- PTCRN: Per-token common-random-numbers, a family of methods. This includes ad hoc seed reuse.
- PTOC: Per-token optimal coupling.
- APOC: All-prefix-optimal coupling.

I’ve described these methods in previous posts, so here we’ll just compare them. This post collects the facts needed to show PTCRN < PTOC < APOC. i.e. APOC strictly dominates PTOC, which in turn strictly dominates every PTCRN method.

## Why study prefix share-probability?

Domination with respect to prefix share-probability implies:

- Domination with respect to whole-response equality probability `P[X = Y]`.
- Domination with respect to longest-common-prefix survival-function `LCP-SF(k) = P[LCP(X,Y) > k]`, where LCP is the length of the longest common prefix.

In both cases, the reason is that the probability of interest can be expressed as a sum of the share-probabilities of a prefix-free set of prefixes.

But this still leaves a question of why care about prefixes specifically. There are many practically-relevant string similarity metrics you could imagine using, such as edit distance, that can’t be expressed using only prefix share-probability. Reasons:

- The response coupling method in typical use today, ad hoc seed reuse, will typically not have useful effects other than promoting a long common prefix. (Though, in principle, it could, for example if the response is structured in a way that the token positions align even after the responses differ.) So, methods that dominate ad hoc seed reuse with respect to prefix share-probability are typically going to be better than it in every way.
- It’s not clear how to directly approach the problem of coupling responses to maximize a complicated metric such as edit distance. One way would be to use prefix-oriented methods as subroutines.

Now let’s establish the dominance hierarchy.

## PTCRN <= PTOC

See [this proof](2024-06-06-note-crn-ptc.md).

## PTCRN < PTOC

See [this counterexample](2024-06-03-three-discrete-distributions-cant-be-pairwise-optimally-coupled.md).

(Note: Since writing that post, I learned of [Angel and Spinka (2019)](https://arxiv.org/abs/1903.00632), in which they give the same counterexample. That preprint is very interesting and deserves a post discussing it.)

## PTOC <= APOC

This is immediate from the fact that APOC is constructed to be optimal for every prefix share-probability. See for example [my first post on APOC](2024-03-05-all-prefix-optimal-coupling-for-model-comparison.md).

## PTOC < APOC

See [this counterexample](2024-02-27-whole-response-coupling-can-outperform-per-token-coupling-an-example.md).

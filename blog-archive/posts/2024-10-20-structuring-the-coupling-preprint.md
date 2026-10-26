---
title: "Structuring the coupling preprint"
date: 2024-10-20T20:59:41+00:00
modified: 2024-10-20T20:59:41+00:00
url: https://masharpe.wordpress.com/2024/10/20/structuring-the-coupling-preprint/
tags: ["coupling", "research", "writing"]
categories: ["Uncategorized"]
---

# Structuring the coupling preprint

I am now continually faced with the challenge of framing and structuring the coupling preprint. For my own reference, focusing on maximal recoupling was suitable, but to interest others, it flows more naturally as:

- Motivation: discrete-diffusion LLMs.
- Problem: simultaneously maximal coupling of Bayesian networks (SMC-BN).
- Solution: simultaneously maximal coupling of chain-product trees (SMC-CPT); maximal recoupling (MRC).

CPT is a new abstraction. It turns out that applying SMC directly to BNs is not so natural. It makes sense to state the problem in terms of BNs, because that’s terminology people will recognize, but, when presenting the solution, I should switch to more appropriate custom terminology.

For structuring the preprint, an outlining approach can be: definitions -> algorithms -> theorem statements -> lemma statements -> proofs. The forwards flow here is greater than the backwards flow. e.g. Changing a proof may not have many repercussions, but changing a definition has many repercussions. This provides the motivation for introducing CPTs as a concept now.

A CPT is a rooted directed tree, with all arcs oriented towards the root, with three kinds of nodes: leaves, chains, and products.

- A leaf node has no children and gives the distribution of an atomic subvariable.
- A chain node has one child and refines the child subtree’s distribution with an additional subvariable.
- A product node has two children whose distributions are combined by tensor product.

[This appeared with slightly different terminology in the pseudocode post.](2024-10-08-full-pseudocode-for-sampling-from-a-simultaneous-maximal-coupling-of-bayesian-networks.md)

The solution to SMC-BN can then be structured something like:

- Theorem characterizing SMC-BN.
  - Possible case: delegated to SMC-CPT.
  - Impossible case: via generalized examples.
- SMC-CPT.
  - Definition of CPT.
  - Statement of SMC-CPT-Cond and SMC-CPT algorithms.
  - Theorem: validity, maximality, efficiency.
- MRC.
  - Statement of MRC-Cond algorithm.
  - Theorem: validity, maximality, efficiency, preservation.

Note that we won’t give an explicit algorithm for SMC-BN. In practice, if you want to use the solution, you would want to reformulate your problem in terms of CPTs.

## Properties of SMC-CPT

The SMC-CPT algorithm has two versions: the unconditional SMC-CPT and the conditional SMC-CPT-Cond. The user would typically invoke SMC-CPT, but it’s easier to analyze the conditional version.

Given X, Y, and a CPT T, here are the properties of SMC-CPT-Cond:

(validity) If `Xhat ~ P_X`, then `SMC-CPT-Cond(Xhat) ~ P_Y`.

(maximality) If `Xhat ~ P_X`, then, for every subtree T’, the set S of indices in T’ satisfies

```
Phat[Xhat_S != SMC-CPT-Cond(Xhat)] = D_TVD(P_X, P_Y)
```

(efficiency) If, for some `lambda > 0`, a series of calls to SMC-CPT-Cond satisfies, for every `x in E`,

```
E[# calls with x] <= lambda P_X(x),
```

then, for every `x in E` and i,

```
E[# generations from P_{Y_i|X_i=x_i}] <= lambda P_{X_i}(x_i).
```

(I am not certain that introducing lambda actually helps.)

## Properties of MRC

MRC has some properties that we need for SMC-CPT but others that are unnecessary, though they may be interesting and aid understanding.

Necessary for SMC-CPT:

- Validity
- Maximality
- Detailed efficiency: input frequency `<=P_X(x)` implies subcall frequency `<=P_X(x)`
- Maximal subcouplings remain maximal

Bonus properties for subcouplings:

- Self-loops don’t decrease.
- Cost decrease upper bounds sum of gross non-self arc increase.
- Consequence of previous two: `TVD(P,Phat) <= 2 (cost decr)`.

More bonus properties:

- Closed-form formula for the result of MRC.
- Short (but computationally inefficient) existence proof.

Since some of these proofs involve (basic) Markov chain theory, plus terminology from network flows, I’d ideally like to quarantine all that inside one powerful lemma. The statement of such a lemma remains to be determined.

A note on the statement of MRC and MRC-Cond: In the reference document, I stated the unconditional version of MRC and compared it to the unconditional version of CMC (classic maximal coupling). But the conditional variant MRC-Cond is really the more useful algorithm, so it would be better to use CMC-Cond as the comparison, which is slightly different from how it’s presented in Johnson 1998.

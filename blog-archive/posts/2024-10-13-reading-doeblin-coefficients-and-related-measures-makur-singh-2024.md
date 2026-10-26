---
title: "Reading: “Doeblin Coefficients and Related Measures”, Makur & Singh 2024"
date: 2024-10-13T18:52:32+00:00
modified: 2024-10-13T18:52:32+00:00
url: https://masharpe.wordpress.com/2024/10/13/reading-doeblin-coefficients-and-related-measures-makur-singh-2024/
tags: ["coupling", "reading"]
categories: ["Uncategorized"]
---

# Reading: “Doeblin Coefficients and Related Measures”, Makur & Singh 2024

This paper caught my attention by being a rare hit for “simultaneously maximal coupling” in a Google Scholar search. I wanted to see what it had to say about that topic. Here are my notes from skimming relevant sections.

Link: [“Doeblin Coefficients and Related Measures”, Makur & Singh 2024](https://arxiv.org/abs/2309.08475)

## Relevant content

The main purpose of this paper is to study “Doeblin coefficients”. In the paper, Definition 1: given a row-stochastic matrix W, the Doeblin coefficient `tau(W)` is the sum of the minimum values of the columns. Note that, for a two-row matrix, this is one minus the TVD, and is the agreement probability of a maximal coupling of two random variables with marginal distributions given by the rows.

Like in the two-row case, an n-way coupling exists with all-way agreement probability `tau(W)` (Section II-A, Thoerem 2). The proof (Section III-B) goes similarly to the 2-way case: assign probability to the agreement, then make the residual sampling independent (conditioned on non-agreement). They give a formula to do this.

Section II-D studies simultaneously maximal coupling in Theorem 5. They use transposed notation compared to me: two token positions (X and Y) with n joint distributions. (Why they only study two token positions and not more, I don’t know–presumably it’s enough for the results they want to prove.) The proof (Section IV-A) again uses a formula, assigning the necessary probabilities to agreements and sampling residuals independently. [(Compare with my post on a formula for APOC.)](2024-06-21-specifying-apoc.md)

One minor note is that finite alphabets are used throughout. They say that many results can be extended but that doing so introduces new difficulties.

## Comparison to Angel & Spinka 2021

Given that they’re coupling n>=3 variables, I was surprised to not see a mention of [Angel & Spinka 2021](https://arxiv.org/abs/1903.00632). The key difference is that Makur & Singh maximize n-way agreement probability. Angel & Spinka try to simultaneously maximize the pairwise (2-way) agreement probabilities, which they show is not possible in general, so they settle for an approximation.

## Future reading

**“Maximal Coupling”, Goldstein 1979.** This is cited as the simultaneously-maximal-coupling result being generalized. Having glanced at it, it concerns non-Markovian coupling, which is what interests me, so it’s definitely worth a look.

**“Strong data-processing inequalities for channels and Bayesian networks”, Polyanskiy & Wu 2017.** They cite Remark 10 as giving an example of impossibility of simultaneously maximally coupling all of the whole joint and both positions. That means this paper must also investigate simultaneously maximal couplings in some way.

**“Markov Chains and Mixing Times”, 1st ed, Levin et al. 2009.** They cite Proposition 4.7 of this text for the fact that TVD is the disagreement probability of maximal coupling, credited to Dobrushin.

**“Probabilistic Machine Learning: Advanced Topics”, Murphy, 2023.** They cite Section 4.2 for formalization of Bayesian networks. My understanding of Bayesian networks is fuzzy at best, so to express SMC-BN well, it may be helpful to consult this text.

## Popularity

- Posted: 2023.
- Published: IEEE Transactions on Information Theory, 2024.
- Citations: 4.

## Discussion

- This paper uses the term “simultaneously maximal coupling” in the same way that I do, which makes me comfortable using that term.
- That they restrict their attention to finite alphabets gives me some comfort to restrict myself to finite alphabets, too.
- The use of formulas, rather than sampling algorithms, is less interesting to me, since I am primarily interested in the LLM setting in which we want to sample from (simultaneously) maximal couplings, not just establish their existence. In fact, it’s a bit unclear to me what the motivating application is behind this paper.

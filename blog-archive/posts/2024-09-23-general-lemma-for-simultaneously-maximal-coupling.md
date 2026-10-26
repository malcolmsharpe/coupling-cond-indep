---
title: "General lemma for simultaneously maximal coupling"
date: 2024-09-23T20:26:45+00:00
modified: 2024-09-23T20:26:45+00:00
url: https://masharpe.wordpress.com/2024/09/23/general-lemma-for-simultaneously-maximal-coupling/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# General lemma for simultaneously maximal coupling

In [my previous post](2024-09-22-key-lemma-for-ncfoc.md), I presented a lemma that allows proving NCFOC by constructing a maximal coupling that preserves two smaller pre-existing maximal couplings. To generalize to simultaneously maximal couplings in Bayesian networks (SMCBN), I needed another easier lemma, and, while thinking how to prove it, I realized that I could generalize both lemmas considerably with a unified proof. That generalized lemma is presented in this post.

**Lemma.** Take random variables X1, …, Xn, Y1, …, Yn. There exists a maximal coupling `P*` of X and Y such that, for every `S subset of [n]` for which X_S and Y_S were maximally coupled, `P*` preserves the marginal distribution of `(X_S, Y_S)`.

**Proof.** Use an LP:

- The feasible solutions are the probability vectors that are couplings of X and Y and preserve the specified marginals.
- The objective is to maximize `P[X = Y]`.

The original joint distribution is a feasible solution of the LP, and, since the feasible solutions are probability vectors, the LP is bounded. Since the LP is feasible and bounded, it has an optimal solution `P*`.

We only need show that `P*` is a maximal coupling of X and Y.

Suppose otherwise. Then there exist a,b,c such that b != a, c != a, `p*(a,b) > 0`, `p*(c,a) > 0`. Let `delta = min{ p*(a,b), p*(c,a) }` and set `ptilde = p* + delta (e_{aa} + e_{cb} - e_{ab} - e_{ca})`. Observe that ptilde is still a valid coupling and has `Ptilde[X = Y] = delta + P*[X = Y]`.

**Claim.** For every `S subset of [n]` for which X_S and Y_S were maximally coupled, ptilde preserves the marginal distribution of `(X_S, Y_S)`.

Proving this claim will show that ptilde is a feasible solution to the LP with greater objective value than `P*`, a contradiction, which will complete the proof of the lemma.

**Proof of claim.** Since `p*(a_S, b_S) >= p*(a, b) > 0` and `p*(c_S, a_S) >= p*(c, a) > 0`, we have at least one of a_S = b_S or a_S = c_S. Without loss of generality, a_S = c_S.

Then delta mass was moved from `(a_S, b_S)` and `(c_S, a_S) = (a_S, a_S)` to `(a_S, a_S)` and `(c_S, b_S) = (a_S, b_S)`, which is no change. **[]**

## Discussion

If you can tolerate dealing with the entire joint distribution, this lemma gives a construction for the maximal coupling: either solve the LP or repeatedly apply the exchange move. But in practice, it’s computationally impractical to manipulate the entire joint distribution, so efficient sampling remains for future work.

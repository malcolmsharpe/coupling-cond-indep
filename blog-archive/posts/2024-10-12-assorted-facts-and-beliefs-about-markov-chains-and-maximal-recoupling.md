---
title: "Assorted facts and beliefs about Markov chains and maximal recoupling"
date: 2024-10-12T20:56:47+00:00
modified: 2024-10-12T20:56:47+00:00
url: https://masharpe.wordpress.com/2024/10/12/assorted-facts-and-beliefs-about-markov-chains-and-maximal-recoupling/
tags: ["coupling", "research"]
categories: ["Uncategorized"]
---

# Assorted facts and beliefs about Markov chains and maximal recoupling

Here are some odds and ends that may be useful for the preprint draft.

## Markov chains

### Flow implied by stationary distribution

Let P be the transition matrix of a finite Markov chain, and let pi be a stationary distribution, i.e. `pi^T P = pi^T`. Let `A = Diag(pi) P`.

Then the sum of A is 1 and, for all i, its ith row sum equals its ith column sum equals pi_i.

Proof of whole sum:

```
1^T A 1
    = 1^T Diag(pi) P 1
    = 1^T Diag(pi) 1
    = 1
```

Proof of row sum: for all i,

```
e_i^T A 1
    = e_i^T Diag(pi) P 1
    = e_i^T Diag(pi) 1
    = e_i^T pi
    = pi_i
```

Proof of column sum: for all i,

```
1^T A e_i
    = 1^T Diag(pi) P e_i
    = pi^T P e_i
    = pi^T e_i
    = pi_i
```

So A gives a joint distribution of transitions. Moreover, if `(I,J) ~ A`, then `Law(I) = Law(J) = pi`, so A is a coupling of pi with pi.

### Beliefs

I have reasonable confidence that these beliefs are true, though maybe with slightly different conditions. I would like to find them in a Markov chain reference so that I can cite them.

**Belief.** Given a Markov chain with state space E and a stationary distribution pi, if `s in E` has `pi_s > 0`, then s is recurrent.

**Proof idea.** Suppose that s is not recurrent. Then there is a nonzero probability `p` that a path starting at s does not return to s. Consider the distribution of infinite paths with starting state distributed according to pi. There is some probability that such a path does not contain s. By taking one step, that probability increases by `pi_s * p > 0`. But pi was a stationary distribution, so the distribution of paths is the same, a contradiction. **[]**

I call the above a proof idea rather than a proof because it is not quite rigorous. Some care is needed to handle the distribution of infinite paths, since in general there are uncountably many of them.

**Belief.** Let a Markov chain with finite state space E and transition matrix P have a stationary distribution pi. Let `s in E` have `pi_s > 0`. Let `A = Diag(pi) P`. For `i,j in E`, let `N_{ij}^{(s)}` be the expected number of transitions from i to j before the first return to s for a path that begins at s. Then `N_{ij}^{(s)} <= pi_s^{-1} A_{ij}`.

**Proof idea.** By the previous belief, s is recurrent. Consider the distribution of infinite paths with starting state distributed according to pi. Note that the chain may be reducible, so the measure of the subset of these paths that contain s may be less than 1. But since s is recurrent, every path that does contain s contains it infinitely many times, with probability 1.

Then compare frequency of s with the frequency of each transition. The frequency of s is given by pi_s; the frequency of each transition i,j is `A_{ij}`; and the frequency of each transition i,j that has s in the future is `<= A_{ij}`. Then we take the ratio of frequencies to get `N_{ij}^{(s)} <= pi_s^{-1} A_{ij}`. **[]**

The above proof idea has the same issues with handling the distribution of infinite paths rigorously, along with a new issue of relating this frequency ratio to the paths from s to itself.

**Believed corollary.** The expected number of transitions before first return is `<= pi_s^{-1}`.

## Maximal recoupling

### Efficiency

To use MRC recursively, as in SMC-I and SMC-BN, we need a finely-detailed claim about MRC’s efficiency.

**Belief.** Consider a series of calls to `MRC_{Y|X}` such that, for all x,

```
E[number of inputs x] <= P_X(x)
```

Then, for all x,

```
E[number of samples from "Y|X=x"] <= P_X(x)
```

### Reducing MRC’s loop to a Markov chain

Begin with the states as vertices with flow from v to w given by `P_{XY}(v,w)`. Add an auxiliary node s with flow that balances the original nodes. So s has outflow and inflow `D_{TVD}(X,Y)`, which we’ll label D for concision.

Then the total flow is `1 + 2D`. So, for all v, `pi_v = (1 + 2D)^{-1} f_v` is a stationary distribution. In particular, `pi_s = (1 + 2D)^{-1} D`. The mean hitting time of s is

```
<= pi_s^{-1} = (1 + 2D)/D
```

In MRC:

- The loop is entered with probability D.
- The number of samples from Y|X is “path length – 2”.

So the expected number of samples from Y|X per execution is

```
<= D ((1 + 2D)/D - 2)
= 1
```

### Effect on subcouplings

The most powerful statement about [MRC’s effect on subcouplings](2024-10-02-details-of-maximal-recouplings-effect-on-subcouplings.md) is the following. I have removed the equivalence class language that I’ve used before, because I don’t think it helps.

**Belief.** Let `f : E -> E'` be a function to a finite set E’. Let Phat be the joint distribution arising from applying MRC to a joint distribution P. Then

```
D_{TVD}(P_{f(X)f(Y)}, Phat_{f(X)f(Y)}) <= 2 (P[f(X) = f(Y)] - Phat[f(X) = f(Y)])
```

The proof idea I had in the previous post was rather handwavy, so I’d like to find a concise algebraic proof.

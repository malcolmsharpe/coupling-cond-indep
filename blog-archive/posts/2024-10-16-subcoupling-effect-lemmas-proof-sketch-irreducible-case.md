---
title: "Subcoupling effect lemmas proof sketch (irreducible case)"
date: 2024-10-16T22:15:08+00:00
modified: 2024-10-16T22:15:08+00:00
url: https://masharpe.wordpress.com/2024/10/16/subcoupling-effect-lemmas-proof-sketch-irreducible-case/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Subcoupling effect lemmas proof sketch (irreducible case)

Following on [from yesterday’s post towards proving the detailed effect of maximal recoupling on subcouplings](2024-10-15-towards-proving-detailed-effect-on-subcouplings.md), today I sketched proofs of all the necessary lemmas in the irreducible case.

First a note about irreducibility, then the proof sketches.

## Irreducibility

We’ll justify our use of the terminology “irreducible” by connecting to Markov chains. We’ve seen before that a joint distribution P can be transformed to a Markov chain by adding an auxiliary node that feeds the source and receives from the sinks.

**Claim.** P is irreducible if and only if its corresponding Markov chain is irreducible.

**Proof sketch.** P being irreducible means every node has a path to a sink, which is equivalent to every node having a path from a source, which together are equivalent to, in the Markov chain, the auxiliary node having a path to and from every node. **[]**

(Admittedly, more ought to be said about why a node having a path to a sink means it has a path from a source, and vice versa. It’s straightforward network flow stuff.)

## Lemma proof sketches

For conciseness, we’ll often write `P(x,y)` to mean `P_{XY}(x,y)`. When either input is a set, the meaning is to sum over that set.

Recall that, for irreducible P, the lemma from the last post said:

```
P = E_t[g_old(t)]
Phat = e_t[g_new(t)]
```

where

```
g_old(t) = sum_{i=1}^l e_{x_{i-1} x_i}
g_new(t) = sum_{i=1}^{l-1} e_{x_i x_i} + e_{x_0 x_l}
```

We’ll first analyze the self-loops, showing that they do not lose flow.

**Lemma (effect on subcoupling self-loops).** Assume P is irreducible. Take `S subseteq E`. Then

```
Phat(S,S) >= P(S,S)
```

**Proof sketch.** Observe

```
Phat(S,S) + Phat(S,E\S) = P_X(S)
P(S,S) + P(S,E\S) = P_X(S)
```

So

```
Phat(S,S) - P(S,S) = P(S,E\S) - Phat(S,E\S)
```

We must prove this is non-negative.

Using the lemma from last post,

```
P(S,E\S) - Phat(S,E\S)
    = E_t[g_old(t)(S,E\S) - g_new(t)(S,E\S)]
```

Consider the value inside the expectation for a trajectory `t = x_0, ..., x_l`. We will seek to prove that it is always non-negative. Since `S` and `E\S` are disjoint, then unless `x_0 in S` and `x_l not in S`, `g_new(t)(S,E\S) = 0` and the value is non-negative.

So assume `x0 in S` and `x_l not in S`. Then `g_new(t)(S,E\S) = 1`, and there exists `1 <= i <= l` such that `x_{i-1} in S` and `x_i not in S`. So

```
g_old(t)(S,E\S) >= g_old(t)_{x_{i-1} x_i} = 1
=> g_old(t)(S,E\S) - g_new(t)(S,E\S) >= 1 - 1 = 0.
```

So the expectation is over non-negative values and is thus itself non-negative, completing the proof. **[]**

The above lemma is already enough to prove that maximal subcouplings remain maximal, which is enough for the applications SMC-I and SMC-BN, but it’s not the most powerful result possible, so we forge onwards to prove that any increased flow on non-self arcs is compensated for by an improvement in cost.

**Lemma (effect on subcoupling non-self arcs).** Assume P is irreducible. Let F be a partition of E. Then

```
sum_{distinct S,T in F} (P(S,T) - Phat(S,T)) >= sum_{distinct S,T in F} max{0, Phat(S,T) - P(S,T)}
```

**Proof sketch.** We’ll use a claim.

**Claim.** For every trajectory t,

```
sum_{distinct S,T in F} (g_old(t)(S,T) - g_new(t)(S,T)) >= sum_{distinct S,T in F} max{0, g_new(t)(S,T) - g_old(t)(S,T)}
```

Once we have the claim, we can finish the proof by

```
sum_{distinct S,T in F} ( P(S,T) - Phat(S,T) )
= sum_{distinct S,T in F} ( E_t[g_old(t)(S,T)] - E_t[g_new(t)(S,T)] )
= E_t[ sum_{distinct S,T in F} ( g_old(t)(S,T) - g_new(t)(S,T) ) ]
>= E_t[ sum_{distinct S,T in F} max{0, g_new(t)(S,T) - g_old(t)(S,T)} ]    by claim
= sum_{distinct S,T in F} E_t[ max{0, g_new(t)(S,T) - g_old(t)(S,T)} ]
>= sum_{distinct S,T in F} max{0, E_t[g_new(t)(S,T) - g_old(t)(S,T)]}    by Jensen's inequality
= sum_{distinct S,T in F} max{0, Phat(S,T) - P(S,T)}
```

**Claim proof sketch.** Take a trajectory t. If `g_new(t)(S,T) <= g_old(t)(S,T)` for all `distinct S,T in F`, done.

So assume there exists `distinct S0,T0 in F` such that `g_new(t)(S0,T0) > g_old(t)(S0,T0)`. By the definitions, this means:

- `g_new(t)(S0,T0) = 1` and `g_old(t)(S0,T0) = 0`
- `x_0 in S_0` and `x_l in T_0`
- For all `1 <= i <= l`, either `x_{i-1} not in S0` or `x_i not in T0`.

Let `1 <= i <= l-1` be the first such that `x_i not in S0` and let `2 <= j <= l` be the last such that `x_{j-1} not in T0`.

Then `x_{i-1} in S0` and `x_j in T0`, which shows `i != j`. So

```
sum_{distinct S,T in F} ( g_old(t)(S,T) - g_new(t)(S,T) )
>= sum_{distinct S,T in F} ( (e_{x_{i-1} x_i} + e_{x_{j-1} x_j})(S,T) - g_new(t)(S,T) )
= 1 + 1 - 1
= 1
= sum_{distinct S,T in F} max{0, g_new(t)(S,T) - g_old(t)(S,T)}
```

which proves the claim, completing the proof. **[]**

---
title: "Organizing MRC properties"
date: 2024-10-17T19:47:54+00:00
modified: 2024-10-17T19:47:54+00:00
url: https://masharpe.wordpress.com/2024/10/17/organizing-mrc-properties/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Organizing MRC properties

We’ve established a few properties of MRC’s effect on subcouplings (with proofs in the irreducible case, and at least safe conjectures for the reducible case). Now I must decide which to include in the preprint and where. Here are the properties, briefly, and which others they directly imply:

- (i) Self-loops don’t decrease. => (v)
- (ii) Cost decrease upper bounds sum of gross non-self arc increase. => (v)
- Used together, (i) and (ii) imply (iii).
- (iii) TVD(P,Phat) <= 2 (cost decrease). => (iv), (v)
- (iv) Maximal subcouplings are preserved exactly. => (vi)
- (v) Subcoupling cost never increases. => (vi)
- (vi) Maximal subcouplings remain maximal.

Property (vi) is the weakest and is all we need for the application to simultaneously maximal coupling. It would be nice to express a single strongest property, but neither of (i) and (ii) implies the other, and they aren’t implied by (iii) either, so I think we need to state both. Everything that follows is an easy corollary of (i) and (ii), but (i) and (ii) are both tricky to prove (and require special care for the reducible case, too).

Since I haven’t written it before, here’s a proof that (i) and (ii) imply (iii).

**Corollary.** Assume P irreducible, E’ finite, `f : E -> E'`. Then

```
D_TVD(P_{f(X)f(Y)}, Phat_{f(X)f(Y)}) <= 2 (Phat[f(X) = f(Y)] - P[f(X) = f(Y)])
```

**Proof.** Let `F = {f^{-1}({x}) : x in E}`, so F is a partition of E. Then

```
D_TVD(P_{f(X)f(Y), Phat_{f(X)f(Y)})
= sum_{S,T in F} max{0, Phat(S,T) - P(S,T)}
= sum_{S in F} max{0, Phat(S,S) - P(S,S)} + sum_{S,T in F, S != T} max{0, Phat(S,T) - P(S,T)}
<= 2 sum_{S in F} (Phat(S,S) - P(S,S))
```

where the first term used (i) for equality and the second term used (ii) for inequality. **[]**

As for where to put each property:

- (i) and (ii) would be put in a theorem in the main body.
- (vi) would be either put near the proof of SMC-BN, or, if I mention it in the abstract, in the main body. (I guess it’s strange that I’m waffling between this result being minor enough to bury in an appendix versus it being notable enough to go in the abstract!)

We can concisely express all the important properties of the MRC algorithm’s induced coupling by:

**Theorem.** Let Phat be the coupling sampled by the MRC algorithm applied to P. Then:

- Phat is a maximal coupling.
- For all S, `Phat(S,S) >= P(S,S)`.
- For every partition F of E,

```
sum_{S in F} (Phat(S,S) - P(S,S)) >= sum_{S,T in F, S != T} max{0, Phat(S,T) - P(S,T)}
```

That maximal subcouplings remain maximal is a trivial corollary of the second property. The third property isn’t needed by any downstream application, but it’s interesting.

The other important property of the MRC algorithm is its efficiency, namely that it doesn’t sample the original coupling too much.

**Theorem.** If a collection of generations from `Phat_{Y|X}` satisfy, for all x,

```
E[number of generations from Phat_{Y|X=x}] <= P_X(x)
```

then generations from `P_{Y|X}` satisfy, for all x,

```
E[generations from P_{Y|X=x}] <= P_X(x).
```

The unconditional sampling case can be stated more simply:

**Theorem.** During one generation from `Phat_{XY}`,

```
E[number of generations from P_{XY}] <= 1.
```

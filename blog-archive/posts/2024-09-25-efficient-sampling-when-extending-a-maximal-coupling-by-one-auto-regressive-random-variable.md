---
title: "Efficient sampling when extending a maximal coupling by one auto-regressive random variable"
date: 2024-09-25T18:09:26+00:00
modified: 2024-09-26T19:18:38+00:00
url: https://masharpe.wordpress.com/2024/09/25/efficient-sampling-when-extending-a-maximal-coupling-by-one-auto-regressive-random-variable/
tags: ["coupling", "proof", "research", "sampling"]
categories: ["Uncategorized"]
---

# Efficient sampling when extending a maximal coupling by one auto-regressive random variable

In my previous post, we saw [a general lemma for extending maximal couplings to larger simultaneously maximal couplings](2024-09-23-general-lemma-for-simultaneously-maximal-coupling.md). Though the proof is pleasant, it doesn’t show how to efficiently sample from such a simultaneously maximal coupling.

In this post, I tackle the easiest step towards efficient sampling from a simultaneously maximal coupling: the case that corresponds to [APOC unconditional sampling](2024-07-04-apoc-unconditional-sampling-conceptual-pseudocode.md). Unlike in APOC, though, this sampling algorithm can extend *any* maximal coupling.

(The harder step is efficiently sampling from an independent combination of two maximal couplings.)

**Lemma.** Let P be a given probability distribution of random variables X1, X2, Y1, Y2, which range over finite sets, such that X1 and Y1 are maximally coupled. Then Algorithm (below) induces a new probability distribution Palg that maximally couples X and Y and preserves the given marginal distribution of (X1,Y1).

**Algorithm.**

1. Sample (a1, b1) with probability `P[X1 = a1, Y1 = b1]`.
2. If a1 = b1, with probability `sum_{a_2} min{ P[X=a], P[Y=a] } / P[X1 = Y1 = a1]`, sample a2 = b2 with weight `min{ P[X=a], P[Y=a] }`.
3. Otherwise, sample a2 with weight `max{0, P[X=a] - P[Y=a]}` and b2 with weight `max{0, P[Y=b] - P[X=b]}`.
4. Return X=a and Y=b.

**Proof of lemma.**

The four properties we must check are:

- (a) `Palg[(X1,Y1) = (a1,b1)] = P[(X1,Y1) = (a1,b1)]` for all a1, b1
- (b) `Palg[X=a] = P[X=a]` for all a
- (c) `Palg[Y=b] = P[Y=b]` for all b
- (d) `Palg[X=Y=a] = min{ P[X=a], P[Y=b] }` for all a

Property (a) shows the marginal distribution of (X1,Y1) was preserved. Properties (b) and (c) show that Palg is a valid coupling of X and Y. Property (d) shows that Palg is a maximal coupling of X and Y.

(a) Immediate from step 1 of the algorithm.

(d) We use the chain rule of probability, then substitute the probabilities from the algorithm, then simplify:

```
Palg[X=Y=a]
    = Palg[X1=Y1=a1] Palg[X2=Y2 | X1=Y1=a1] Palg[X2=Y2=a2 | X2=Y2, X1=Y1=a1]
    = P[X1=Y1=a1] (sum_{a2} min{P[X=a], P[Y=a]} / P[X1=Y1=a1]) (min{P[X=a], P[Y=a]} / sum_{a2} min{P[X=a], P[Y=a]})
    = min{P[X=a], P[Y=a]}
```

(b) We apply the law of total probability to sum over disjoint cases, then substitute the probabilities from the algorithm, then simplify:

```
Palg[X=a]
    = Palg[X=Y=a] + Palg[X=a, Y1=a1, Y2 != a2] + Palg[X=a, Y1 != a1]
    = min{P[X=a], P[Y=a]}
        + P[X1=Y1=a1] (1 - sum_{a'2} min{P[X=a'], P[Y=a']} / P[X1=Y1=a1]) max{0, P[X=a] - P[Y=a]} / sum_{a'2} max{0, P[X=a'] - P[Y=a']}
        + sum_{b1 != a1} P[X1=a1, Y1=b1]  max{0, P[X=a], - P[Y=a]} / sum_{a'2} max{0, P[X=a'] - P[Y=a']}
    = P[X=a]
```

(c) Similar to (b). **[]**

(Note: In the proof, I ignored various degenerate cases where the denominators can be zero. Explicitly handling them during the proof seems like a distraction, so it might be better to rewrite the proof to avoid division entirely.)

**Edit:** [Addendum.](2024-09-26-addendum-to-previous-post.md)

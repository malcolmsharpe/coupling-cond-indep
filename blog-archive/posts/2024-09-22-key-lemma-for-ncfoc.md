---
title: "Key lemma for NCFOC"
date: 2024-09-22T17:30:22+00:00
modified: 2024-09-22T17:30:22+00:00
url: https://masharpe.wordpress.com/2024/09/22/key-lemma-for-ncfoc/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Key lemma for NCFOC

I’ve now found a proof for the critical lemma that allows proving the NCFOC conjecture, and, by use of another easier lemma derived from APOC, [the conjecture for simultaneously maximal coupling of Bayesian networks (SMCBN)](2024-09-19-conjecture-the-broadest-generalization-of-apoc-and-ncfoc.md). This post contains a draft of the proof.

This lemma is the only novel cleverness needed to prove NCFOC and SMCBN. Everything else is either an easy variation of known results or easy induction. The lemma proof itself is not too hard–the main hard part was realizing what the lemma statement should be.

**Lemma (exchange).** Assume X1, X2, Y1, Y2 are RVs such that X1 and Y1 are maximally coupled and X2 and Y2 are maximally coupled. Then there exists a maximum coupling P\* of X = (X1, X2) and Y = (Y1, Y2) that preserves the marginal distributions of (X1, Y1) and (X2, Y2). i.e.

```
P*[X = Y = a] = min{ P*[X=a], P*[Y=a] } forall a
P*[X=a] = P[X=a] forall a
P*[Y=a] = P[Y=a] forall a
P*[X1 = a /\ Y1 = b] = P[X1 = a /\ Y1 = b] forall a,b
P*[X2 = a /\ Y2 = b] = P[X2 = a /\ Y2 = b] forall a,b
```

For the proof, we’ll need a certain proposition about maximal couplings:

**Proposition.** Assume X and Y are RVs over the same finite set Sigma. Then X and Y are maximally coupled if and only if, for every a,b,c in Sigma with b != a and c != a, we have at least one of `P[X=a /\ Y=b] = 0` or `P[X=c /\ Y=a] > 0`.

The proof idea for this proposition is that, in a maximal coupling, only one of X and Y can have spare probability for a.

**Proof of lemma.** Let `phat(x1, x2, y1, y2)` be the given joint distribution. Consider the linear program whose feasible solutions are the marginal-preserving joints and whose objective is the probability of X=Y:

```
max sum_a p(a1, a2, a1, a2)
s.t.
    sum_b p(a1, a2, b1, b2) = sum_b phat(a1, a2, b1, b2) forall a
    sum_b p(b1, b2, a1, a2) = sum_b phat(b1, b2, a1, a2) forall a
    sum_{a2,b2} p(a1, a2, b1, b2) = sum_{a2,b2} phat(a1, a2, b1, b2) forall b1,a1
    sum_{a1,b1} p(a1, a2, b1, b2) = sum_(a1,b1) phat(a1, a2, b1, b2) forall b2,a2
    1^T p = 1
    p >= 0
```

Observe that:

- phat is a feasible solution
- All feasible solutions are probability vectors, so the LP is bounded.

Since the LP is feasible and bounded, it has an optimal solution `p*`. It’s enough to prove that `p*` is a maximal coupling of X and Y, since the LP constraints ensure that the marginal preservation conditions hold.

For notation, let `P*[X = a /\ Y = b] = p*(a1, a2, b1, b2)` forall a,b.

Suppose `p*` is not maximal. Then, by the Proposition, there exist a,b,c,d,e,f with (c,d) != (a,b) and (e,f) != (a,b) such that

```
  1 2             1 2
X a b    and    X e f
Y c d           Y a b
```

both have positive probability.

So either a != c or b != d; without loss of generality, a != c. Since X1 and Y1 are maximally coupled and both `P*[X1 = a /\ Y1 = c] > 0` and `P*[X1 = e /\ Y1 = a] > 0`, we have a = e (by the Proposition).

Then, since (e,f) != (a,b), we have b != f. Since X2 and Y2 are maximally coupled and both `P*[X2 = b /\ Y2 = d] > 0` and `P[X2 = f /\ Y2 = b] > 0`, we have b = d.

Taken together, we found positive probability for

```
  1 2             1 2
X a b    and    X a f
Y c b           Y a b
```

Let `delta = min{ p*(a,b,c,b), p*(a,f,a,b) } > 0` be the minimum probability of these two configurations. We will move delta probability mass to

```
  1 2             1 2
X a b    and    X a f
Y a b           Y c b
```

i.e. Let

```
ptilde = p* + delta ( evec(a,b,a,b) + evec(a,f,c,b) - evec(a,b,c,b) - evec(a,f,a,b) )
```

Then the change to the marginals is

```
RVs      decreased by delta    increased by delta
X1,X2    ab, af                ab, af
Y1,Y2    cb, ab                ab, cb
X1,Y1    ac, aa                aa, ac
X2,Y2    bb, fb                bb, fb
```

The decreases and increases balance, so ptilde is feasible for the LP.

Also, the objective increased by delta, i.e. `LPobj(ptilde) = delta + LPobj(p*)`, which contradicts optimality of `p*`. **[]**

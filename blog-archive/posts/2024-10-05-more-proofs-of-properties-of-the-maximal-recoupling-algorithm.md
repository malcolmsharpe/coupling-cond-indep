---
title: "More proofs of properties of the maximal recoupling algorithm"
date: 2024-10-05T22:07:22+00:00
modified: 2024-10-05T22:07:22+00:00
url: https://masharpe.wordpress.com/2024/10/05/more-proofs-of-properties-of-the-maximal-recoupling-algorithm/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# More proofs of properties of the maximal recoupling algorithm

Continuing on from [my previous post](2024-10-04-progress-towards-proving-properties-of-the-maximal-recoupling-algorithm.md), property status:

- Coupling validity:
  - Marginal of X: obvious.
  - Marginal of Y: previously.
- Coupling maximality: obvious.
- Termination: previously.
- Efficiency: today.
- Effect on subcouplings:
  - Preservation of maximal subcouplings: today.
  - “Coupling TVD <= 2 \* loss improvement”: todo.

The proofs remain quite sketchy, but I believe they are correct and complete (unlike [the “proof idea” on 2024-10-02](2024-10-02-details-of-maximal-recouplings-effect-on-subcouplings.md)), aside from parts marked TODO.

## Analysis framework

We’ll transform the MRC loop so we can analyze it as a random walk.

### Unaugmented graph

Let G0 = (V0, A0) be a directed graph whose nodes V0 are the values taken by X and Y. The arcs A0 are those with nonzero weight, where the weight of arc `vw` is `W0_{vw} = P[X = v, Y = w]`. (Note that self-loops are included.) We call a node v a source if it has more out-weight than in-weight and a sink if it has more in-weight than out-weight.

Observe that, for every node v in V0,

```
sum_w W0_{wv} = P[Y = v]
sum_w W0_{vw} = P[X = v]
```

So the sum of sink deficits is

```
sum_v max{0, sum_w (W0_{wv} - W0_{vw})}
     = sum_v max{0, P[Y=v] - P[X=v]}
     = TVD(X,Y)
```

and likewise the sum of source excesses is

```
sum_v max{0, sum_w (W0_{vw} - W0_{wv})}
    = TVD(X,Y)
```

### Augmented graph

G0 is not directly usable, since a random walk doesn’t take into account that we begin at a source and end at a sink.

Add an auxiliary node aux to obtain G = (V,A) and weights W where `V = V0 U {aux}` with, forall v in V0,

```
W_{aux v} = max{0, sum_w(W0_{vw} - W0{wv})}
W_{v aux} = max{0, sum_w(W0_{wv} - W0{vw})}
```

Then G is balanced: at every node, the in-weight and out-weight are equal. Also, `sum_v W_{aux v} = TVD(X,Y)`. For conciseness later, let `D = TVD(X,Y)`.

### Random walk

Let’s now consider random walks on the balanced weighted directed graph G, where at each step the next arc is chosen with probability proportional to its weight. We can express the transition matrix as follows:

For v in V, let

```
p_v = sum_w W_{vw} = 1^T W
p^{-1}_v = (p_v)^-1
```

The transition matrix A is then given by

```
A = Diag(p^{-1}) W
```

Observe that

```
p^T A
    = p^T Diag(p^{-1}) W
    = 1^T W
    = p
```

so p is an unnormalized stationary distribution.

Moreover, when a node is drawn from this stationary distribution, the probability of the next arc being vw is proportional to `W_{vw}`.

Other assorted facts that we’ll need:

- `1^T W 1 = 1 + 2 D`
- `1^T p = 1 + 2 D`
- `p_aux = D`

### Expected traversal count per arc

#### Irreducible case

Assume irreducibility.

Begin an infinite random walk at aux. Note that the Markov chain may be periodic, so we don’t necessarily converge to a stationary distribution. But we can use the Cesaro limit (TODO: presumably this is well-known Markov chain theory)

```
lim_{n -> inf} (1/n) sum_{k=1}^n e_{aux} A^n = p
```

(TODO: More should be said here about how the next point follows from the previous.)

Then, for all vw,

```
E[# traversals of vw per visit to aux]
    = (W_{vw} / sum(W)) / (p_{aux} / sum(p))
    = (W_{vw} / (1 + 2 D)) / (D / (1 + 2 D))
    = W_{vw} / D
```

Since the probability of reaching the loop in MRC is D, we have

```
E[# traversals of vw per execution of MRC] = W_{vw}
```

#### General case

TODO

Get

```
E[# traversals of vw per execution of MRC] <= W_{vw}
```

## Efficiency

We wish to bound the expected number of samples drawn from Y. A sample occurs when an arc vw is traversed, except if v or w is aux. So

```
E[samples from Y per execution of MRC]
    = sum_{v != aux, w != aux} E[# traversals of vw per execution of MRC]
    <= sum_{v != aux, w != aux} W_{vw}
    = 1
```

## Preservation of maximal subcouplings

Let V0 be partitioned into equivalence classes `[-]` such that P was a maximal coupling of [X] and [Y]. Let Phat be the probability distribution induced by MRC.

We must prove that, for all c and d,

```
Phat[ [X]=[c], [Y]=[d] ] = P[ [X]=[c], [Y]=[d] ]
```

If `[c] = [d]`, then by maximality of P for `[-]`,

```
Phat[ [X]=[c], [Y]=[d] ]
    = Phat[ [X]=[Y]=[c] ]
    <= P[ [X]=[Y]=[c] ]
    = P[ [X]=[c], [Y]=[d] ]
```

Otherwise, `[c] != [d]`. If MRC returns `(b_1, b_{k+1})` with `[b_1] = [c]` and `[b_{k+1}] = [d]`, then, by maximality, there exists `1 <= i <= k` such that `[b_i] = [c]` and `[b_{i+1}] = [d]`. (TODO: More should be said about why this follows from maximality.) So

```
Phat[ [X]=[c], [Y]=[d] ]
    <= sum_{v,w s.t. [v] = [c], [w] = [d]} E[# traversals of vw per MRC execution]
    <= sum_{v,w s.t. [v] = [c], [w] = [d]} W_{vw}
    = P[ [X]=[c], [Y]=[d] ]
```

Overall, we have

```
1
    = sum_{[c], [d]} Phat[ [X]=[c], [Y]=[d] ]
    <= sum_{[c], [d]} P[ [X]=[c], [Y]=[d] ]
    = 1
```

so all the inequalities hold with equality, as needed.

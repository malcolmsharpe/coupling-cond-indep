---
title: "Towards proving detailed effect on subcouplings"
date: 2024-10-15T19:38:03+00:00
modified: 2024-10-15T19:38:03+00:00
url: https://masharpe.wordpress.com/2024/10/15/towards-proving-detailed-effect-on-subcouplings/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Towards proving detailed effect on subcouplings

[Yesterday’s maximal recoupling draft](2024-10-14-mrc-reference-rough-draft.md) needs proofs for the appendix, and while I have sketches for many of them, the biggest hole is proving detailed effect on subcouplings (Proposition 4 in the PDF). In this post, I’ll state a lemma and give a proof sketch for it.

Because of the connection to Markov chains, we’ll call P *irreducible* if every `x in E` has a nonzero path (wrt P) to some “sink” `y in E`, where “sink” means `P_Y(y) > P_X(y)`.

In an execution of the MRC loop, call `a_0, ..., a_l` its *trajectory*, where `a_0 = x`, `a_l` is the final value of y, and `a_1, ..., a_{l-1}` are the intermediate values of a.

For a trajectory `t = a_0, ..., a_l`, let

```
g_old(t) = sum_{i=1}^l e_{x_{i-1} x_i}
g_new(t) = sum_{i=1}^{l-1} e_{x_i x_i} + e_{x_0 x_l}
```

where `e` indicates a one-hot vector.

**Lemma.** Assume P is irreducible. Then

```
P_{XY} = E_t[g_old(t)]
Phat_{XY} = E_t[g_new(t)]
```

where the expectation is over one execution of the maximal recoupling algorithm.

**Proof sketch.** We’ve shown previously that, given irreducibility, the expected number of transitions from x to y is `P_{XY}(x,y)`, which shows the first statement.

Now let’s show the second statement. For non-self arcs, the claim is immediate from the algorithm. So we only need to check self-loops.

Take `x in E`. From the algorithm, we have

```
Phat_{XY}(x,x) = min{ P_X(x), P_Y(x) }
``
Also,
```

E_t[g_new(t)*{xx}] = E_t[# times x is interior of t] = E_t[ (# times x is a tail in t) – {t_0 = x} ] = sum_y P*{XY}(x,y) – max{0, P_X(x) – P_Y(x)}  
= P_X(x) – max{0, P_X(x) – P_Y(x)}  
= min{ P_X(x), P_Y(x) }  
“`  
which establishes the equality. **[]**

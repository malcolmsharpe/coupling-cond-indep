---
title: "Towards the subcoupling effect in the reducible case"
date: 2024-10-17T21:38:59+00:00
modified: 2024-10-17T21:38:59+00:00
url: https://masharpe.wordpress.com/2024/10/17/towards-the-subcoupling-effect-in-the-reducible-case/
tags: ["coupling", "proof", "research"]
categories: ["Uncategorized"]
---

# Towards the subcoupling effect in the reducible case

[MRC’s effect on subcouplings is reasonably well sketched out in the irreducible case](2024-10-17-organizing-mrc-properties.md), but the reducible case offers some complication. This post sketches approaches.

## Proving loop effect

### Irreducible case

First, recall what we did for the irreducible case.

```
P = E_t[g(t)]
Phat = E_t[ghat(t)]
```

where

```
g(t) = sum_{i=1}^l e_{x_{i-1} x_i}
ghat(t) = sum_{i=1}^{l-1} e_{x_i x_i} + e_{x_0 x_l}
```

We want to show

```
P(S, E\S) >= Phat(S, E\S)
```

which we’ll obtain by showing

```
g(t)(S,E\S) >= ghat(t)(S,E\S)
```

Observe that the right-hand-side is either 0 or 1. The case where it’s 0 is vacuous.

If the right-hand-side is 1, then `x_0 in S, x_l not in S`, so there is i such that `x_{i-1} in S, x_i not in S`. Then

```
g(t)(S,E\S) >= (e_{x_{i-1} x_i})(S,E\S) = 1
```

which completes the proof.

## Reducible case

Reducibility doesn’t change the relationship of g and ghat, but it changes the relationships of P to g and Phat to ghat.

The impact of reducibility:

- For non-self arcs of Phat, equality still holds: for all v != w, `Phat(v,w) = E_t[ghat(t)(v,w)]`. So still have

```
Phat(S,E\S) = E_t[ghat(S,E\S)] <= E_t[g(t)(S,E\S)]
```

- We have seen in previous posts that `E_t[g(t)] <= P`, so

```
E_t[g(t)(S,E\S)] <= P(S,E\S)
```

That’s enough to adapt the proof.

## Other notes

Every non-self arc of Phat is contributed fully by ghat, even in the reducible case.

Contribution is all-or-nothing: for each arc vw, if vw is reachable by source/sink, then

```
P(v,w) = E_t[g(t)(v,w)]
Phat(v,w) = E_t[ghat(t)(v,w)]
```

Otherwise,

```
E_t[g(t)(v,w)] = 0
E_t[ghat(t)(v,w)] = 0
```

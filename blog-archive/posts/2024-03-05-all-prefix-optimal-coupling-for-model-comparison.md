---
title: "All-prefix-optimal coupling for model comparison"
date: 2024-03-05T23:02:33+00:00
modified: 2024-03-05T23:02:33+00:00
url: https://masharpe.wordpress.com/2024/03/05/all-prefix-optimal-coupling-for-model-comparison/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# All-prefix-optimal coupling for model comparison

Suppose you want to compare two models by coupling their nondeterministic responses. Two options for doing this are greedily coupling each token while generating and coupling whole responses. Greedily coupling tokens is what speculative decoding uses, because you want a long shared prefix. But, [as I showed with an example in a previous post](2024-02-27-whole-response-coupling-can-outperform-per-token-coupling-an-example.md), if you’d like the whole response to be equal, greedy token coupling is suboptimal. Unfortunately, when using whole-response coupling, resampling the whole response has no particular reason to generate a long shared prefix.

Is there a way to get the best of both worlds, getting long shared prefixes while still attaining the optimal probability that the whole responses are equal? It turns out that there is, I believe, though I haven’t finished checking the algorithmic details, so it still could be wrong. The coupling method will make prefixes of every length equal with maximum probability.

## Defining all-prefix-optimal coupling

We’ll couple model responses in such a way that every prefix is, considered in isolation, optimally coupled. Let P and Q be the distributions of responses for the two models. Let a be a token string of length L >= 0, and let X and Y be the length-L prefixes of the two model responses.

An all-prefix-optimal coupling C satisfies

```
C[X = a /\ Y = a]   = min{ P[X = a], Q[Y = a] }
C[X = a /\ Y != a]  = max{ 0, P[X = a] - Q[Y = a] }
C[X != a /\ Y = a]  = max{ 0, Q[Y = a] - P[X = a] }
C[X != a /\ Y != a] = 1 - max{ P[X = a], Q[Y = a] }
```

The justification for calling this “optimal” is as follows. Take a finite set S of token strings that satisfies:

- Prefix-free: no string in S is a prefix of any other string in S.
- Every sufficiently long string has a prefix in S.

By interpreting the elements of S as prefixes of responses, P and Q define probability distributions on S. Then C optimally couples P and Q on S with respect to non-equality cost (i.e. the cost is 0 if the same element of S is sampled, otherwise 1).

## Sketch of algorithm for sampling from the coupled distribution C

The previous section laid out the property that we want C to satisfy, but it didn’t construct a C satisfying that property nor even prove that one exists. In this section, I sketch an algorithm that samples from such a C (though it’s preliminary so bugs are quite possible).

At a high level, the algorithm begins in joint mode, sampling from both P and Q simultaneously, until a non-equal pair of tokens is sampled, at which point it switches to split mode, completing the two responses separately. Even once in split mode, both of the two branches require evaluating probabilities using both models.

Now, let’s describe each mode. Let x and y be the response prefixes sampled so far from P and Q, respectively.

### Joint mode

Note that, in joint mode, `x = y`. For each token t in the alphabet:

- Let `p(t) := P(x ++ t)` and `q(t) := Q(y ++ t)` be the probabilities after appending token t.
- Let `s(t) := min{p(t), q(t)}` be the probability of appending t and being in joint mode.
- Let `pR(t) := max{0, p(t) - s(t)}` and `qR(t) := max{0, q(t) - s(t)}` be the residuals.

Let `S(x) = min{P(x), Q(y)}`, which is the probability to have sampled x in joint mode. With probabilities `s(t)/S(x)` (which generally add up to strictly less than 1), append t to both x and y and remain in joint mode.

Otherwise, sample tx according to weight `pR(tx)` and append it to x, and sample ty according to weight `qR(ty)` and append it to y. Then continue sampling each response in split mode.

### Split mode

Without loss of generality, we describe sampling a token to append to x. In that case, `P(x) > Q(x)` holds as an invariant.

Define `p(t), q(t), s(t), pR(t), qR(t)` as before. Sample t according to weight `pR(t)` and append it to x, then continue sampling in split mode.

## Discussion

In the algorithm, there is an arbitrary choice of how to couple the two non-equal tokens at the moment of splitting. I left that independent in the algorithm.

The algorithm is reasonably simple to implement, but I’m still not sure that it’s correct.

As an alternative algorithm, it’s also possible to think of the response prefixes as forming a tree and define C bottom-up.

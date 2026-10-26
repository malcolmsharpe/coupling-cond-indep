---
title: "Sampling diverse LLM responses via generalized sampling-without-replacement"
date: 2024-05-03T03:55:27+00:00
modified: 2024-05-03T03:55:27+00:00
url: https://masharpe.wordpress.com/2024/05/03/sampling-diverse-llm-responses-via-generalized-sampling-without-replacement/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# Sampling diverse LLM responses via generalized sampling-without-replacement

Suppose we have a prompt where we want to evaluate k diverse random responses from one LLM. A simple option is to sample those responses independently. But more diversity is possible. (Indeed, it’s a general pattern that independent sampling tends to be prone to clumping.)

Instead of independent sampling, we’ll still generate k random responses, where each one is an unbiased sample from the LLM, but where the responses are coupled to increase their diversity. In the simpler case of a uniform probability distribution over a small finite set, sampling without replacement is a way of achieving such a coupling, where diversity is quantified as the number of unique items sampled. It is not however obvious how to generalize sampling without replacement to LLM responses, because:

- LLM responses have unequal probabilities
- For typical response lengths, any particular response is so unlikely that it will hardly ever be sampled twice anyway

This post addresses these issues one by one.

## Generalizing sampling-without-replacement to unequal probabilities

First let’s just consider a distribution P over a small finite set V. (Interpret V as the token vocabulary.)

The obvious approach is to remove items as we sample, but that causes the marginal distributions of all items except the first to be biased samples from P. For example, consider an item A with probability 99% and an item B with probability 1%. If you sample two items, you’ll nearly always sample A first and then B second. It might sound helpful to shuffle, but then the marginal distributions become 50%/50%, not the desired 99%/1%.

An approach that actually works:

- Partition the interval [0,1) into intervals with length corresponding to the probabilities of P.
- Optional: Shuffle the order of the intervals.
- Select a point x0 in [0,1) uniformly at random.
- Select also the k-1 other equally-spaced points `x0 + 1/k mod 1, x0 + 2/k mod 1, ...`.
- The k samples are then the items corresponding to the intervals pierced by those points.

Observations about this algorithm:

- Any item with probability less than `1/k` is never chosen twice. (This is tight: it’s easy to check that, for the marginal distributions to be correct, every item with probability greater than `1/k` must sometimes be chosen more than once.)
- In the case where P is the uniform distribution over V, the coupled distribution is exactly the same as sampling without replacement.

This procedure works well for a single token, but there are too many whole responses to enumerate them all.

## Extending to whole responses

We again choose k equally-spaced points in [0,1) uniformly at random. The task is how to decode these into whole responses.

The idea for decoding is to arrange the responses in lexicographic order. (Optionally, also shuffle the token order at each node.) That way, for every given prefix, the responses with that prefix are contiguous in [0,1). As a consequence, the sampling procedure avoids sampling responses with long shared prefixes.

Implementing this is tricky, because a single floating-point number doesn’t have enough random bits to select a whole response. I don’t know the best way, but one option would be to represent x as a lazy infinite string of bits, add the 1/k spacing using lazy arithmetic, then decode using arithmetic coding.

## Alternative for black box APIs

The above requires access to token probability distributions. There is an alternative that works with black box APIs.

It uses the same idea as my previous post. Here, rather than coupling two different LLMs, we’re coupling one LLM with itself k times. But similarly we can sample nk responses independently, arrange them into n k-tuples to maximize the expected diversity of a k-tuple, then select and internally shuffle a k-tuple uniformly at random to show to the user.

In this case, the optimization problem, of arranging nk responses into n k-tuples maximizing expected diversity, seems likely to be NP-hard for most diversity metrics you’d imagine. So some heuristic is required.

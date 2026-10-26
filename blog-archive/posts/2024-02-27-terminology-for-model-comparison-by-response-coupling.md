---
title: "Terminology for model comparison by response coupling"
date: 2024-02-27T20:51:42+00:00
modified: 2024-02-27T20:52:54+00:00
url: https://masharpe.wordpress.com/2024/02/27/terminology-for-model-comparison-by-response-coupling/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# Terminology for model comparison by response coupling

Since my earlier posts describing the technique for model comparison I called “joint generation”, I discovered that there is standard terminology and switched to that. Here is the key.

- “Joint generation” -> “coupling”. *Coupling* is the act of taking two probability distributions and introducing dependence between them.
- *Optimal transport* is the problem of choosing a coupling that optimizes the expected value of some given function of the random variables. (For example, you might want to maximize the probability that the two random variables are equal.)
- *Total variation distance* is half the L1 distance between two probability distributions.
- “Speculative sampling” can also be called “speculative decoding”. This terminology seems not standardized though.

Speculative decoding implicitly involves optimal transport, and [there is literature on applying it explicitly](https://arxiv.org/abs/2310.15141). My goal is fundamentally different though because speculative decoding is a performance optimization, whereas I’m interested in:

- Evaluation: making it easier for a human to compare two models.
- Synthetic data creation: generating paired data for DPO in which the pairs are similar, hopefully improving data efficiency.

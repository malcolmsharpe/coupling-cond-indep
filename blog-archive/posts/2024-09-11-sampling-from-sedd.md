---
title: "Sampling from SEDD"
date: 2024-09-11T19:15:22+00:00
modified: 2024-09-11T19:15:22+00:00
url: https://masharpe.wordpress.com/2024/09/11/sampling-from-sedd/
tags: ["coupling", "llm", "paper", "sampling"]
categories: ["Uncategorized"]
archive_note: related post not in the author's core list
---

# Sampling from SEDD

The paper [Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution (Lou et al. 2024)](https://icml.cc/virtual/2024/oral/35554) ([previous discussion](https://masharpe.wordpress.com/2024/09/10/generative-perplexity/)) proposes a discrete diffusion alternative to auto-regressive LLMs. In this post, we focus on sampling from a trained SEDD model. Motivating questions:

- Can SEDD be used as a draft model for speculative decoding?
- Can two SEDD response distributions be coupled using methods such as all-prefix-optimal coupling (APOC)?
- How fast is SEDD sampling?

## Basics of SEDD sampling

The structure of sampling from SEDD:

1. Start with a (possibly random) base state (conceptually, it’s noise).
2. Informed by the SEDD model, randomly select a new state.
3. Repeat step 2 a pre-determined number of times.

Different base states and transitions are possible, and the paper presents two; we’ll focus on “Absorb”. In Absorb, the base state is a string of d mask tokens (so it is *not* random), and the transitions change one or more mask tokens to non-mask tokens. Note that the string never changes length, and, once a token has been unmasked, it never changes.

## SEDD can’t be a fully probabilistic draft model

So, now that we understand the structure of sampling, what are the prospects for SEDD as a draft model in speculative decoding? For non-probabilistic speculative decoding (i.e. temperature zero), all you need is generated text, so of course SEDD can create those drafts. What’s more interesting is whether SEDD can be used with probabilistic speculative decoding (which is the kind originally proposed).

Probabilistic speculative decoding ordinarily requires auto-regressive next-token probabilities to compute accept probabilities and sample from the residual distribution when necessary. SEDD, being non-auto-regressive, does not provide next-token probabilities. This is already problematic.

What seems fatal for SEDD as a draft model is that it cannot even provide a probability for the draft as a whole. While I am not certain of this (since maybe there is some trick I don’t know), SEDD certainly can’t provide probabilities for given text, since that’s why the paper reports only upper bounds on negative log likelihood (NLL) via evidence lower bound (ELBO), not exact NLLs. I see no reason that SEDD would be able to report a probability for text it generates, either.

[There is a preprint on using SEDD for probabilistic speculative decoding.](https://arxiv.org/abs/2408.05636) How they obtain probabilities is explained in the first paragraph of subsection 4.1, but I don’t understand it. My guess is that they are using the SEDD model to suggest random local perturbations of its generated text. You could perhaps call that semi-probabilistic.

## Two SEDD sampling trajectories can be coupled

You might want to couple two SEDD models for reasons such as: speculative sampling for efficiency; or comparing similar models, prompts, etc. With image diffusion models, using a fixed seed for coupling is common, but it’s not obvious to me how you would use more advanced coupling methods (but I have very limited knowledge of diffusion models, so I am not confident in this claim).

Since SEDD sampling consists of a series of discrete random decisions, they can be coupled by the usual methods such as fixed seed, per-token optimal coupling (PTOC), and APOC.

There is an additional interesting opportunity with the example dynamics presented in the paper (such as Absorb). They sample the token transition at each index independently. The independence means one step could have all its indexes coupled by [non-crossing-family-optimal coupling (NCFOC)](2024-07-11-conjecture-non-crossing-family-optimal-coupling.md), if my conjecture is correct that NCFOC is possible for independent random variables.

To then extend the advantage of NCFOC to multiple steps would require some as-yet-unimagined generalization of both APOC and NCFOC.

## SEDD sampling is fast if you have enough parallelism

In Figure 1(a) of the paper, SEDD is shown as achieving better quality than GPT-2 for the same number of network evaluations, but I think there’s a catch: with GPT-2, each network evaluation only needs to compute the next token, whereas with SEDD, each network evaluation needs to reingest the entire token string. That’s because tokens can change anywhere in the string (in the two dynamics presented by the paper).

So each SEDD network evaluation requires much more parallelism than each GPT-2 network evaluation. If you have the parallelism available, that doesn’t add any latency. If you don’t, though, then latency per network evaluation will increase.

Another catch about SEDD’s performance is that unmasking several tokens independently simultaneously seems risky. What if they aren’t compatible? But if you only unmask one token at a time, you need as many network evaluations as GPT-2.

## Conclusion

- SEDD sampling consists of a series of random discrete decisions, modifying a token string.
- SEDD sampling does not produce probabilities, so it is not usable for fully probabilistic speculative decoding.
- SEDD sampling can be coupled by fixed seed, PTOC, APOC, and perhaps more advanced methods.
- Getting good sampling latency from SEDD requires plenty of parallelism.

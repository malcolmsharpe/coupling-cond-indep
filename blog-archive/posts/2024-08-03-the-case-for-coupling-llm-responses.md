---
title: "The case for coupling LLM responses"
date: 2024-08-03T18:46:59+00:00
modified: 2024-08-03T18:47:24+00:00
url: https://masharpe.wordpress.com/2024/08/03/the-case-for-coupling-llm-responses/
tags: ["coupling", "llm"]
categories: ["Uncategorized"]
---

# The case for coupling LLM responses

I’d like to present APOC in a useful way. Since APOC is an optimal method for coupling LLM responses, it’s an easy sell to users who already couple LLM responses using a fixed seed: APOC can be used in many of the same use cases for improved results.

What’s surprising is how rare it is to use a fixed seed to couple LLM responses:

- Searching the web reveals very little discussion of the technique in any context. (By contrast, fixed seeds are commonly discussed for image generation with Stable Diffusion.)
- [OpenAI’s seed parameter doesn’t ensure responses are fully deterministic](https://152334h.github.io/blog/non-determinism-in-gpt-4/).
- Anthropic doesn’t offer a seed parameter, and neither do any of the providers hosting Llama 3.1 405B. (I checked together.ai, Hyperbolic, Fireworks AI, Lepton AI, deepinfra, OctoAI, and NovitaAI.)

This post will argue that the current non-use of coupling is likely a mistake: there are many applications where coupling LLM responses should be beneficial, whether that’s with a fixed seed or a more advanced method such as APOC. (For this discussion, I’ll only list applications of coupling to make responses similar, although [there are potential applications for making responses dissimilar](2024-05-03-sampling-diverse-llm-responses-via-generalized-sampling-without-replacement.md), too.)

## Users that would benefit from coupling LLM responses

### Model users

Applications:

- Pairwise evaluation of different models or quantizations on a task (even, in principle, models with differing tokenizers). [Example.](https://github.com/Artefact2/llm-eval/blob/master/generate-answers)
- Prompt engineering (for evaluating the effect of prompt tweaks).
- Sampler configuration (e.g. to isolate the effect of temperature).
- Evaluation of control vectors, abliteration, etc.

### Model post-trainers

- Mid-training evaluation of fine-tuning (including SFT and DPO).
- Comparison of a pre-finetune model to a post-finetune model.

### Inference providers

- Inference latency optimization (i.e. speculative decoding). Note: Unlike the other applications listed here, speculative decoding uses per-token optimal coupling, not fixed-seed coupling, and is already in increasingly common use.

### Quantization researchers

- Qualitatively isolate the impact of quantization.

### Sampler researchers

- Sampler design (e.g. of new anti-repetition samplers).

### Data creators

- Production of pairs for preference labeling.

## Benefits from coupling LLM responses

Now that we’ve listed some use cases, here are the various benefits they’d receive:

- Reduce the cost of human evaluation of model pairs.
  - Fewer labels are required (because of variance reduction).
  - Each label is easier to assign (because pairs have fewer differences to consider).
- Reduce the cost of LLM inference during evaluation.
  - Fewer generations are required (because of variance reduction).
  - Fewer judgings are required (ditto).
- Tighten confidence bounds on evaluation metrics (by exploiting the cost reduction to increase sample size).
- Isolate differences in preference pairs (e.g. for more effective DPO data).
- Give insight into the qualitative effect of small changes.

## Discussion

To be truly compelling, the benefits must be quantified. That said, from the user perspective, there’s little downside to using a fixed seed: it’s a UX problem (the frontends don’t make it easy) and a backend problem (seed parameters are often not offered and often don’t ensure determinism). In image generation, where those problems are already solved, users commonly use fixed seeds.

Over time, as UIs and backends improve, I expect coupling LLM responses to become standard practice for many tasks. These applications will presumably initially use fixed seeds, since that is the most widely-available coupling method available.

Compared to fixed-seed, coupling methods that are specialized to two models (and require logprob interactions), such as PTOC and APOC, create greater difficulty for the UI and backend, so they need to offer compelling improvements over fixed seeds. I expect whether that’s the case will vary by application.

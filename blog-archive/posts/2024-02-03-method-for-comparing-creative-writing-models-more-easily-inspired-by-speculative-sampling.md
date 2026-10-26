---
title: "Method for comparing creative writing models more easily (inspired by speculative sampling)"
date: 2024-02-03T19:34:44+00:00
modified: 2024-02-03T19:34:44+00:00
url: https://masharpe.wordpress.com/2024/02/03/method-for-comparing-creative-writing-models-more-easily-inspired-by-speculative-sampling/
tags: ["evaluation", "llm", "sampling"]
categories: ["Uncategorized"]
---

# Method for comparing creative writing models more easily (inspired by speculative sampling)

For creative writing tasks, users must choose: model, quantization, prompt, and sampling parameters. To evaluate two options, the most accurate method is to generate responses from each and note which gives the preferred result, as judged by a human evaluator. Human evaluator time is expensive, so we’d like to make their job as efficient as possible.

(For convenience, I’ll use ‘model’ as a shorthand for ‘model, quantization, prompt, sampling parameters’. Using this terminology, the model fully specifies the probability distribution of the next token.)

A difficulty with comparing responses is that the random number generation introduces an additional source of variance that obscures the model difference. Even if the same model is used to generate both responses, the responses may have differing quality levels.

For deterministic tasks, such as answering a multiple choice question, that additional RNG variance doesn’t apply. But it’s particularly problematic for creative writing, where RNG variance is desirable.

In this post, I propose a method for making the responses more similar, so that the difference between them more clearly isolates the difference between the models. In particular, if the two models are identical, the responses will be identical, too.

## Review of speculative sampling

(See [https://blog.dust.tt/speculative-sampling-llms-writing-a-lot-faster-using-other-llms/](https://blog.dust.tt/speculative-sampling-llms-writing-a-lot-faster-using-other-llms/ ) for a more standard explanation.)

Let U be a finite set (e.g. tokens or characters) and let P and Q be two different discrete probability distributions over U. Let `X ~ P` and `Y ~ Q`.

We’d like to maximize `P(X = Y)` by carefully designing the joint distribution `R(X,Y)`. One procedure for obtaining the optimal joint distribution R is:

- Sample `X ~ P`.
- If `Q(X) > P(X)`, set `Y = X`.
- Otherwise, with probability `Q(X) / P(X)`, set `Y = X`.
- Otherwise, sample Y with weight `max{0, Q(Y) - P(Y)}`.

P is called the “draft model” and Q the “target model”. In typical applications of speculative sampling, the draft model is smaller and cheaper to evaluate than the target model, but that’s not generally true of our application.

## Extending to auto-regressive sequence sampling

In the sequence case, we care not just about whether the two responses are entirely equal but also about whether they are similar, for example as quantified by edit distance. If we apply the technique from the previous section directly, then, whenever the draft sequence is resampled, the entire sequence would be thrown out, which is wasteful of edit distance.

Instead, we’ll generate token-by-token, as with standard speculative sampling, until a resampling occurs. That way, at least some prefix of the responses will be equal, after which they diverge.

After diverging, can we reduce the edit distance for the remainder of the response? Yes! We can generate as much as we like of each response separately, then resume joint sampling according to some heuristic. For example, we might generate each response until it reaches a newline, then resume joint sampling. We could even imagine using reinforcement learning to train a language-model-based heuristic where the reward is the minimization of edit distance.

## Tokenizer independence

Suppose we’re comparing two models that use different tokenizers. It’s not immediately obvious how speculative sampling applies.

The trick is that any model that auto-regressively generates tokens implies a model that auto-regressively generates characters. To see that fact, take the token distribution and marginalize out all but the first character. After sampling the first character of the token, use the conditional token distribution (conditioned on the first character) to sample the next character, and so on.

By interpreting the two models as auto-regressive character generators, we can do speculative sampling on characters instead of tokens, making our technique tokenizer-independent.

Being tokenizer-independent brings a benefit for the rejoining heuristic too: it gives us the flexibility to, for example, generate each sequence until reaching a space character, then rejoining from there on.

## Applications

Who wants this? It’s a feature, not a product. It would fit best into a playground-like tool oriented towards creative writing tasks. Ideally, the tool would already be designed for model comparison and prompt engineering, allowing comparison of two responses.

The Chatbot Arena is an example of a tool where this feature would be useful, but a crucial limitation is that token probability distributions are required. Many APIs don’t provide token probabilities, and even with an API that does, the procedure would require making one call per token, which would be very slow. So this is best implemented closer to the model itself, at the same layer where you would implement ordinary speculative sampling.

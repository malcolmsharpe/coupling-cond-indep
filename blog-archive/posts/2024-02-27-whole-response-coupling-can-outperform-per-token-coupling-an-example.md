---
title: "Whole-response coupling can outperform per-token coupling: an example"
date: 2024-02-27T20:42:25+00:00
modified: 2024-02-27T20:42:25+00:00
url: https://masharpe.wordpress.com/2024/02/27/whole-response-coupling-can-outperform-per-token-coupling-an-example/
tags: ["coupling", "evaluation", "llm", "sampling"]
categories: ["Uncategorized"]
---

# Whole-response coupling can outperform per-token coupling: an example

Suppose we’re sampling from a model and a quant with the goal for the responses to be equal as often as possible. The optimal way is by coupling responses according to optimal transport with non-equality-indicator cost. But another natural approach is to couple the first token, then the next, etc., each again using optimal transport with non-equality-indicator cost.

It’s intuitively believable that the per-token coupling does not perform as well as whole-response coupling, as measured by non-equality-indicator cost of the whole responses. Here is a simple example confirming that intuition.

Let the token alphabet be {a,b}. We’ll generate length-2 responses. Model 1 is a uniform distribution over {aa, ab, bb}. Model 2 is a uniform distribution over {aa, ba, bb}.

Whole-response coupling yields a joint distribution that is uniform over:

- (aa, aa)
- (ab, ba)
- (bb, bb)

This joint distribution gives a 2/3 probability that the whole response is equal.

Now let’s calculate the effect of per-token coupling. First, coupling the first token gives this joint distribution that is uniform over:

- (a, a): in this case, 1/2 probability of equality, for (aa, aa)
- (a, b): in this case, 0 probability of equality
- (b, b): in this case, 1/2 probability of equality, for (bb, bb)

Altogether, there is a 1/3 probability that the whole response is equal.

## Discussion

For practical relevance, the important question to answer is how often the quant generates the same response as the original model. Whole-response achieves this optimally, and the example above shows that using per-token coupling instead can give worse results.

Whole-response coupling is less convenient, however, since there are too many responses possible to compute the entire distribution. But that turns out not to be a problem, since one response can be sampled from model 1, and the other response, if equality is rejected, can be sampled from model 2 using rejection sampling. If we only care about the probability of equality, we don’t even need to sample from model 2 at all.

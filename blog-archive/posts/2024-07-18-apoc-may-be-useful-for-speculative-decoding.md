---
title: "APOC may be useful for speculative decoding"
date: 2024-07-18T22:41:35+00:00
modified: 2024-07-18T22:41:35+00:00
url: https://masharpe.wordpress.com/2024/07/18/apoc-may-be-useful-for-speculative-decoding/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# APOC may be useful for speculative decoding

Speculative decoding is a technique for generating responses from large LLMs with lower latency by exploiting parallelism. It implicitly couples the draft model and reference model, with a per-token optimal coupling (PTOC), which inspired all-prefix-optimal coupling (APOC).

Given that spec dec inspired APOC, it’s natural to wonder whether APOC could be applied to speculative decoding. Indeed, this seems possible, if two conditions are met:

- The draft model must be sufficiently cheap to evaluate.
- The draft model must sometimes sample tokens that are more likely under the reference model than under the draft model. (For this to be true, the draft model must be probabilistic and must closely approximate the reference model.)

If these two conditions are met, here is an illustrative-but-extreme example of how you might do spec dec using APOC:

1. Sample the entire response using the draft model.
2. Using the start of the APOC conditional sampling algorithm, reject a suffix of the draft to find the split point, and sample a token at the split point.
3. The APOC conditional samplign algorithm would now usually sample a suffix; call this suffix distribution the “residual model”.
4. Return to step 1, recursively applying speculative decoding to the residual model.

Note that every iteration accumulates another instantiation of the draft model that must be evaluated, which is why the draft model must be very cheap. A milder form of this approach could generate only a certain number of tokens rather than a whole response. That’s essentially a hybrid of PTOC and APOC, and various other hybrids may be considered as well.

If APOC indeed proves useful for spec dec as I speculate above, that raises the possibility that APOC is already known in the spec dec literature, but I don’t think it is. Though there are many spec dec papers now, most of them are focused on engineering, and many are non-probabilistic (which makes APOC useless, as I mentioned earlier).

In a quick skim of the literature, I only found three spec dec papers that seem worth citing in a “Related Work” section:

- [The original Leviathan et al. 2023 speculative decoding paper.](https://arxiv.org/abs/2211.17192)
- [The later, independent reinvention by Chen et al. 2023.](https://arxiv.org/abs/2302.01318)
- [Sun et al. 2023, which makes the connection to coupling explicit.](https://proceedings.neurips.cc/paper_files/paper/2023/hash/6034a661584af6c28fd97a6f23e56c0a-Abstract-Conference.html)

The final paper, by Sun et al., is fundamentally still rooted in the per-token setting: their improvement is to generalize to multiple candidates per token. The novelty of APOC is to eliminate the dependence on the granularity of the tokenizer, and this is only possible by breaking out of the per-token viewpoint.

Unfortunately, demonstrating practical usefulness of APOC for spec dec would be quite challenging.

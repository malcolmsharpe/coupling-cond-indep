---
title: "Pseudocode for joint generation"
date: 2024-02-07T19:23:03+00:00
modified: 2024-02-07T19:24:57+00:00
url: https://masharpe.wordpress.com/2024/02/07/pseudocode-for-joint-generation/
tags: ["llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# Pseudocode for joint generation

Here is simple pseudocode for [my post about a method for more easily comparing non-deterministic responses from different models, quants, prompts, samplers, etc.](2024-02-03-method-for-comparing-creative-writing-models-more-easily-inspired-by-speculative-sampling.md) For simplicity, it uses only two models and no rejoining heuristic (such as rejoining on newlines, periods, or spaces).

Notice that it’s conceptually very similar to speculative sampling. Unlike spec samp, we continue joint generation even after resampling occurs.

```
def choose_token(weights):
    # Randomly choose a token according to the (possibly unnormalized) weights
    ...

def reuse_sample(distr_draft, token_draft, distr_target):
    prob_draft = distr_draft[token_draft]
    prob_target = distr_target[token_target]

    if random() * prob_draft < prob_target:
        return token_draft

    weights_excess = max{0, distr_target - distr_draft}
    return choose_token(weights_excess)

# Sample a response from the draft model
model_draft = ... # load draft model
distrs_draft = []
tokens_draft = []

do:
    distr_draft = model_draft(tokens_draft)
    token_draft = choose_token(distr_draft)

    distrs_draft.append(distr_draft)
    tokens_draft.append(token_draft)
while token_draft != EOS

unload(model_draft) # optionally unload draft model, to save VRAM

# Sample a response from the target model, reusing tokens when possible
model_target = ... # load target model
tokens_target = []

i = 0
do:
    distr_target = model_target(tokens_target)
    if i < len(tokens_draft):
        token_target = reuse_sample(distrs_draft[i], tokens_draft[i], distr_target)
    else:
        token_target = choose_token(distr_target)

    tokens_target.apppend(token_target)

    i += 1
while token_target != EOS

print(decode(tokens_draft))
print(decode(tokens_target))
```

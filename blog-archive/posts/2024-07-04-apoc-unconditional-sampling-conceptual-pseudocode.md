---
title: "APOC unconditional sampling: conceptual pseudocode"
date: 2024-07-04T20:08:20+00:00
modified: 2024-07-04T20:08:20+00:00
url: https://masharpe.wordpress.com/2024/07/04/apoc-unconditional-sampling-conceptual-pseudocode/
tags: ["coupling", "llm", "research"]
categories: ["Uncategorized"]
---

# APOC unconditional sampling: conceptual pseudocode

Although [I’ve previously described the algorithm for unconditional sampling from the APOC joint distribution](2024-03-05-all-prefix-optimal-coupling-for-model-comparison.md), that description was vague. For implementation purposes, it was necessary to create more precise descriptions.

The first such precise description of the APOC unconditional sampling algorithm is conceptual pseudocode: it specifies the algorithm precisely with minimum clutter, but it has limitations that make it unsuitable as a direct template for implementation, which I’ll discuss after.

## Pseudocode

```
for i = 0, 1, 2, ...:
    pxa := P[X_{<i} = a_{<i}]
    pyb := P[Y_{<i} = b_{<i}]

    forall t:
        pxat_V[t] := P[X_{<=i} = a_{<i} ++ t]
        pyat_V[t] := P[Y_{<=i} = a_{<i} ++ t]

        pxbt_V[t] := P[X_{<=i} = b_{<i} ++ t]
        pybt_V[t] := P[Y_{<=i} = b_{<i} ++ t]

    if a_{<i} = b_{<i}:
        pmeet_V := minimum(pxat_V, pybt_V) / min(pxa, pyb)
        pmeet := sum(pmeet_V)

        if random() > pmeet:
            goto else

        a[i] := b[i] := multinomial(pmeet_V)
    else:
        wxt_V := maximum(0, pxat_V - pyat_V)
        wyt_V := maximum(0, pybt_V - pxbt_V)

        a[i] := multinomial(wxt_V)
        b[i] := multinomial(wyt_V)
```

Terminology:

- X and Y are random variables for the two responses.
- a and b are the particular values of X and Y respectively during the current execution.
- t is a token.
- `random()` returns a number uniformly sampled from `[0,1)`.
- `multinomial(p_V)` returns a draw from the discrete distribution with probabilities given by `p_V`.

## Limitations

### Floating-point underflow

Token string probabilities, such as `P[X = a]`, will typically underflow the range of normalized floating-point numbers, even with double-precision floating-point.

To see why, note that -1022 is the minimum exponent representable by normalized double-precision floating-point numbers. `2^-1022` is about `2e-308`, so, for example, a 512-token response of 10%-probability tokens would underflow.

The solution is to use log-probabilities in the algorithm instead of probabilities.

### Not expressed in terms of LLM forward passes

The operation available with a real LLM is a forward pass that returns logits for the next token. The above pseudocode is instead expressed in terms of probabilities of prefixes.

It’s straightforward to convert from next-token logits to prefix probabilities, but some care is needed so that it works well with floating point.

### No EOS handling

Real LLMs typically terminate their generation with an end-of-string (EOS) token. Conceptually, it’s convenient to imagine that, once generation has produced one EOS token, the LLM will forevermore return 100% probability for the EOS token. In practice, though, LLMs will produce non-EOS tokens if generation is continued after EOS, so the EOS token must be specially handled.

### Poor time complexity

The various probabilities used in the loop body are probabilities of strings of tokens, so calculating them in the naive way recomputes many LLM forward passes in each iteration. It’s more efficient to accumulate probabilities so only a constant number of forward passes is needed in each iteration.

### Sensitivity to inference engine nondeterminism

Although an LLM forward pass theoretically always returns the same outputs when given the same inputs, this is typically not true with practical inference engines. (As one strange consequence, temp=0 sampling is nondeterministic with some APIs.) Since modern LLMs typically use bfloat16 as their floating-point type for inference, which has a small (7-bit) fraction, floating-point error can produce noticeable differences in the next-token probability distribution, so the impact of nondeterminism is non-negligible.

A partial solution is to never do an LLM forward pass with the same inputs twice. Instead, reuse the previous result. This is also faster, since LLM forward passes are expensive.

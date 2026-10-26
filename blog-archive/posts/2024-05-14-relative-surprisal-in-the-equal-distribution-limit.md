---
title: "Relative surprisal in the equal distribution limit"
date: 2024-05-14T18:21:11+00:00
modified: 2024-05-14T18:21:11+00:00
url: https://masharpe.wordpress.com/2024/05/14/relative-surprisal-in-the-equal-distribution-limit/
tags: ["entropy", "math", "probability"]
categories: ["Uncategorized"]
---

# Relative surprisal in the equal distribution limit

To make inference possible with large LLMs and limited VRAM, post-training quantization is commonly applied, which is essentially lossy compression, reducing the bits-per-weight at some loss of quality and fidelity to the original LLM. For example, LLMs are typically trained with 16 bpw, and quantization often reduces to values such as 8 bpw or 4 bpw.

Ideally, the quantized LLM would specify the same probability distribution as the original LLM. The distribution can be viewed as a distribution over tokens or a distribution over entire responses, and both viewpoints have their pros and cons. Practically, the quantized LLM won’t specify exactly the same distribution as the original LLM, but it will be very close, which motivates a theoretical study of the equal distribution limit.

One way to compare similar distributions is KL divergence, also known as relative entropy. Like how entropy can be thought of as the expected surprisal `E_{X~P}[-lg(P(X))]`, relative entropy can be thought of as the expected relative surprisal `E_{X~P}[lg(P(X)) - lg(Q(X))]`.

This post develops some background results useful for the following reasons:

- Relative entropy is asymmetric, so there’s a choice of whether to measure `D(quant || full)` or `D(full || quant)`. But it turns out that relative entropy becomes symmetric in the equal distribution limit, so it doesn’t matter which direction you choose.
- The coupling technique all-pairs-optimal-coupling (APOC) that I’ve described in previous posts competes against a simpler baseline of per-token coupling (PTC). Theoretically, APOC should outperform PTC when the standard deviation of relative surprisal greatly exceeds the expected relative surprisal. It turns out that the ratio of variance of relative surprisal to expected relative surprisal is a constant in the equal distribution limit, so the SD does in fact greatly exceed the mean, implying that APOC outperforms PTC in the equal distribution limit.

## Estimating expected relative surprisal

Let p and q be two nearly-equal probability distributions over a finite set with equal support. (“Equal support” is important because, if there’s an element where one distribution assigns zero probability and the other doesn’t, the relative entropy in one direction will be infinite.)

Then this is a formula for the expected relative surprisal, in nats:

```
D(p||q) = sum_i (p_i - q_i)^2 / (p_i + q_i) + O(||p - q||^3)
```

The idea for the derivation: let `r = (1/2)(p + q)` and `h = p - r`, then use `ln(a + x) - ln(a - x) = 2x/a + O(x^3)`.

Notice that the leading term is the same as for `D(q||p)`. So

```
D(p||q) ~ D(q||p)    as ||p - q|| -> 0
```

## Estimating variance of relative surprisal

This is a formula for the variance of the relative surprisal, in square nats:

```
V(p||q) = 2 sum_i (p_i - q_i)^2 / (p_i + q_i) + O(||p - q||^3)
```

The idea for the derivation: the square-mean is higher order, so calculate mean-square similarly to the previous derivation.

The leading term is a constant multiplied by `D(p||q)`, so we have

```
V(p||q) ~ (2 nats) D(p||q)    as ||p - q|| -> 0
```

`2 nats` is `2 / (ln 2) bits`, approximately `2.8854 bits`.

In my preliminary experiments, I’ve seen values for 8-bit quants such as 2.91 bits and 2.87 bits, and values for 4-bit quants such as 2.89 bits and 3.73 bits. So for the 8-bit quant (which we expect to be closer to the original LLM), the theoretical fit is good.

## References

Though “variance of relative surprisal” seems like a simple and natural quantity to study, I haven’t found the term used anywhere except in [[Boes et al., 2020]](https://arxiv.org/abs/2009.08391), which is doing something in quantum information theory that is beyond me.

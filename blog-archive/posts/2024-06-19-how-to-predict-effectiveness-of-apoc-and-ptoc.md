---
title: "How to predict effectiveness of APOC and PTOC"
date: 2024-06-19T18:14:22+00:00
modified: 2024-06-19T18:14:22+00:00
url: https://masharpe.wordpress.com/2024/06/19/how-to-predict-effectiveness-of-apoc-and-ptoc/
tags: ["coupling", "research", "theory"]
categories: ["Uncategorized"]
---

# How to predict effectiveness of APOC and PTOC

Suppose we want to empirically compare the effectiveness of APOC against baselines, such as PTOC, PTCRN methods (including ad hoc seed reuse), and independent generation. Assume the metric we’re computing is the longest-common-prefix survival function (LCP SF).

The simplest way to estimate the LCP SF is to generate using each method repeatedly and aggregate the results to obtain an empirical distribution. For ad hoc seed reuse, this may be the only option, if the generation is a black box, which is the case for proprietary APIs.

For other methods (including APOC, PTOC, certain PTCRN methods, and independent generation), though, we can estimate the LCP SF without fully generating a pair of responses. Estimating without generation has two advantages:

- Estimating the LCP SF may be simpler than sampling a pair of responses. This is particularly true for APOC, which has a tricky implementation, but where estimating the LCP SF is easy.
- Variance reduction techniques can increase the accuracy of our estimate.

The particular variance reduction technique we’ll use is “conditional Monte Carlo” (see Rubinstein and Kroese 2008). For a given threshold i, observe that

```
P[LCP(X,Y) >= i]
    = P[X_{<i} = Y_{<i}]
    = E_{a ~ X}[ P[Y_{<i} = a_{<i} | X_{<i} = a_{<i}] ]
```

The inner probability can be computed exactly for many coupling methods. For APOC:

```
P[Y_{<i} = a_{<i} | X_{<i} = a_{<i}]
    = min{1, P[Y_{<i} = a_{<i}] / P[X_{<i} = a_{<i}]}
```

For PTOC:

```
P[Y_{<i} = a_{<i} | X_{<i} = a_{<i}]
    = prod_{j<i} min{1, P[Y_j = a_j | Y_{<j} = a_{<j}] / P[X_j = a_j | X_{<j} = a_{<j}]}
```

For independent generation:

```
P[Y_{<i} = a_{<i} | X_{<i} = a_{<i}]
    = P[Y_{<i} = a_{<i}]
```

(Note: There is an additional minor opportunity for further variance reduction, which is to handle the token at position `i-1` specially, since the LLM forward pass gives us its full distribution. I have not yet made use of this extra trick, since it increases implementation difficulty.)

Something interesting about these formulas for the inner probability is that the formulas for independent generation and PTOC are monotone down as functions of i, but APOC’s formula is not. That means the estimates of APOC’s LCP SF may not be monotone, even though obviously the exact LCP SF must be.

For example results, [see a previous post](2024-06-04-apoc-will-substantially-outperform-ptc-on-nf8-quant-preliminary-experiment.md), showing a preliminary experiment estimating the longest-common-prefix survival function (LCP SF) for APOC and PTOC.

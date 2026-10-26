---
title: "APOC conditional generation algorithm"
date: 2024-06-09T20:20:26+00:00
modified: 2024-06-09T20:20:26+00:00
url: https://masharpe.wordpress.com/2024/06/09/apoc-conditional-generation-algorithm/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# APOC conditional generation algorithm

As previously discussed, All-Prefix Optimal Coupling (APOC) is a method for coupling two distributions over strings so as to maximize the length of their longest common prefix. Mathematically, APOC simply defines a joint probability distribution satisfying a desired optimality property, but, in practice, what we actually want is to sample from the joint distribution. Here are two main ways you might wish to do so:

- Unconditional sampling: sample from `P[X=a /\ Y=b]`. At a high level, the algorithm is to simultaneously generate the responses until they split, after which the responses are completed independently via split mode generation.
- Conditional sampling: given a response Y=b from one of the marginal distributions, sample from the conditional distribution `P[X=a | Y=b]`. The algorithm to realize this case will be the subject on this blog post.

Conditional sampling is more general, since it can be used to implement unconditional sampling. One good reason you might want conditional sampling is if you have one reference distribution from which you want to evaluate various perturbations. Examples: a full-precision model compared to a variety of quantizations; the current prompt compared to a variety of candidate replacements. In such a case, you can generate a response from the reference distribution once, then sample from each of the perturbed distributions conditioned on the reference distribution. (Additionally, those conditional samples can themselves be usefully coupled, but that is beyond the scope of this post.)

The conditional sampling algorithm is trickier than the one for unconditional sampling. The key aspect of APOC that makes it hard is that each token of X is influenced not only by previous tokens of Y but also *future* tokens of Y. That property is what gives APOC its power over simpler couplings such as Per-Token Coupling (PTC), but it also requires careful handling.

## Conditional generation algorithm, at a high level

To make the problem tractable, the key idea is to first sample the split point: the first index at which X and Y differ. Here is the high-level pseudocode:

```
1. Take Y=b.
2. Sample the split point I=i from distribution P[I=i | Y=b].
3. Set X_{<i} = a_{<i} := b_{<i}.
4. Sample X_{>=i} = a_{>=i} using split mode generation.
5. Return a.
```

## Conditional generation algorithm, in more detail

Now let’s see how to realize this algorithm idea. We’ll introduce the required probabilities here, but we still omit important adaptations for numerical stability and efficiency, which are left for a later post.

```
1. Take Y=b.

2. Let L = 1 + min{i : b_i = EOS}.

3. Sample split point I=i with probability proportional to

    If i = L,
        min{ P[X=b], P[Y=b] }

    If i < L,
        (min{ P[X_{<i} = b_{<i}], P[Y_{<i} = b_{<i}] } - sum_t min{ P[X_{<=i} = b_{<i} ++ t], P[Y_{<=i} = b_{<i} ++ t] })
        * prod_{i <= j < L} [
                (P[Y_{<j} = b_{<j}] - sum_t min{ P[Y_{<=j} = b_{<j} ++ t], P[X_{<=j} = b_{<j} ++ t] })^(-1)
                * max{0, P[Y_{<=j} = b_{<=j}] - P[X_{<=j} = b_{<=j}]}
            ]

4. Set X_{<i} = a_{<i} := b_{<i}.

5. Sample X_{>=i} = a_{>=i} according to the usual "split mode" algorithm:

    1. Initialize j := i.

    2. Sample a_j with probability
            (P[X_{<j} = a_{<j}] - sum_t min{ P[X_{<=j} = a_{<j} ++ t], P[Y_{<=j} = a_{<j} ++ t] })^(-1)
            * max{0, P[X_{<=j} = a_{<=j}] - P[Y_{<=j} = a_{<=j}]}

    3. If a_j = EOS, terminate.

    4. Set j := j + 1.

    5. Repeat from step 2.

5. Return a.
```

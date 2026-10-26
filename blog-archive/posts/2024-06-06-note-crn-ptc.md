---
title: "Note: CRN <= PTC"
date: 2024-06-06T22:18:22+00:00
modified: 2024-06-06T22:23:07+00:00
url: https://masharpe.wordpress.com/2024/06/06/note-crn-ptc/
tags: ["coupling", "llm", "research", "theory"]
categories: ["Uncategorized"]
---

# Note: CRN <= PTC

(This is essentially an appendix to an upcoming post, and is not expected to be understandable out of context.)

“CRN <= PTC” means the LCP SF of PTC dominates of LCP SF of any CRN-based method. The approach is to establish an upper bound that is obeyed by any CRN-based method, then show that PTC achieves that upper bound. Note that this applies no matter the choice of model, prompt, etc.–there is no situation in which CRN outperforms PTC at maximizing LCP.

The CRN-based method commonly used in practice, which is reusing a seed for multiple generations, is difficult to analyze because its behavior is an implementation detail of the inference engine. We’ll assume that the randomness is provided by a sequence of independent draws uniformly from [0,1), one per token index of the response: `U_0, U_1, ...`. Then the response `X` is determined using a (deterministic) token choice function `f`: `X_0 = f(U_0, X_{<0}), X_1 = f(U_1, X_{<1}), ...`.

Any method described by that framework satisfies a certain conditional independence property. Let X and Y be the responses we are coupling. Then for every token sequences a and b and index i,

```
P[X_i = a_i | X_{<i} = a_{<i}, Y_{<i} = b_{<i}] = P[X_i = a_i | X_{<i} = a_{<i}]
```

After all, the event `Y_{<i} = b_{<i}` only gives us information about `U_{<i}`, not the current random variate `U_i`. The symmetric property holds too:

```
P[Y_i = b_i | X_{<i} = a_{<i}, Y_{<i} = b_{<i}] = P[Y_i = b_i | Y_{<i} = b_{<i}]
```

Observe that PTC satisfies that conditional independence property too, because it couples the token distributions. (APOC does not satisfy the property, because the prefix of the other response determines whether we’re in joint mode or split mode. That allows APOC to achieve better performance.)

Thus, for every token sequence a and index i, we get the following upper bound, for both CRNs and PTC:

```
P[X_{<i} = Y_{<i} = a_{<i}]
    = prod_{j < i} P[X_j = Y_j = a_j | X_{<j} = Y_{<j} = a_{<j}]
    <= prod_{j < i} min{ P[X_j = a_j | X_{<j} = Y_{<j} = a_{<j}], P[Y_j = a_j | X_{<j} = Y_{<j} = a_{<j}] }
    = prod_{j < i} min{ P[X_j = a_j | X_{<j} = a_{<j}], P[Y_j = a_j | Y_{<j} = a_{<j}] }
```

Note that it’s only the final step that used the conditional independence property. For PTC only, we can continue, since it optimally couples at each token index:

```
    = prod_{j < i} P[X_j = Y_j = a_j | X_{<j} = Y_{<j} = a_{<j}]
```

which shows the upper bound is tight for PTC.

The LCP SF at index i is given by

```
sum_{distinct a_{<i}} P[X_{<i} = Y_{<i} = a_{<i}]
```

so the previous inequality applies to the LCP SFs too, as needed.

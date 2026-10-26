---
title: "Specifying APOC"
date: 2024-06-21T20:12:11+00:00
modified: 2024-06-21T20:12:11+00:00
url: https://masharpe.wordpress.com/2024/06/21/specifying-apoc/
tags: ["coupling", "research"]
categories: ["Uncategorized"]
---

# Specifying APOC

Before describing algorithms to sample from APOC, it is helpful to specify it precisely.

## Specification via optimality and conditional independence

This first way to specify APOC makes optimality clear.

We first require that APOC satisfies the [all-prefix-optimality property](2024-06-19-all-prefix-optimality-property-of-string-coupling.md): for every sequence a and for every index i,

```
P[X_{<i} = Y_{<i} = a_{<i}] = min{ P[X_{<i} = a_{<i}], P[Y_{<i} = a_{<i}] }
```

To specify a unique coupling, we additionally require the following conditional independence property: for all sequences a and b and for every index i,

```
(X_i = a_i ⫫ Y_{<=i} = b_{<=i} | X_{<i} = a_{<i} /\ X_{<=i} != Y_{<=i})
```

We also require the symmetric property (i.e. exchanging X with Y and a with b):

```
(Y_i = b_i ⫫ X_{<=i} = a_{<=i} | Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i})
```

## Implementation-friendly specification

This second way to specify APOC informs implementation of sampling.

Equality case: for every sequence a and index i,

```
P[X_i = Y_i = a_i | X_{<i} = Y_{<i} = a_{<i}]
    = min{ P[X_{<=i} = a_{<=i}], P[Y_{<=i} = a_{<=i}] }
      / min{ P[X_{<i} = a_{<i}], P[Y_{<i} = a_{<i}] }
```

Non-equality case: for all sequences a and b and for every index i,

```
P[X_i = a_i /\ Y_i = b_i | X_{<i} = a_{<i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
=   P[X_i = a_i | X_{<i} = a_{<i} /\ X_{<=i} != Y_{<=i}]
  * P[Y_i = b_i | Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
```

The factors are then given (proportionally, since it’s convenient to omit the normalizing constant) by

```
P[X_i = a_i | X_{<i} = a_{<i} /\ X_{<=i} != Y_{<=i}] ∝ max{0, P[X_{<=i} = a_{<=i}] - P[Y_{<=i} = a_{<=i}]}
```

and symmetrically

```
P[Y_i = b_i | Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}] ∝ max{0, P[Y_{<=i} = b_{<=i}] - P[X_{<=i} = b_{<=i}]}
```

The normalizing constants are obtained by summing over a_i (for the first formula) and b_i (for the second formula).

## Deriving the implementation version

We can derive the implementation-friendly specification from the one stated in terms of optimality and conditional independence.

The all-prefix-optimality property alone gives the equality case and the formulas for the factors in the non-equality case.

The conditional independence properties are used to factorize the non-equality case. This is tricky, so here is some more detail: for all sequences a and b and for every index i,

```
P[X_i = a_i /\ Y_i = b_i | X_{<i} = a_{<i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
=   P[X_i = a_i | X_{<i} = a_{<i} /\ Y_{<=i} = b_{<=i} /\ X_{<=i} != Y_{<=i}]
  * P[Y_i = b_i | X_{<i} = a_{<i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
```

by the chain rule.

We can apply the conditional independence property to the first factor directly, but the second factor requires special handling. We must apply the law of total probability over possible values for a_i, and within the sum we can use conditional independence:

```
P[Y_i = b_i | X_{<i} = a_{<i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
    = sum_{a_i} P[Y_i = b_i | X_{<=i} = a_{<=i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
                * P[X_i = a_i | X_{<i} = a_{<i} /\ Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
    = P[Y_i = b_i | Y_{<i} = b_{<i} /\ X_{<=i} != Y_{<=i}]
```

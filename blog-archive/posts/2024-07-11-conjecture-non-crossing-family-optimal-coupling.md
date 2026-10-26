---
title: "Conjecture: non-crossing-family-optimal coupling"
date: 2024-07-11T18:15:11+00:00
modified: 2024-07-11T18:15:11+00:00
url: https://masharpe.wordpress.com/2024/07/11/conjecture-non-crossing-family-optimal-coupling/
tags: ["coupling", "experiment", "math", "research"]
categories: ["Uncategorized"]
---

# Conjecture: non-crossing-family-optimal coupling

In searching for generalizations of APOC, one promising direction is to generalize its auto-regressive factorization to more general Bayesian networks. The fully general case is hard, so, to get started, it is helpful to pick another interesting special case of Bayesian networks, which is independent variables. (This is in a sense the opposite special case, since auto-regressive factorization corresponds to the maximum possible number of arcs in a Bayesian network, while independence corresponds to zero arcs.)

Even the special case of independence turns out to be hard, and I haven’t yet been able to prove an optimal coupling result for it. However, I’ve formulated a conjecture in which exploratory experiments give me some confidence.

## Conjecture: non-crossing-family-optimal coupling

Given:

- Finite set Sigma (the token vocabulary).
- Integer n >= 1.
- Random variables X,Y taking values in Sigma^n, such that `X_1,...,X_n` are independent and `Y_1,...,Y_n` are independent.

Let F be a non-crossing family of sets of indexes. i.e. F is a subset of `2^[n]`, and for every I,J in F, one of the following holds:

- `I /\ J = Empty`
- I subset of J
- J subset of I

Then there exists a coupling of X and Y such that, for every I in F and a in Sigma^n,

```
P[X_I = Y_I = a_I] = min{ P[X_I = a_I], P[Y_I = a_I] }
```

where `X_I = a_I` means `X_i = a_i forall i in I`.

## Discussion

Note that, since coupling X and Y doesn’t change the marginal distributions, we still have independence of `X_1,...,X_n` and independence of `Y_1,...,Y_n`.

The independence requirement is necessary, as shown by [the second counterexample of an earlier post](2024-06-27-two-useful-simple-counterexamples-of-string-coupling.md).

Regarding progress towards proving the conjecture, I haven’t even proven it for the special case of n=2 and |Sigma|=2. (This should be possible by doing enough case analysis, but it becomes unwieldy quickly.)

## Exploratory experiments

Since it is hard to either prove the conjecture, even in special cases, as well as hard to provide a counterexample establishing the necessity of the non-crossing condition, I resorted to computational experiments.

Given the probability distributions for X and Y, the existence of an NCFO coupling can be determined using linear programming. So this naturally suggests a Monte Carlo approach: generate a random probability distribution for each of X and Y, then check whether an NCFO coupling exists. By doing many trials, we hope to find a counterexample, if one exists.

Here is the table of results, with 100 trials for each case.

| n | \|Sigma\| | F | Failure rate |
| --- | --- | --- | --- |
| 2 | 2 | `{{0}, {1}, {0,1}}` | 0% |
| 3 | 2 | `{{0}, {1}, {0,1}, {2}, {0,1,2}}` | 0% |
| 3 | 2 | `{{0,1}, {0,2}}` | 41% |
| 2 | 3 | `{{0}, {1}, {0,1}}` | 0% |
| 4 | 2 | `{{0}, {1}, {0,1}, {2}, {3}, {2,3}, {0,1,2,3}}` | 0% |
| 4 | 2 | `{{0}, {1}, {0,1}, {2}, {0,1,2}, {3}, {0,1,2,3}}` | 0% |
| 2 | 4 | `{{0}, {1}, {0,1}}` | 0% |
| 4 | 2 | `{{0,1,2}, {2,3}}` | 57% |

Observe that both cases where F is crossing fail, whereas no failure is observed for non-crossing F. Also, note that one n=4 case is included where the structure of F is of a complete binary tree, rather than prefixes. Even with that structure, an optimal coupling is always found.

---
title: "Proof strategy for efficiency analysis of SMCBN"
date: 2024-10-10T22:56:12+00:00
modified: 2024-10-10T22:56:12+00:00
url: https://masharpe.wordpress.com/2024/10/10/proof-strategy-for-efficiency-analysis-of-smcbn/
tags: ["algorithm", "coupling", "proof", "research", "sampling"]
categories: ["Uncategorized"]
---

# Proof strategy for efficiency analysis of SMCBN

In moving towards writing a rough draft of a preprint for simultaneously maximal coupling of Bayesian networks (SMCBN), the only large remaining piece is the efficiency analysis: in particular, how many samples are drawn from the given marginal distributions? Before, [we’ve analyzed the efficiency of MRC in isolation](2024-10-05-more-proofs-of-properties-of-the-maximal-recoupling-algorithm.md), and SMCBN increases the difficulty by nesting many calls to MRC interleaved with other subroutines.

To ease analysis, we’ll make a minor alteration to [the SMCBN pseudocode presented previously](2024-10-08-full-pseudocode-for-sampling-from-a-simultaneous-maximal-coupling-of-bayesian-networks.md). In that post, BuildJoint applied to Leaf used the classic maximal coupling (CMC) algorithm. But we’ve noted before that [MRC generalizes CMC](2024-10-01-key-subroutine-for-simultaneously-maximal-coupling.md), so we can rewrite that case of BuildJoint to use MRC instead of CMC:

```
BuildJoint(Leaf mX mY):
    1. j <- Trivial(mX, mY)
    2. Return MaximalRecoupling(j)

Trivial : Marginal E -> Marginal E -> Joint E

Trivial(mX, mY) =
    LX(x) = mX.L(x)
    LY(y) = mY.L(y)
    sampX():
        1. Return mX.samp()
    sampY|X(_):
        1. Return mY.samp()
```

Now we’re ready to begin the analysis. Due to its complexity, I haven’t filled in the details yet, so this post just presents a proof strategy.

The key question: how many of each leaf sampling operation is expected during one call of Sample? (TODO: ChainRule also does sampling, so it requires its own analysis, which I haven’t begun yet.)

Fix one leaf.

## mX.samp

First, the easy one: mX.samp.

**Claim.** mX.samp is invoked exactly once.

**Proof sketch.** Observe it’s only called during recursive invocation of sampX. This happens exactly once, in step 2 of Sample. **[]**

## mY.samp

**Claim.** The expected number of calls to mY.samp is at most 1.

**Proof strategy.**

Consider the call stack when mY.samp is called on this leaf. For some k that is the same for every invocation, the call stack will be:

```
MRC^1, Build^1, MRC^2, Build^2, ..., MRC^k, Build^k
```

where, for 1 <= i <= k-1, “Build^i” is either TensorProduct or ChainRule, and “Build^k” is Trivial.

For 1 <= i <= k, use `[-]^i` to refer to the equivalence class mapping used by MRC^i.

We’ll use mutual induction to prove, for every 1 <= i <= k,

- For each `[x]^i`, `E[calls of MRC^i.sampY|X([x]^i)] <= P[[X]^i = [x]^i]`.
- For each `[x]^i`, `E[calls of Build^i.sampY|X([x]^i)] <= P[[X]^i = [x]^i]`.

Once we have proven that, we will know that, for all `[x]^k`,

```
E[calls of Build^k.sampY|X([x]^k)] <= P[[X]^k = [x]^k]
```

So,

```
E[calls of mY.samp]
    = E[calls of Trivial.sampY|X]
    = sum_{[x]^k} E[calls of Trivial.sampY|X([x]^k)]
    = sum_{[x]^k} E[calls of Build^k.sampY|X([x]^k)]
    <= sum_{[x]^k} P[[X]^k = [x]^k]
    = 1
```

which is the claim.

Thus it’s enough to work through the induction. We need: a base case for MRC^1; an inductive step from MRC^i to Build^i; and an inductive step from Build^i to MRC^{i+1}.

### Base case (MRC^1)

We must show

```
forall [x]^1, E[calls of MRC^1.sampY|X([x]^1)] <= P[[X]^1 = [x]^1]
<=> forall x, E[calls of MRC^1.sampY|X(x)] <= P[X = x]
```

which is obvious since this call only occurs in step 3 of Sample. (In fact, the inequality holds with equality.)

### Inductive step from MRC^i to Build^i

Note: This is the part with a TODO that makes the proof not complete.

Given 1 <= i <= k, we need to show that if, for each `[x]^i`,

```
E[calls of MRC^i.sampY|X([x]^i)] <= P[[X]^i = [x]^i]
```

holds, then, for each `[x]^i`,

```
E[calls of Build^i.sampY|X([x]^i)] <= P[[X]^i = [x]^i]
```

The handwavy intuitive justification: if we call `MRC^i.sampY|X([x]^i)` exactly expected `P[[X]^i = [x]^i]` times, that’s the same as just running `MRC^i` (to sample both X and Y), which [we have seen previously](2024-10-05-more-proofs-of-properties-of-the-maximal-recoupling-algorithm.md) makes at most `P[[X]^i = [x]^i]` expected calls to `Build^i.sampY|X([x]^i)`. And obviously if the inequality is instead strict, so there are fewer calls to `MRC^i.sampY|X`, that can only reduce the number of calls to `Build^i.sampY|X`.

### Inductive step from Build^i to MRC^{i+1}

Take 1 <= i <= k-1.

This part is thankfully easier, since Build^i is either TensorProduct or ChainRule, and both of those make exactly one subcall per call.

We need to show that if, for each `[x]^i`,

```
E[calls of Build^i.sampY|X([x]^i)] <= P[[X]^i = [x]^i]
```

holds, then, for each `[x]^{i+1}`,

```
E[calls of MRC^{i+1}.sampY|X([x]^{i+1}) <= P[[X]^{i+1} = [x]^{i+1}]
```

To see this, for each `[x]^{i+1}`, observe:

```
E[calls of MRC^{i+1}.sampY|X([x]^{i+1})
    = sum_{[x']^i s.t. [x']^{i+1} = [x]^{i+1}} E[calls of Build^i.sampY|X([x']^i)]
    <= sum_{[x']^i s.t. [x']^{i+1} = [x]^{i+1}} P[[X]^i = [x']^i]
    = P[[X]^{i+1} = [x]^{i+1}]
```

as needed.

# Implementation: MRC and SMC-CPT

A small pure-Python implementation of the algorithms in
[`../auto-paper`](../auto-paper). Maximal recoupling (MRC) is Algorithm 2 of the
paper. SMC-CPT, simultaneously maximal coupling on chain-product trees, is in
Section 5. The implementation comes with tests against exact computations and
demos on toy distributions.

## Layout

- `smccpt/core.py`: oracles (`Marginal`, `Conditional`), the joint constructions
  (`Independent`, `Tensor`, `ChainRule`, `MRC`), CPT nodes (`Leaf`, `Product`,
  `Chain`) and the `SMCCPT` sampler. The core needs no dependencies.
- `smccpt/exact.py`: exact computation of MRC and SMC-CPT couplings by linear
  algebra on small finite examples, used as ground truth (needs numpy).
- `smccpt/baselines.py`: per-variable/per-token coupling (PTOC), per-coordinate
  maximal coupling, and classic maximal coupling of whole vectors.
- `tests/test_smccpt.py`: 89 tests (`python -m pytest -q`, needs numpy and pytest).
  They check that:
  - the exact SMC-CPT coupling has the right marginals and is maximal on every
    node scope, over random trees;
  - MRC of the independent coupling is classic maximal coupling, and MRC
    preserves a maximal coarsening;
  - the sampler's empirical distribution matches the exact coupling (21
    Monte Carlo tests with tolerance twice the expected sampling error);
  - the oracle-call bounds of the paper's SMC-CPT theorem hold;
  - on chains, SMC-CPT equals the APOC recursion.

  As a check that the tests can fail, a mutant that restarts MRC's walk from
  the input instead of walking fails 16 of them.
- `demos/run_demos.py`: writes [`demos/results.md`](demos/results.md).

## Usage

```python
import random
from smccpt import SMCCPT, Leaf, Product, Chain, categorical, conditional_categorical

# Two independent positions, then a third that depends on both.
tree = Chain(
    Product(Leaf("p1", categorical({"a": .6, "b": .4}), categorical({"a": .5, "b": .5})),
            Leaf("p2", categorical({"a": .3, "b": .7}), categorical({"a": .4, "b": .6}))),
    "p3",
    conditional_categorical(lambda h: {"a": .9, "b": .1} if h == ("a", "a") else {"a": .2, "b": .8}),
    conditional_categorical(lambda h: {"a": .8, "b": .2} if h == ("a", "a") else {"a": .3, "b": .7}),
)
x, y = SMCCPT(tree).sample(random.Random(0))
```

`x` is distributed as the X-model and `y` as the Y-model. Simultaneously,
`{p1}`, `{p2}`, `{p1,p2}` and `{p1,p2,p3}` are each maximally coupled. For
speculative-decoding-style use, `SMCCPT(tree).sample_y_given_x(rng, x)` takes a
given draw `x` from the X-model.

## Demo results (summary)

The full tables are in [`demos/results.md`](demos/results.md). In all three toys,
SMC-CPT attains the optimum agreement probability 1 − TV on every guaranteed
set, within Monte Carlo error. Each baseline is optimal on only some of the sets:

- **Independent coordinates (4 bits):** per-coordinate coupling is optimal on
  singletons only, and whole-vector CMC on the whole vector only. SMC-CPT is
  optimal on all 7 sets of the laminar family. For example, on the whole
  vector it achieves 0.431, against 0.188 for per-coordinate coupling.
- **Autoregressive bigram model (5 tokens):** SMC-CPT is optimal for every
  prefix. Per-token coupling (PTOC, as in speculative decoding) reaches 0.727
  on the full response, against the optimal 0.868.
- **Two-step masked-diffusion toy:** SMC-CPT is optimal on {p1}, {p2}, {p1,p2},
  {p1,p2,p3} and all four positions. PTOC gets 0.490 on all four, against the
  optimal 0.717.

Measured oracle costs match the paper's bounds. Each Y-side oracle and each
MRC loop is used about once per sample, which is the bound, attained with
equality in these examples.

## Caveats

- The code uses probabilities, not log-probabilities. That is fine for toys,
  but long sequences would underflow (see the paper's appendix).
- Likelihoods are recomputed rather than cached.
- Only finite distributions are supported.

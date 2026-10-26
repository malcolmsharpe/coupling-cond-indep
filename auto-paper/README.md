# Paper: maximal recoupling and simultaneously maximal coupling

`paper.tex` (compiled: `paper.pdf`) is a paper-style write-up of the 2024 research
archived in [`../blog-archive`](../blog-archive). It standardizes the notation
that changed across the notes, completes the proof sketches, and fixes the
errors found along the way. It is written mainly as a reference for LLMs, but it
is meant to be readable by people too.

It was written by Claude (Anthropic) from the notes, with proofs reviewed by
GPT-6 Astra (OpenAI, via Codex). The main claims were also checked numerically.
The "Provenance and status" section of the paper lists what was added or
corrected relative to the notes.

## Main results

- **Maximal recoupling (MRC).** A rejection sampler with the same shape as the
  classic maximal-coupling algorithm. It turns any coupling into a maximal one
  and preserves every coarsening that was already maximally coupled. It never
  lowers the agreement probability of any coarsening, and the total-variation
  change is at most twice the gain. It makes at most one expected call to the
  old coupling's conditional sampler. The paper also gives a closed form
  (pseudoinverse of a normalized flow matrix).
- **SMC-CPT.** Simultaneously maximal coupling on chain-product trees, built by
  applying MRC at every node, with each Y-side oracle called at most once in
  expectation.
- **Characterizations.** Families that can be simultaneously maximally coupled
  for all distributions are exactly the chains (no assumptions), the laminar
  families (independent coordinates), and the laminar families whose disjoint
  members have disjoint ancestor sets (Bayesian networks).
- **The autoregressive case.** SMC-CPT reproduces the all-prefix-optimal coupling
  (APOC). Per-token optimal coupling dominates seed reuse prefix by prefix.

## Building

```
latexmk -pdf paper.tex
```

Uses only standard TeX Live packages. The bibliography is inline, so no biber
is needed.

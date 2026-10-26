# Blog archive

An archive of the posts on coupling from Malcolm Sharpe's blog,
[masharpe.wordpress.com](https://masharpe.wordpress.com/), written between
February and October 2024. The research started with comparing LLM quantizations
by coupling their responses. It ended with maximal recoupling and simultaneously
maximal coupling under conditional independence constraints.

The blog isn't indexed by search engines. This archive exists so that the
material is available in one place.

## Layout

- `posts/`: one Markdown file per post, named `YYYY-MM-DD-slug.md`, with YAML
  front matter (title, dates, original URL, tags). Links between archived posts
  are rewritten as relative links. [`posts/INDEX.md`](posts/INDEX.md) lists
  every post, newest first.
- `html/`: the original HTML content of each post, unmodified, as returned by the
  WordPress.com API. Use it if the Markdown conversion looks wrong.
- `media/`: full-resolution copies of the images embedded in posts.
- `tex/`: LaTeX sources for the three PDFs that were attached to posts:
  - `mrc_ref_2024_10_15/`: "Maximal recoupling" rough draft, attached to
    [MRC reference (rough draft)](posts/2024-10-14-mrc-reference-rough-draft.md).
    This is the version that was posted. Compiling it reproduces the posted PDF.
  - `mrc_ref_2024_10_18/`: a later, unposted revision of the same draft. It adds
    algorithm environments and a first appendix proof.
  - `coupling_example/`: attached to
    [Writing practice: coupling example](posts/2024-09-03-writing-practice-coupling-example.md).
  - `ptcrn_le_ptoc/`: attached to
    [Writing practice: PTCRN <= PTOC](posts/2024-09-04-writing-practice-ptcrn-ptoc.md).

  The PDFs themselves are not archived. The two writing-practice PDFs are
  byte-identical to builds of these sources.
- `tools/`: the script that built the archive, and the list of posts it archives.

## Which posts are included

`tools/post_list.txt` has the 66 posts the author listed as the coupling
research notes. Four related posts are also included and marked `extra` in the
index: *Sampling from SEDD*, *Factoring out a continuous random variable from an
LLM response distribution*, *Continuous variants of truncation samplers*, and
*Which proprietary LLM API providers support seed for reproducibility*. None of
the archived posts had comments.

## Reading guide

Terminology and notation changed over time, and some early posts contain
mistakes that later posts corrected. Prefer the later posts. For a consolidated
and corrected treatment, see [`../auto-paper`](../auto-paper).

Rough phases:

1. **Feb–Aug 2024: coupling two LLM response distributions.** Per-token optimal
   coupling (PTOC, as in speculative decoding) versus all-prefix-optimal coupling
   (APOC), seed reuse (PTCRN), experiments on quantized models, and simple
   counterexamples. APOC turned out to be known: as greedy block verification
   (Sun et al. 2024) and, earlier, as maximal agreement couplings (Völlering 2016).
2. **Sep 2024: simultaneously maximal coupling with independence.** The
   non-crossing-family (NCFOC) conjecture, the crossing counterexample, the
   SMC-BN conjecture, and an LP/exchange-argument existence proof.
3. **Oct 2024: maximal recoupling (MRC) and the SMC-BN algorithm.** The MRC
   algorithm and the proofs of its properties, the closed form, full pseudocode
   for SMC-BN (later called SMC-CPT, for chain-product trees), and the efficiency
   analysis.
4. **Oct 2024: plans for the preprint.** "Approach for writing recent results",
   "Organizing MRC properties", and "Structuring the coupling preprint".

## Rebuilding

```
pip install requests beautifulsoup4 markdownify
python tools/build_archive.py . tools/post_list.txt
```

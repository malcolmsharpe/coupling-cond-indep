"""Tests: exact properties of MRC/SMC-CPT, and agreement of the sampler with the exact coupling.

Run from auto-impl/:  python -m pytest -q
"""

import itertools
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smccpt import (  # noqa: E402
    SMCCPT,
    Chain,
    Counter,
    Leaf,
    Product,
    categorical,
    conditional_categorical,
    node_scopes,
    scope,
)
from smccpt.exact import (  # noqa: E402
    agreement,
    is_maximal,
    marginals,
    max_agreement,
    mrc_exact,
    project,
    smc_cpt_exact,
)


def rand_dist(rng, values, zero_prob=0.3):
    w = [rng.random() if rng.random() > zero_prob else 0.0 for _ in values]
    if sum(w) == 0:
        w[rng.randrange(len(w))] = 1.0
    s = sum(w)
    return {v: wi / s for v, wi in zip(values, w)}


def rand_cond(rng, values):
    cache = {}

    def table(h):
        if h not in cache:
            cache[h] = rand_dist(rng, values)
        return cache[h]

    return conditional_categorical(table)


def rand_tree(rng, shape, alphabet):
    """shape: nested tuples. 'v' = leaf, ('P', a, b) = product, ('C', a) = chain."""
    counter = itertools.count()

    def rec(s):
        if s == "v":
            return Leaf(f"v{next(counter)}", categorical(rand_dist(rng, alphabet)), categorical(rand_dist(rng, alphabet)))
        if s[0] == "P":
            return Product(rec(s[1]), rec(s[2]))
        return Chain(rec(s[1]), f"v{next(counter)}", rand_cond(rng, alphabet), rand_cond(rng, alphabet))

    return rec(shape)


SHAPES = [
    "v",
    ("C", "v"),
    ("P", "v", "v"),
    ("C", ("P", "v", "v")),
    ("P", ("C", "v"), "v"),
    ("C", ("C", ("C", "v"))),
    ("P", ("P", "v", "v"), ("C", "v")),
]


def check_scopes_maximal(tree, P):
    vars_ = scope(tree)
    for S in node_scopes(tree):
        sub = project(P, [vars_.index(v) for v in S])
        assert is_maximal(sub), S


@pytest.mark.parametrize("seed", range(40))
def test_exact_coupling_properties(seed):
    rng = random.Random(seed)
    tree = rand_tree(rng, SHAPES[seed % len(SHAPES)], alphabet=["a", "b", "c"][: 2 + seed % 2])
    alph = {v: ["a", "b", "c"][: 2 + seed % 2] for v in scope(tree)}
    P = smc_cpt_exact(tree, alph)
    mx, my = marginals(P)
    # Marginals are the CPT's X and Y distributions.
    for x, p in mx.items():
        assert abs(p - SMCCPT(tree).joint.LX(x)) < 1e-12
    for y, p in my.items():
        assert abs(p - SMCCPT(tree).joint.LY(y)) < 1e-12
    check_scopes_maximal(tree, P)


def test_mrc_of_independent_is_cmc():
    rng = random.Random(1)
    for _ in range(50):
        px = rand_dist(rng, range(5))
        py = rand_dist(rng, range(5))
        P = {((a,), (b,)): px[a] * py[b] for a in px for b in py if px[a] * py[b] > 0}
        Q = mrc_exact(P)
        D = sum(max(0, px[a] - py[a]) for a in px)
        for a in px:
            for b in py:
                exp = min(px[a], py[a]) if a == b else (max(0, px[a] - py[a]) * max(0, py[b] - px[b]) / D if D else 0)
                assert abs(Q.get(((a,), (b,)), 0.0) - exp) < 1e-12


def test_mrc_preserves_maximal_coarsening():
    rng = random.Random(2)
    for _ in range(100):
        # Coarse classes {0,1}, {2,3}, {4,5}; coarse flow only from class 0 to class 2 -> coarse-maximal.
        P = {}
        for S in [(0, 1), (2, 3), (4, 5)]:
            for a in S:
                for b in S:
                    P[((a,), (b,))] = rng.random()
        for a in (0, 1):
            for b in (4, 5):
                P[((a,), (b,))] = rng.random() * 0.5
        tot = sum(P.values())
        P = {k: v / tot for k, v in P.items()}
        Q = mrc_exact(P)
        f = lambda k: (k[0] // 2,)  # noqa: E731
        coarse = lambda M: {(fa, fb): sum(p for (a, b), p in M.items() if (f(a), f(b)) == (fa, fb)) for fa in [(0,), (1,), (2,)] for fb in [(0,), (1,), (2,)]}  # noqa: E731
        cP, cQ = coarse(P), coarse(Q)
        assert all(abs(cP[k] - cQ[k]) < 1e-10 for k in cP)
        assert is_maximal(Q)


@pytest.mark.parametrize("shape_idx", range(len(SHAPES)))
@pytest.mark.parametrize("seed", range(3))
def test_sampler_matches_exact(shape_idx, seed):
    rng = random.Random(1000 * seed + shape_idx)
    alphabet = ["a", "b", "c"]
    tree = rand_tree(rng, SHAPES[shape_idx], alphabet)
    P = smc_cpt_exact(tree, {v: alphabet for v in scope(tree)})
    smc = SMCCPT(tree)
    N = 60000
    counts = {}
    for _ in range(N):
        x, y = smc.sample(rng)
        k = (tuple(x.values()), tuple(y.values()))
        counts[k] = counts.get(k, 0) + 1
    tv = 0.5 * sum(abs(counts.get(k, 0) / N - P.get(k, 0.0)) for k in set(counts) | set(P))
    # Expected sampling TV is about 0.5 * sum_k sqrt(2 p_k (1 - p_k) / (pi N)); allow twice that.
    expected = 0.5 * sum(np.sqrt(2 * p * (1 - p) / (np.pi * N)) for p in P.values())
    assert tv < 2 * expected + 0.002, (tv, expected)


@pytest.mark.parametrize("shape", SHAPES[1:])
def test_oracle_call_bounds(shape):
    """Theorem 5.3(c): X-side samplers once; Y-side samplers and MRC loops <= 1 in expectation."""
    rng = random.Random(7)
    tree = rand_tree(rng, shape, ["a", "b", "c"])
    counter = Counter()
    smc = SMCCPT(tree, counter)
    N = 20000
    for _ in range(N):
        smc.sample(rng)
    for (kind, name), c in counter.counts.items():
        mean = c / N
        if kind == "X":
            assert mean == 1.0
        else:  # Y-side sampler calls, MRC invocations, MRC loop iterations: each <= 1 in expectation
            assert mean < 1.0 + 4 * np.sqrt(3.0 / N) + 0.02, (kind, name, mean)


def apoc_exact(px_list, Pprev, kx, ky, alphabet):
    """One step of the APOC recursion (paper, Section 7) on dict couplings."""
    pX1, pY1 = marginals(Pprev)
    pX = {x + (a,): pX1[x] * kx(x)[a] for x in pX1 for a in alphabet}
    pY = {y + (b,): pY1[y] * ky(y)[b] for y in pY1 for b in alphabet}
    keys = set(pX) | set(pY)
    rX = {k: max(0.0, pX.get(k, 0) - pY.get(k, 0)) for k in keys}
    rY = {k: max(0.0, pY.get(k, 0) - pX.get(k, 0)) for k in keys}
    nX = lambda h: sum(rX.get(h + (z,), 0) for z in alphabet)  # noqa: E731
    nY = lambda h: sum(rY.get(h + (z,), 0) for z in alphabet)  # noqa: E731
    out = {}
    for k in keys:
        m = min(pX.get(k, 0), pY.get(k, 0))
        if m > 0:
            out[(k, k)] = m
    for (x1, y1), p in Pprev.items():
        if x1 == y1:
            mass = p - sum(min(pX.get(x1 + (z,), 0), pY.get(x1 + (z,), 0)) for z in alphabet)
        else:
            mass = p
        if mass <= 1e-15:
            continue
        for a in alphabet:
            for b in alphabet:
                q = mass * rX.get(x1 + (a,), 0) / nX(x1) * rY.get(y1 + (b,), 0) / nY(y1)
                if q > 0:
                    out[(x1 + (a,), y1 + (b,))] = out.get((x1 + (a,), y1 + (b,)), 0) + q
    return out


@pytest.mark.parametrize("seed", range(20))
def test_autoregressive_equals_apoc(seed):
    rng = random.Random(100 + seed)
    alphabet = ["a", "b", "c"]
    tree = rand_tree(rng, ("C", ("C", ("C", "v"))), alphabet)
    # Walk down to the leaf, then rebuild APOC step by step.
    chain = []
    t = tree
    while isinstance(t, Chain):
        chain.append(t)
        t = t.child
    leaf = t
    Pa = smc_cpt_exact(leaf, {leaf.var: alphabet})
    for c in reversed(chain):
        kx = lambda h, c=c: {a: c.cX.L(h, a) for a in alphabet}  # noqa: E731
        ky = lambda h, c=c: {b: c.cY.L(h, b) for b in alphabet}  # noqa: E731
        Pa = apoc_exact(None, Pa, kx, ky, alphabet)
    P = smc_cpt_exact(tree, {v: alphabet for v in scope(tree)})
    assert max(abs(P.get(k, 0) - Pa.get(k, 0)) for k in set(P) | set(Pa)) < 1e-12
    # And every prefix is maximally coupled.
    vars_ = scope(tree)
    for i in range(1, len(vars_) + 1):
        sub = project(P, list(range(i)))
        assert abs(agreement(sub) - max_agreement(*marginals(sub))) < 1e-12

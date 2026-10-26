"""Toy demonstrations of SMC-CPT against baseline couplings.

For each toy pair of distributions (X, Y) and each set S that SMC-CPT is supposed to
couple maximally, report the Monte Carlo agreement probability P[X_S = Y_S] of each
method next to the optimum 1 - TV(X_S, Y_S), computed exactly by enumeration.

Run from auto-impl/:  python demos/run_demos.py  (writes demos/results.md)
"""

import itertools
import random
import sys
from pathlib import Path

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
from smccpt.baselines import independent_per_variable, per_variable, whole_cmc  # noqa: E402

N = 100_000
OUT = []


def enumerate_joint(tree, alphabet):
    """Exact distributions of X and Y (dicts over full tuples) by enumeration."""
    smc = SMCCPT(tree)
    vals = list(itertools.product(alphabet, repeat=len(scope(tree))))
    px = {v: smc.joint.LX(v) for v in vals}
    py = {v: smc.joint.LY(v) for v in vals}
    return px, py


def optimum(px, py, idx):
    mx, my = {}, {}
    for v, p in px.items():
        k = tuple(v[i] for i in idx)
        mx[k] = mx.get(k, 0) + p
    for v, p in py.items():
        k = tuple(v[i] for i in idx)
        my[k] = my.get(k, 0) + p
    return sum(min(mx.get(k, 0), my.get(k, 0)) for k in set(mx) | set(my))


def run(name, description, tree, alphabet, methods, sets=None):
    rng = random.Random(0)
    vars_ = scope(tree)
    sets = sets or node_scopes(tree)
    px, py = enumerate_joint(tree, alphabet)
    idxs = [[vars_.index(v) for v in S] for S in sets]
    opt = [optimum(px, py, idx) for idx in idxs]
    results = {}
    costs = None
    for mname, sampler in methods.items():
        hits = [0] * len(sets)
        counter = Counter() if mname == "SMC-CPT" else None
        if mname == "SMC-CPT":
            smc = SMCCPT(tree, counter)
            sampler = lambda rng: tuple(tuple(d.values()) for d in smc.sample(rng))  # noqa: E731
        sq = {}
        for _ in range(N):
            before = dict(counter.counts) if counter else None
            x, y = sampler(rng)
            for j, idx in enumerate(idxs):
                hits[j] += all(x[i] == y[i] for i in idx)
            if counter:  # per-sample squared counts, for standard errors of the mean costs
                for k, v in counter.counts.items():
                    d = v - before.get(k, 0)
                    sq[k] = sq.get(k, 0) + d * d
        results[mname] = [h / N for h in hits]
        if counter:
            costs = {k: (v / N, ((sq[k] / N - (v / N) ** 2) / N) ** 0.5) for k, v in counter.counts.items()}
    se = 0.5 / N**0.5
    OUT.append(f"## {name}\n\n{description}\n")
    header = "| set S | optimum 1-TV | " + " | ".join(results) + " |"
    OUT.append(header)
    OUT.append("|" + "---|" * (2 + len(results)))
    for j, S in enumerate(sets):
        cells = []
        for m in results:
            v = results[m][j]
            mark = "" if v > opt[j] - 4 * se else " ✗"
            cells.append(f"{v:.3f}{mark}")
        OUT.append(f"| {{{','.join(S)}}} | {opt[j]:.3f} | " + " | ".join(cells) + " |")
    OUT.append(f"\n(Monte Carlo, N = {N:,}; standard error ≤ {se:.4f}. ✗ marks a value more than 4 standard errors below the optimum.)\n")
    if costs:
        fmt = lambda c: f"{c[0]:.3f} ± {c[1]:.3f}" if c else "—"  # noqa: E731
        ys = {k[1]: c for k, c in costs.items() if k[0] == "Y"}
        loops = {k[1]: c for k, c in costs.items() if k[0] == "loop"}
        OUT.append(
            "SMC-CPT mean oracle cost per sample, ± one standard error. The paper's bound is at most 1 in "
            "expectation for each entry, with equality when every value can reach a sink, as here. "
            "Product nodes make no Y-side draws of their own.\n"
        )
        OUT.append("| node scope | Y-side oracle draws | MRC loop iterations |")
        OUT.append("|---|---|---|")
        for S in sets:
            k = tuple(S)
            OUT.append(f"| {{{','.join(S)}}} | {fmt(ys.get(k))} | {fmt(loops.get(k))} |")
        OUT.append("")


def demo_independent():
    pX = [0.8, 0.6, 0.7, 0.3]
    pY = [0.4, 0.5, 0.2, 0.6]
    leaves = [Leaf(f"x{i+1}", categorical({1: pX[i], 0: 1 - pX[i]}), categorical({1: pY[i], 0: 1 - pY[i]})) for i in range(4)]
    tree = Product(Product(leaves[0], leaves[1]), Product(leaves[2], leaves[3]))
    px, py = enumerate_joint(tree, [0, 1])
    methods = {
        "SMC-CPT": None,
        "per-coordinate maximal": lambda rng: independent_per_variable([l.mX for l in leaves], [l.mY for l in leaves], rng),
        "whole-vector CMC": lambda rng: whole_cmc(px, py, rng),
        "per-token (PTOC)": lambda rng: per_variable(tree, rng),
    }
    run(
        "1. Independent coordinates",
        "Four independent biased bits on each side, P[X_i=1] = (0.8, 0.6, 0.7, 0.3), "
        "P[Y_i=1] = (0.4, 0.5, 0.2, 0.6). CPT: product of products, so the laminar family "
        "{x1},{x2},{x1,x2},{x3},{x4},{x3,x4},{x1..x4} is guaranteed (paper: theorem \"independent coordinates\"). "
        "Per-coordinate coupling is optimal on singletons only; whole-vector CMC is optimal on the whole vector only.",
        tree,
        [0, 1],
        methods,
    )


def bigram(temp_shift):
    """A 3-letter bigram 'language model'; temp_shift perturbs it (as a stand-in for a quantized model)."""
    base = {
        None: [0.5, 0.3, 0.2],
        "a": [0.2, 0.5, 0.3],
        "b": [0.6, 0.1, 0.3],
        "c": [0.3, 0.3, 0.4],
    }

    def dist(prev):
        w = [p ** (1 / (1 + temp_shift)) for p in base[prev]]
        s = sum(w)
        return {c: wi / s for c, wi in zip("abc", w)}

    return dist


def demo_autoregressive():
    dX, dY = bigram(0.0), bigram(0.6)
    t = Leaf("t1", categorical(dX(None)), categorical(dY(None)))
    for i in range(2, 6):
        t = Chain(t, f"t{i}", conditional_categorical(lambda h: dX(h[-1])), conditional_categorical(lambda h: dY(h[-1])))
    px, py = enumerate_joint(t, list("abc"))
    methods = {
        "SMC-CPT": None,
        "per-token (PTOC)": lambda rng: per_variable(t, rng),
        "whole-response CMC": lambda rng: whole_cmc(px, py, rng),
    }
    run(
        "2. Autoregressive bigram model",
        "Responses of 5 tokens from a 3-letter bigram model X and a flattened copy Y (exponent 1/1.6 on the "
        "probabilities, then renormalized). CPT: a chain, so every prefix is guaranteed; SMC-CPT coincides "
        "with APOC (paper: theorem \"SMC-CPT reproduces APOC\"). PTOC is the coupling of standard speculative decoding.",
        t,
        list("abc"),
        methods,
    )


def demo_diffusion():
    """Two-step 'masked diffusion' toy: step 1 unmasks positions 1, 2 independently; step 2 unmasks 3, 4
    conditionally independently given positions 1, 2."""
    p1X, p1Y = {"a": 0.6, "b": 0.4}, {"a": 0.45, "b": 0.55}
    p2X, p2Y = {"a": 0.3, "b": 0.7}, {"a": 0.5, "b": 0.5}

    def step2(bias):
        def table(h):
            agree = h[0] == h[1]
            p = 0.8 if agree else 0.35
            p = min(0.95, max(0.05, p + bias))
            return {"a": p, "b": 1 - p} if h[0] == "a" else {"a": 1 - p, "b": p}

        return table

    t = Product(Leaf("p1", categorical(p1X), categorical(p1Y)), Leaf("p2", categorical(p2X), categorical(p2Y)))
    t = Chain(t, "p3", conditional_categorical(step2(0.0)), conditional_categorical(step2(-0.15)))
    # Position 4 depends on positions 1 and 2 only (conditionally independent of position 3 given them).
    t = Chain(
        t,
        "p4",
        conditional_categorical(lambda h: step2(0.05)(h[:2])),
        conditional_categorical(lambda h: step2(-0.1)(h[:2])),
    )
    px, py = enumerate_joint(t, ["a", "b"])
    methods = {
        "SMC-CPT": None,
        "per-token (PTOC)": lambda rng: per_variable(t, rng),
        "whole CMC": lambda rng: whole_cmc(px, py, rng),
    }
    run(
        "3. Two-step masked-diffusion toy",
        "Four positions. Step 1 unmasks p1, p2 independently; step 2 unmasks p3, p4 conditionally "
        "independently given (p1, p2). CPT: chain(chain(product(p1, p2), p3), p4). Guaranteed sets: "
        "{p1},{p2},{p1,p2},{p1,p2,p3},{p1..p4}. By the paper's Bayesian-network theorem, {p3} and {p4} cannot both be added "
        "in general (they share the ancestors p1, p2).",
        t,
        ["a", "b"],
        methods,
    )


if __name__ == "__main__":
    demo_independent()
    demo_autoregressive()
    demo_diffusion()
    text = "# Demo results\n\nGenerated by `demos/run_demos.py`.\n\n" + "\n".join(OUT)
    (Path(__file__).parent / "results.md").write_text(text)
    print(text)

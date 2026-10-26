"""Baseline couplings to compare SMC-CPT against.

- `per_variable`: couple variables one at a time in the CPT's scope order. While
  all earlier variables agree, the next pair is maximally coupled (classic maximal
  coupling of the two conditionals). After the first disagreement, the remaining
  Y-variables are sampled from their own conditionals independently. For
  autoregressive models this is per-token optimal coupling (PTOC), as in
  speculative decoding.
- `independent_per_variable`: for independent coordinates, maximally couple each
  coordinate separately and independently of the others.
- `whole_cmc`: classic maximal coupling of the two whole joint distributions,
  given exactly as dicts (only feasible for small examples).
"""

from __future__ import annotations

import random

from .core import Leaf, Node, Product, sample_x, scope


def cmc_cond(rng: random.Random, x, LX, LY, sampY):
    """Classic maximal coupling, conditional form (Algorithm 1 of the paper)."""
    if rng.random() * LX(x) < LY(x):
        return x
    while True:
        y = sampY()
        if rng.random() * LY(y) >= LX(y):
            return y


def _steps(t: Node, rng: random.Random):
    """For each variable in scope order, a function (x_prefix, y_prefix) -> (LX, LY, sampY)."""
    out = []

    def rec(t: Node, offset: int):
        if isinstance(t, Leaf):
            out.append(lambda xp, yp, t=t: (t.mX.L, t.mY.L, lambda: t.mY.samp(rng)))
        elif isinstance(t, Product):
            rec(t.left, offset)
            rec(t.right, offset + len(scope(t.left)))
        else:
            rec(t.child, offset)
            k = len(scope(t.child))
            out.append(
                lambda xp, yp, t=t, o=offset, k=k: (
                    lambda a: t.cX.L(xp[o : o + k], a),
                    lambda b: t.cY.L(yp[o : o + k], b),
                    lambda: t.cY.samp(rng, yp[o : o + k]),
                )
            )

    rec(t, 0)
    return out


def per_variable(t: Node, rng: random.Random) -> tuple[tuple, tuple]:
    """PTOC-style sequential coupling (see module docstring)."""
    x = sample_x(t, rng)
    y: list = []
    agree = True
    for i, step in enumerate(_steps(t, rng)):
        LX, LY, sampY = step(x[:i], tuple(y))
        yi = cmc_cond(rng, x[i], LX, LY, sampY) if agree else sampY()
        y.append(yi)
        agree = agree and yi == x[i]
    return x, tuple(y)


def independent_per_variable(marginals_x: list, marginals_y: list, rng: random.Random):
    """Independent coordinates: maximally couple each coordinate on its own."""
    x, y = [], []
    for mX, mY in zip(marginals_x, marginals_y):
        a = mX.samp(rng)
        x.append(a)
        y.append(cmc_cond(rng, a, mX.L, mY.L, lambda: mY.samp(rng)))
    return tuple(x), tuple(y)


def whole_cmc(px: dict, py: dict, rng: random.Random):
    """Classic maximal coupling of two explicitly given finite distributions."""
    xs, wx = zip(*[(k, v) for k, v in px.items() if v > 0])
    ys, wy = zip(*[(k, v) for k, v in py.items() if v > 0])
    x = rng.choices(xs, wx)[0]
    y = cmc_cond(rng, x, lambda a: px.get(a, 0.0), lambda b: py.get(b, 0.0), lambda: rng.choices(ys, wy)[0])
    return x, y

"""Maximal recoupling (MRC) and simultaneously maximal coupling on chain-product trees (SMC-CPT).

This follows the paper in ../auto-paper (Algorithm 2 and Section 5). A *joint* is an
object that can evaluate the two marginal likelihoods and sample Y given X; the
sampler for X is kept separately, since it is only ever needed once per sample.

Values of a CPT node are tuples, ordered as the node's scope (see `scope`).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Hashable, Sequence

Value = Hashable


# ---------------------------------------------------------------------------
# Oracles


@dataclass
class Marginal:
    """A distribution of one atomic variable: likelihood and sampler."""

    L: Callable[[Value], float]
    samp: Callable[[random.Random], Value]


@dataclass
class Conditional:
    """A conditional distribution of one variable given a history (a tuple).

    `L(history, value)` and `samp(rng, history)` must be defined for every history,
    including histories of probability zero (any fixed distribution will do there).
    """

    L: Callable[[tuple, Value], float]
    samp: Callable[[random.Random, tuple], Value]


def categorical(probs: dict) -> Marginal:
    """Marginal oracle for a finite distribution given as {value: probability}."""
    items = [(v, p) for v, p in probs.items() if p > 0]
    values = [v for v, _ in items]
    weights = [p for _, p in items]
    return Marginal(L=lambda v: probs.get(v, 0.0), samp=lambda rng: rng.choices(values, weights)[0])


def conditional_categorical(table: Callable[[tuple], dict]) -> Conditional:
    """Conditional oracle from a function mapping a history to {value: probability}."""
    return Conditional(
        L=lambda h, v: table(h).get(v, 0.0),
        samp=lambda rng, h: categorical(table(h)).samp(rng),
    )


# ---------------------------------------------------------------------------
# Call counting (used by tests to check the efficiency bounds)


@dataclass
class Counter:
    counts: dict = field(default_factory=dict)

    def tick(self, key) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1


# ---------------------------------------------------------------------------
# Joints


class Joint:
    """Interface: LX, LY (marginal likelihoods of the joint's scope) and sampYgivenX."""

    def LX(self, x: tuple) -> float:
        raise NotImplementedError

    def LY(self, y: tuple) -> float:
        raise NotImplementedError

    def sampYgivenX(self, rng: random.Random, x: tuple) -> tuple:
        raise NotImplementedError


class Independent(Joint):
    """The independent coupling of two one-variable marginals (a leaf, before recoupling)."""

    def __init__(self, mX: Marginal, mY: Marginal, counter: Counter | None, name):
        self.mX, self.mY, self.counter, self.name = mX, mY, counter, name

    def LX(self, x):
        return self.mX.L(x[0])

    def LY(self, y):
        return self.mY.L(y[0])

    def sampYgivenX(self, rng, x):
        if self.counter:
            self.counter.tick(("Y", self.name))
        return (self.mY.samp(rng),)


class Tensor(Joint):
    """Independent combination J1 (x) J2 of the couplings of two independent scopes."""

    def __init__(self, j1: Joint, j2: Joint, k1: int):
        self.j1, self.j2, self.k1 = j1, j2, k1  # k1 = size of j1's scope

    def LX(self, x):
        a = self.j1.LX(x[: self.k1])
        return 0.0 if a == 0 else a * self.j2.LX(x[self.k1 :])

    def LY(self, y):
        a = self.j1.LY(y[: self.k1])
        return 0.0 if a == 0 else a * self.j2.LY(y[self.k1 :])

    def sampYgivenX(self, rng, x):
        return self.j1.sampYgivenX(rng, x[: self.k1]) + self.j2.sampYgivenX(rng, x[self.k1 :])


class ChainRule(Joint):
    """J |x (K_X, K_Y): extend a coupling by one variable following each side's own conditional."""

    def __init__(self, j: Joint, cX: Conditional, cY: Conditional, counter: Counter | None, name):
        self.j, self.cX, self.cY, self.counter, self.name = j, cX, cY, counter, name

    def LX(self, x):
        a = self.j.LX(x[:-1])
        return 0.0 if a == 0 else a * self.cX.L(x[:-1], x[-1])

    def LY(self, y):
        a = self.j.LY(y[:-1])
        return 0.0 if a == 0 else a * self.cY.L(y[:-1], y[-1])

    def sampYgivenX(self, rng, x):
        y1 = self.j.sampYgivenX(rng, x[:-1])
        if self.counter:
            self.counter.tick(("Y", self.name))
        return y1 + (self.cY.samp(rng, y1),)


class MRC(Joint):
    """Maximal recoupling of a joint (Algorithm 2 of the paper)."""

    def __init__(self, j: Joint, counter: Counter | None = None, name=None):
        self.j, self.counter, self.name = j, counter, name

    def LX(self, x):
        return self.j.LX(x)

    def LY(self, y):
        return self.j.LY(y)

    def sampYgivenX(self, rng, x):
        if self.counter:
            self.counter.tick(("MRC", self.name))
        px, py = self.j.LX(x), self.j.LY(x)
        if rng.random() * px < py:  # with probability min{1, pY(x)/pX(x)}
            return x
        v = x
        while True:
            if self.counter:
                self.counter.tick(("loop", self.name))
            w = self.j.sampYgivenX(rng, v)
            if rng.random() * self.j.LY(w) < self.j.LX(w):  # with probability min{1, pX(w)/pY(w)}
                v = w
                continue
            return w


# ---------------------------------------------------------------------------
# Chain-product trees


@dataclass
class Leaf:
    var: str
    mX: Marginal
    mY: Marginal


@dataclass
class Product:
    left: "Node"
    right: "Node"


@dataclass
class Chain:
    child: "Node"
    var: str
    cX: Conditional  # history = values of child's scope, in child's scope order
    cY: Conditional


Node = Leaf | Product | Chain


def scope(t: Node) -> list[str]:
    if isinstance(t, Leaf):
        return [t.var]
    if isinstance(t, Product):
        return scope(t.left) + scope(t.right)
    return scope(t.child) + [t.var]


def build(t: Node, counter: Counter | None = None) -> Joint:
    """The (conditional sampler of the) SMC-CPT coupling for the tree t."""
    name = tuple(scope(t))
    if isinstance(t, Leaf):
        return MRC(Independent(t.mX, t.mY, counter, name), counter, name)
    if isinstance(t, Product):
        j = Tensor(build(t.left, counter), build(t.right, counter), len(scope(t.left)))
        return MRC(j, counter, name)
    return MRC(ChainRule(build(t.child, counter), t.cX, t.cY, counter, name), counter, name)


def sample_x(t: Node, rng: random.Random, counter: Counter | None = None) -> tuple:
    """Ancestral sampling of X along the tree (one call to each X-side sampler)."""
    if isinstance(t, Leaf):
        if counter:
            counter.tick(("X", (t.var,)))
        return (t.mX.samp(rng),)
    if isinstance(t, Product):
        return sample_x(t.left, rng, counter) + sample_x(t.right, rng, counter)
    h = sample_x(t.child, rng, counter)
    if counter:
        counter.tick(("X", tuple(scope(t))))
    return h + (t.cX.samp(rng, h),)


def likelihood_x(t: Node, x: tuple) -> float:
    return build(t).LX(x)


class SMCCPT:
    """Sampler for the simultaneously maximal coupling of a CPT."""

    def __init__(self, tree: Node, counter: Counter | None = None):
        self.tree, self.counter = tree, counter
        self.joint = build(tree, counter)
        self.vars = scope(tree)

    def sample(self, rng: random.Random) -> tuple[dict, dict]:
        x = sample_x(self.tree, rng, self.counter)
        y = self.joint.sampYgivenX(rng, x)
        return dict(zip(self.vars, x)), dict(zip(self.vars, y))

    def sample_y_given_x(self, rng: random.Random, x: dict) -> dict:
        """Conditional use (e.g. speculative decoding): given a draw x from P_X, sample Y."""
        y = self.joint.sampYgivenX(rng, tuple(x[v] for v in self.vars))
        return dict(zip(self.vars, y))


def node_scopes(t: Node) -> list[list[str]]:
    """Scopes of all nodes of the tree: the sets that SMC-CPT maximally couples."""
    if isinstance(t, Leaf):
        return [[t.var]]
    if isinstance(t, Product):
        return node_scopes(t.left) + node_scopes(t.right) + [scope(t)]
    return node_scopes(t.child) + [scope(t)]


def chain_tree(first: Leaf, steps: Sequence[tuple[str, Conditional, Conditional]]) -> Node:
    """Autoregressive CPT: leaf(first) followed by chain nodes."""
    t: Node = first
    for var, cX, cY in steps:
        t = Chain(t, var, cX, cY)
    return t

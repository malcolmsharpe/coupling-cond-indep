"""Exact (enumerative) computation of MRC and SMC-CPT couplings for small finite examples.

Used as ground truth in tests. Couplings are dicts {(x, y): probability} with x, y tuples.
"""

from __future__ import annotations

from itertools import product

import numpy as np

from .core import Chain, Leaf, Node, Product


def mrc_exact(P: dict) -> dict:
    """Exact maximal recoupling of a coupling P (paper, Section 4: walk restricted to R)."""
    states = sorted({x for x, _ in P} | {y for _, y in P}, key=repr)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = np.zeros((n, n))
    for (x, y), p in P.items():
        M[idx[x], idx[y]] += p
    pX, pY = M.sum(1), M.sum(0)
    out = np.diag(np.minimum(pX, pY))
    EX = pX > 0
    K = np.zeros((n, n))
    K[EX] = M[EX] / pX[EX, None]
    rho = np.ones(n)
    pos = pY > 0
    rho[pos] = np.minimum(1.0, pX[pos] / pY[pos])
    Q = K * rho[None, :]
    H = K * (1 - rho)[None, :]
    alpha = np.maximum(0.0, pX - pY)
    # R = nodes reachable from sources; the walk never leaves R.
    R = set(np.flatnonzero(alpha > 0))
    stack = list(R)
    while stack:
        v = stack.pop()
        for w in np.flatnonzero(M[v] > 0):
            if w not in R:
                R.add(w)
                stack.append(w)
    RX = sorted(v for v in R if EX[v])
    if RX:
        QR = Q[np.ix_(RX, RX)]
        occ = np.linalg.solve(np.eye(len(RX)) - QR.T, np.eye(len(RX))).T  # (I - QR)^{-1}
        occ = alpha[RX][:, None] * occ  # row x: expected departures from each v, started at x
        out[np.ix_(RX, range(n))] += occ @ H[RX]
    return {(states[i], states[j]): out[i, j] for i in range(n) for j in range(n) if out[i, j] > 1e-15}


def smc_cpt_exact(t: Node, alphabets: dict) -> dict:
    """Exact SMC-CPT coupling of a CPT whose oracles are finite (alphabets: var -> values)."""
    if isinstance(t, Leaf):
        A = alphabets[t.var]
        P = {((a,), (b,)): t.mX.L(a) * t.mY.L(b) for a in A for b in A if t.mX.L(a) * t.mY.L(b) > 0}
        return mrc_exact(P)
    if isinstance(t, Product):
        P1, P2 = smc_cpt_exact(t.left, alphabets), smc_cpt_exact(t.right, alphabets)
        P = {}
        for (x1, y1), p1 in P1.items():
            for (x2, y2), p2 in P2.items():
                P[(x1 + x2, y1 + y2)] = p1 * p2
        return mrc_exact(P)
    P1 = smc_cpt_exact(t.child, alphabets)
    A = alphabets[t.var]
    P = {}
    for (x1, y1), p1 in P1.items():
        for a, b in product(A, A):
            q = p1 * t.cX.L(x1, a) * t.cY.L(y1, b)
            if q > 0:
                P[(x1 + (a,), y1 + (b,))] = q
    return mrc_exact(P)


def project(P: dict, idx: list[int]) -> dict:
    out: dict = {}
    for (x, y), p in P.items():
        k = (tuple(x[i] for i in idx), tuple(y[i] for i in idx))
        out[k] = out.get(k, 0.0) + p
    return out


def marginals(P: dict) -> tuple[dict, dict]:
    mx: dict = {}
    my: dict = {}
    for (x, y), p in P.items():
        mx[x] = mx.get(x, 0.0) + p
        my[y] = my.get(y, 0.0) + p
    return mx, my


def max_agreement(mx: dict, my: dict) -> float:
    """1 - TV(mx, my): the agreement probability of a maximal coupling."""
    return sum(min(mx.get(k, 0.0), my.get(k, 0.0)) for k in set(mx) | set(my))


def agreement(P: dict) -> float:
    return sum(p for (x, y), p in P.items() if x == y)


def is_maximal(P: dict, tol: float = 1e-12) -> bool:
    mx, my = marginals(P)
    diag = {x: p for (x, y), p in P.items() if x == y}
    return all(abs(diag.get(k, 0.0) - min(mx.get(k, 0.0), my.get(k, 0.0))) < tol for k in set(mx) | set(my))

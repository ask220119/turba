#!/usr/bin/env python3
"""Simplified Bishop factor of safety on one circular slip surface.

Geometry is 2D: a ground surface polyline, horizontal soil layers (top elevation, gamma, c', phi'),
an optional horizontal water table, and a uniform surcharge on the ground surface.

Usage:
    python bishop.py --surface "0,10 10,10 20,0 40,0" --layers "10,19,5,30" \
        --xc 22 --yc 18 --R 19 --gwt 2 --q 10

--layers takes "top_elevation,gamma,c,phi" groups separated by spaces, from top to bottom.
Units: m, kN/m3, kPa, degrees. The script is a check tool: refine the search and confirm the
result with your usual software.
"""
from __future__ import annotations

import argparse
import math

GAMMA_W = 9.81


def ground_y(surface: list[tuple[float, float]], x: float) -> float:
    for (x0, y0), (x1, y1) in zip(surface, surface[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 != x0 else max(y0, y1)
    return surface[0][1] if x < surface[0][0] else surface[-1][1]


def layer_at(layers: list[tuple[float, float, float, float]], y: float) -> tuple[float, float, float, float]:
    """Layer containing elevation y; layers sorted by decreasing top elevation."""
    chosen = layers[0]
    for lay in layers:
        if y <= lay[0]:
            chosen = lay
    return chosen


def column_weight(layers, y_top: float, y_bot: float) -> float:
    """Weight per unit width per unit length of a vertical column between y_bot and y_top."""
    w = 0.0
    tops = [l[0] for l in layers] + [-1e9]
    for i, lay in enumerate(layers):
        top = min(lay[0], y_top)
        bot = max(tops[i + 1], y_bot)
        if top > bot:
            w += lay[1] * (top - bot)
    # above the first layer top (fill above declared layers): use first layer gamma
    if y_top > layers[0][0]:
        w += layers[0][1] * (y_top - max(layers[0][0], y_bot))
    return w


def bishop(surface, layers, xc, yc, R, gwt=None, q=0.0, n_slices=50, tol=1e-5):
    # intersections of the circle with the ground, by scanning
    xs = [surface[0][0] + i * (surface[-1][0] - surface[0][0]) / 4000 for i in range(4001)]
    inside = [x for x in xs if abs(x - xc) < R and yc - math.sqrt(R * R - (x - xc) ** 2) < ground_y(surface, x)]
    if len(inside) < 2:
        raise ValueError("the circle does not cut the slope")
    xa, xb = min(inside), max(inside)
    b = (xb - xa) / n_slices
    slices = []
    for i in range(n_slices):
        x = xa + (i + 0.5) * b
        yb = yc - math.sqrt(R * R - (x - xc) ** 2)
        yt = ground_y(surface, x)
        if yt <= yb:
            continue
        W = column_weight(layers, yt, yb) * b + q * b
        alpha = math.asin((x - xc) / R)
        u = GAMMA_W * max(gwt - yb, 0.0) if gwt is not None else 0.0
        _, _, c, phi = layer_at(layers, yb)
        slices.append((W, alpha, u, c, math.radians(phi)))
    driving = sum(W * math.sin(a) for W, a, *_ in slices)
    if driving < 0:  # slope facing +x: movement towards +x, flip the angle convention
        slices = [(W, -a, u, c, phi) for W, a, u, c, phi in slices]
        driving = -driving
    if driving == 0:
        raise ValueError("no driving moment")
    F = 1.0
    for _ in range(200):
        resisting = 0.0
        for W, a, u, c, phi in slices:
            m = math.cos(a) * (1 + math.tan(a) * math.tan(phi) / F)
            resisting += (c * b + (W - u * b) * math.tan(phi)) / m
        F_new = resisting / driving
        if abs(F_new - F) < tol:
            return F_new
        F = F_new
    return F


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--surface", required=True)
    p.add_argument("--layers", required=True)
    p.add_argument("--xc", type=float, required=True)
    p.add_argument("--yc", type=float, required=True)
    p.add_argument("--R", type=float, required=True)
    p.add_argument("--gwt", type=float, default=None)
    p.add_argument("--q", type=float, default=0.0)
    a = p.parse_args()
    surface = [tuple(map(float, pt.split(","))) for pt in a.surface.split()]
    layers = sorted([tuple(map(float, l.split(","))) for l in a.layers.split()], key=lambda l: -l[0])
    print(f"F (Bishop) = {bishop(surface, layers, a.xc, a.yc, a.R, a.gwt, a.q):.3f}")


if __name__ == "__main__":
    main()

"""Reference checks for the TURBA calculation scripts (hand calculations in comments)."""
import importlib.util
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / "skills"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


menard = load(ROOT / "turba-foundations/scripts/menard_settlement.py")
liq = load(ROOT / "turba-seismic-liquefaction/scripts/liquefaction_spt.py")
bishop = load(ROOT / "turba-slope-stability/scripts/bishop.py")


def test_menard_square_hand_calc():
    # B = L = 2 m, q - sv0 = 230 kPa, EM = 8 MPa, alpha = 0.5, square: lc = 1.10, ld = 1.12
    r = menard.menard_settlement(2.0, 250, 20, 0.5, 8, 8, L=2.0)
    sc = 0.5 / 72 * 0.23 * 1.10 * 2.0
    sd = 2 / 72 * 0.23 * 0.6 * (1.12 * 2.0 / 0.6) ** 0.5
    assert math.isclose(r["sc"], sc, rel_tol=1e-9)
    assert math.isclose(r["sd"], sd, rel_tol=1e-9)
    assert 0.010 < r["s"] < 0.012  # about 11 mm


def test_menard_layered_equals_homogeneous():
    Ec, Ed = menard.layered_moduli([10.0] * 16)
    assert math.isclose(Ec, 10.0)
    # 4/Ed = 1/E + 1/0.85E + 1/E + 1/2.5E + 1/2.5E
    assert math.isclose(Ed, 4 / (1 / 10 + 1 / 8.5 + 1 / 10 + 2 / 25))


def test_menard_shape_table():
    assert menard.shape_coefficients(2, None) == (1.0, 1.0)
    assert menard.shape_coefficients(2, 4) == (1.20, 1.53)
    assert menard.shape_coefficients(1, 50) == (1.50, 2.65)


def test_liquefaction_bi2014_points():
    # CRR(M7.5, 1 atm) at (N1)60cs = 15: about 0.16 (Boulanger and Idriss 2014, figure 8.1)
    assert 0.15 < liq.crr_75(15) < 0.17
    # MSF = 1 at M = 7.5 (by definition, within rounding of the published constants)
    assert abs(liq.msf(7.5, 20) - 1.0) < 0.01
    # clean sand: no fines correction
    assert liq.delta_n_fines(0) < 1e-6
    # FC = 35 %: correction close to 5.5 blows
    assert 5.3 < liq.delta_n_fines(35) < 5.7
    # rd at z = 0 is 1
    assert abs(liq.rd_idriss(0.0, 7.5) - 1.0) < 0.02


def test_liquefaction_profile_runs():
    rows = [{"depth_m": 2, "N60": 8, "FC": 5, "gamma": 18}, {"depth_m": 6, "N60": 25, "FC": 5, "gamma": 19}]
    out = liq.analyse(rows, amax=0.25, M=7.5, gwt=1.0)
    assert out[0]["FS"] < 1.0 < out[1]["FS"]


def test_bishop_undrained_matches_moment_equilibrium():
    # phi = 0: Bishop reduces to F = c R arc / sum(W x); compare with an independent integration.
    surface = [(0, 10), (10, 10), (20, 0), (40, 0)]
    layers = [(10, 18, 40, 0)]
    xc, yc, R = 15, 16, 16
    F = bishop.bishop(surface, layers, xc, yc, R, n_slices=400)
    # independent: arc length between the two ground intersections and moment of the soil weight
    n = 20000
    xs = [i * 40 / n for i in range(n + 1)]
    inside = [x for x in xs if abs(x - xc) < R and yc - math.sqrt(R * R - (x - xc) ** 2) < bishop.ground_y(surface, x)]
    xa, xb = min(inside), max(inside)
    theta = lambda x: math.asin((x - xc) / R)
    arc = R * (theta(xb) - theta(xa))
    dx = (xb - xa) / n
    moment = 0.0
    for i in range(n):
        x = xa + (i + 0.5) * dx
        h = bishop.ground_y(surface, x) - (yc - math.sqrt(R * R - (x - xc) ** 2))
        moment += 18 * max(h, 0) * dx * (x - xc)
    F_ref = 40 * arc * R / abs(moment)
    assert math.isclose(F, F_ref, rel_tol=0.01)


def test_bishop_slope_direction_symmetric():
    right = [(0, 10), (10, 10), (20, 0), (40, 0)]
    left = [(0, 0), (20, 0), (30, 10), (40, 10)]
    layers = [(10, 19, 5, 30)]
    Fr = bishop.bishop(right, layers, 22, 18, 19)
    Fl = bishop.bishop(left, layers, 18, 18, 19)
    assert math.isclose(Fr, Fl, rel_tol=0.02)

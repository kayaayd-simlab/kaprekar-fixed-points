"""Faz 2 — siralama hucresi taramasi (n=8).

Yontem (plandan onaylanmis sapma): sympy.linsolve yerine kesirli aritmetik
(fractions.Fraction) ile satir indirgeme. Sistem A_sigma d = c*B + f sag
tarafta B'de lineer oldugundan cozum dogrudan d_i = x_i*B + y_i cikar.
sympy yalniz ornekleme capraz dogrulamasi icin (kuruluysa).

Hucre siniflari:
  UNIQUE_ALL_B    her B icin tekil cozum -> asimptotik esitsizlik + butunluk
                  analiziyle YASAYAN AILE / PENCERE (sonlu B araligi) / OLU
  UNIQUE_FINITE_B yalniz tek bir B'de cozum (sporadik aday) -> core ile
                  sayisal dogrulanir
  INCONSISTENT    hicbir pozitif tamsayi B'de cozum yok
  UNDERDETERMINED serbest parametreli -> Faz 3'te derin inceleme

Guvence (n=6 dersi): coken hucrelerde ust sinir B_max hesaplanir; B_max > 59
ise (b>60, ground-truth kapsami disi) pencere sayisal taranir.
"""

import json
import os
import random
import sys
from collections import Counter
from fractions import Fraction
from itertools import permutations
from math import ceil, floor, lcm

from core import value_from_d, to_digits, d_vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "cells_n8.json")
GT_BMAX = 60  # Faz 0 ground-truth kapsami (b <= 60)


# ---------- ifadeler ve hucre sistemi ----------

def expressions(t):
    """Kanal t (sondaki sifir sayisi) icin 8 ardil ifadenin lineer verisi.

    Her ifade (M, P, Q): deger = sum_j M[j]*d_j + P*B + Q.  m = 4-t bilinmeyen.
    Faz 1 formulleri:
      t=0: [d0, d1, d2, d3-1, B-d3, B-d2, B-d1, B+1-d0]
      t=1: [d0, d1, d2-1, B, B, B-d2, B-d1, B+1-d0]
      t=2: [d0, d1-1, B, B, B, B, B-d1, B+1-d0]
      t=3: [d0-1, B, B, B, B, B, B, B+1-d0]
    """
    m = 4 - t
    E = []
    for i in range(m - 1):
        row = [0] * m
        row[i] = 1
        E.append((tuple(row), 0, 0))
    row = [0] * m
    row[m - 1] = 1
    E.append((tuple(row), 0, -1))
    for _ in range(2 * t):
        E.append((tuple([0] * m), 1, 0))
    for i in range(m - 1, 0, -1):
        row = [0] * m
        row[i] = -1
        E.append((tuple(row), 1, 0))
    row = [0] * m
    row[0] = -1
    E.append((tuple(row), 1, 1))
    assert len(E) == 8
    return E


def cell_system(E, sigma, m):
    """Hucre denklemleri: E[sigma[i]] - E[sigma[7-i]] = d_i (i=0..3, i>=m ise 0).

    A d = c*B + f bicimine getirilir.
    """
    A, c, f = [], [], []
    for i in range(4):
        Mt, Pt, Qt = E[sigma[i]]
        Mb, Pb, Qb = E[sigma[7 - i]]
        row = [Mt[j] - Mb[j] for j in range(m)]
        if i < m:
            row[i] -= 1
        A.append(row)
        c.append(Pb - Pt)
        f.append(Qb - Qt)
    return A, c, f


def rref(A, c, f, m):
    """[A | c | f] uzerinde kesirli RREF. Doner: rows, rank, pivot kolonlari."""
    rows = [[Fraction(A[i][j]) for j in range(m)]
            + [Fraction(c[i]), Fraction(f[i])] for i in range(4)]
    r = 0
    piv = []
    for col in range(m):
        p = next((i for i in range(r, 4) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [v / pv for v in rows[r]]
        for i in range(4):
            if i != r and rows[i][col] != 0:
                fac = rows[i][col]
                rows[i] = [v - fac * w for v, w in zip(rows[i], rows[r])]
        piv.append(col)
        r += 1
        if r == 4:
            break
    return rows, r, piv


def classify(rows, r, m):
    """Sinif ve (varsa) sabitlenen B degeri."""
    fixed = []
    for i in range(r, 4):
        cc, ff = rows[i][m], rows[i][m + 1]
        if cc == 0 and ff == 0:
            continue
        if cc == 0:
            return "INCONSISTENT", None
        fixed.append(-ff / cc)
    if fixed:
        B0 = fixed[0]
        if any(v != B0 for v in fixed[1:]):
            return "INCONSISTENT", None
        if B0.denominator != 1 or B0 < 1:
            return "INCONSISTENT", None
        return ("UNIQUE_FINITE_B" if r == m else "UNDERDET_FINITE_B"), int(B0)
    return ("UNIQUE_ALL_B" if r == m else "UNDERDETERMINED"), None


# ---------- gecerlilik analizi ----------

def eval_linear(E, x, y, m):
    """Cozumde her ifadenin degeri: (B katsayisi, sabit)."""
    out = []
    for (M, P, Q) in E:
        coef = sum(Fraction(M[j]) * x[j] for j in range(m)) + P
        cons = sum(Fraction(M[j]) * y[j] for j in range(m)) + Q
        out.append((coef, cons))
    return out


def constraints(E, sigma, x, y, m):
    """Gecerlilik kisitlari, her biri (g1, g0, req): g1*B + g0 >= req."""
    ev = eval_linear(E, x, y, m)
    C = []
    for i in range(7):  # siralama: a_i >= a_{i+1}
        a1, b1 = ev[sigma[i]]
        a2, b2 = ev[sigma[i + 1]]
        C.append((a1 - a2, b1 - b2, 0))
    C.append((*ev[sigma[7]], 0))                      # son rakam >= 0
    a0c, a0k = ev[sigma[0]]
    C.append((1 - a0c, -a0k, 0))                      # bas rakam <= B
    C.append((x[0], y[0], 1))                         # d0 >= 1 (8 basamak)
    C.append((x[m - 1], y[m - 1], 1))                 # kanal: son d >= 1
    C.append((1 - x[0], -y[0], 0))                    # d0 <= B
    for i in range(m - 1):                            # d azalan
        C.append((x[i] - x[i + 1], y[i] - y[i + 1], 0))
    return C


def feasibility(C):
    """Kisit sistemi B'de: ('LIVE', lo, None) / ('WINDOW', lo, hi) / ('DEAD',..)."""
    lo, hi = 1, None
    for g1, g0, req in C:
        if g1 > 0:
            lo = max(lo, ceil(Fraction(req - g0, 1) / g1))
        elif g1 == 0:
            if g0 < req:
                return "DEAD", None, None
        else:
            h = floor(Fraction(g0 - req, 1) / (-g1))
            hi = h if hi is None else min(hi, h)
    if hi is not None and hi < lo:
        return "DEAD", None, None
    return ("LIVE", lo, None) if hi is None else ("WINDOW", lo, hi)


def pad4(dv, m):
    return tuple(list(dv) + [0] * (4 - m))


def validate_numeric(dv4, b):
    """d-vektorunu core ile dogrula: gercek 8-basamakli sabit nokta mi."""
    if not all(isinstance(v, int) for v in dv4):
        return False
    if not (b - 1 >= dv4[0] >= dv4[1] >= dv4[2] >= dv4[3] >= 0 and dv4[0] >= 1):
        return False
    v = value_from_d(dv4, b, 8)
    if v < b ** 7:
        return False
    digs = to_digits(v, b)
    return len(digs) == 8 and d_vector(sorted(digs, reverse=True), 8) == dv4


def frac_formula(xi, yi):
    """d_i = xi*B + yi icin okunur metin, ortak paydayla."""
    den = lcm(xi.denominator, yi.denominator)
    a, bnum = xi * den, yi * den
    core_txt = f"{int(a)}B" if a else ""
    if bnum or not core_txt:
        core_txt += f"{int(bnum):+d}" if core_txt else f"{int(bnum)}"
    return f"({core_txt})/{den}" if den != 1 else core_txt


# ---------- kanal taramasi ----------

def scan_channel(t):
    E = expressions(t)
    m = 4 - t
    seen = set()
    counts = Counter()
    families = {}       # (x,y) -> info
    sporadics = set()   # (b, dv4) dogrulanmis
    window_hits = set()
    underdet = []

    for sigma in permutations(range(8)):
        key = tuple(E[j] for j in sigma)
        if key in seen:
            continue
        seen.add(key)
        A, c, f = cell_system(E, sigma, m)
        rows, r, piv = rref(A, c, f, m)
        cls, B0 = classify(rows, r, m)
        counts[cls] += 1

        if cls == "UNIQUE_ALL_B":
            x = [rows[k][m] for k in range(m)]
            y = [rows[k][m + 1] for k in range(m)]
            C = constraints(E, sigma, x, y, m)
            status, lo, hi = feasibility(C)
            counts["  " + status] += 1
            if status == "LIVE":
                D = 1
                for v in x + y:
                    D = lcm(D, v.denominator)
                res = [rr for rr in range(D)
                       if all((x[i] * rr + y[i]).denominator == 1
                              for i in range(m))]
                if not res:
                    counts["  LIVE_ama_butunluk_bos"] += 1
                    continue
                fk = (tuple(x), tuple(y))
                if fk not in families:
                    families[fk] = {"t": t, "D": D, "residues_B": res,
                                    "thr_B": lo, "cells": 0,
                                    "x": [str(v) for v in x],
                                    "y": [str(v) for v in y]}
                fam = families[fk]
                fam["cells"] += 1
                fam["thr_B"] = min(fam["thr_B"], lo)
            elif status == "WINDOW":
                span = hi - lo + 1
                if span > 200000:
                    counts["  WINDOW_cok_genis_UYARI"] += 1
                    continue
                for B in range(max(lo, 1), hi + 1):
                    if any((x[i] * B + y[i]).denominator != 1 for i in range(m)):
                        continue
                    dv = pad4([int(x[i] * B + y[i]) for i in range(m)], m)
                    if validate_numeric(dv, B + 1):
                        window_hits.add((B + 1, dv))
                if hi > GT_BMAX - 1:
                    counts["  WINDOW_GT_disina_tasti"] += 1

        elif cls == "UNIQUE_FINITE_B":
            x = [rows[k][m] for k in range(m)]
            y = [rows[k][m + 1] for k in range(m)]
            vals = [x[i] * B0 + y[i] for i in range(m)]
            if all(v.denominator == 1 for v in vals):
                dv = pad4([int(v) for v in vals], m)
                if validate_numeric(dv, B0 + 1):
                    sporadics.add((B0 + 1, dv))

        elif cls in ("UNDERDETERMINED", "UNDERDET_FINITE_B"):
            underdet.append({"t": t, "sigma": list(sigma),
                             "rank": r, "fixed_B": B0})

    return {"m": m, "distinct_cells": len(seen), "counts": counts,
            "families": families, "sporadics": sporadics,
            "window_hits": window_hits, "underdet": underdet}


# ---------- aile dogrulamasi ----------

def family_first_members(fam, m, count=2):
    """Ailenin esik ustu ilk `count` uyesini uret ve core ile dogrula."""
    x = [Fraction(s) for s in fam["x"]]
    y = [Fraction(s) for s in fam["y"]]
    D, res = fam["D"], set(fam["residues_B"])
    out = []
    B = max(fam["thr_B"], 1)
    while len(out) < count and B < fam["thr_B"] + 5 * max(D, 1) + 100:
        if B % D in res:
            dv = pad4([int(x[i] * B + y[i]) for i in range(m)], m)
            out.append((B + 1, dv, validate_numeric(dv, B + 1)))
        B += 1
    return out


# ---------- sympy capraz dogrulama (ornekleme) ----------

def crosscheck(sample_per_channel=40, seed=42):
    try:
        import sympy as sp
    except ImportError:
        print("\ncapraz dogrulama: sympy kurulu degil, ATLANDI "
              "(ana sonuc kesirli aritmetikle zaten kesin).")
        return
    rng = random.Random(seed)
    Bs = sp.Symbol("B")
    ok = bad = 0
    for t in range(4):
        E = expressions(t)
        m = 4 - t
        for _ in range(sample_per_channel):
            sigma = tuple(rng.sample(range(8), 8))
            A, c, f = cell_system(E, sigma, m)
            rows, r, piv = rref(A, c, f, m)
            cls, B0 = classify(rows, r, m)
            if sp.Matrix(A).rank() != r:
                bad += 1
                print(f"  RANK UYUSMAZLIGI t={t} sigma={sigma}")
                continue
            if cls == "UNIQUE_ALL_B":
                ds = sp.symbols(f"d0:{m}")
                eqs = [sp.Eq(sum(A[i][j] * ds[j] for j in range(m)),
                             c[i] * Bs + f[i]) for i in range(4)]
                sol = sp.linsolve(eqs, ds)
                if len(sol) != 1:
                    bad += 1
                    print(f"  COZUM UYUSMAZLIGI t={t} sigma={sigma}: linsolve={sol}")
                    continue
                tup = next(iter(sol))
                exp = [sp.Rational(rows[k][m]) * Bs + sp.Rational(rows[k][m + 1])
                       for k in range(m)]
                if any(sp.simplify(tup[k] - exp[k]) != 0 for k in range(m)):
                    bad += 1
                    print(f"  FORMUL UYUSMAZLIGI t={t} sigma={sigma}")
                    continue
            ok += 1
    print(f"\nsympy capraz dogrulama: {ok} ornek uyustu, {bad} uyusmazlik.")


# ---------- ana ----------

def main():
    all_out = {}
    print("Faz 2 hucre taramasi (kesirli RREF, 4 kanal):")
    for t in range(4):
        r = scan_channel(t)
        all_out[t] = r
        print(f"\n--- kanal t={t} (k={4+t}, {r['m']} bilinmeyen) ---")
        print(f"  ayrik hucre: {r['distinct_cells']}")
        for k, v in sorted(r["counts"].items()):
            print(f"  {k}: {v}")
        fams = list(r["families"].values())
        fams.sort(key=lambda F: (F["D"], F["x"]))
        print(f"  YASAYAN AILE (tekillesmis): {len(fams)}")
        for F in fams:
            x = [Fraction(s) for s in F["x"]]
            y = [Fraction(s) for s in F["y"]]
            formula = ", ".join(frac_formula(x[i], y[i]) for i in range(r["m"]))
            cong = " veya ".join(f"b={(rr + 1) % F['D']}(mod {F['D']})"
                                 for rr in F["residues_B"])
            members = family_first_members(F, r["m"])
            F["first_members"] = [(b, list(dv), okk) for b, dv, okk in members]
            val = all(okk for _, _, okk in members) and members
            print(f"    D={F['D']} | {cong} | d=({formula}) | "
                  f"esik b>={F['thr_B'] + 1} | hucre={F['cells']} | "
                  f"ilk uyeler={[b for b, _, _ in members]} | "
                  f"dogrulama={'OK' if val else 'HATA!'}")
        if r["sporadics"]:
            sp_ = sorted(r["sporadics"])
            print(f"  sporadik (tek-B, dogrulanmis): {sp_}")
        if r["window_hits"]:
            print(f"  pencere vurusu (dogrulanmis): {sorted(r['window_hits'])}")
        print(f"  belirsiz hucre: {len(r['underdet'])}")

    # JSON onbellek
    dump = {}
    for t, r in all_out.items():
        dump[str(t)] = {
            "distinct_cells": r["distinct_cells"],
            "counts": dict(r["counts"]),
            "families": list(r["families"].values()),
            "sporadics": sorted([b, list(dv)] for b, dv in r["sporadics"]),
            "window_hits": sorted([b, list(dv)] for b, dv in r["window_hits"]),
            "underdet": r["underdet"],
        }
    with open(OUT, "w") as fh:
        json.dump(dump, fh)
    print(f"\nyazildi: {OUT}")

    crosscheck()


if __name__ == "__main__":
    main()

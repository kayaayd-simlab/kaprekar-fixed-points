"""Faz 3b — her-B belirsiz hucrelerin KESIN kapanisi (2 degiskenli kesirli LP).

Her-B belirsiz hucrelerin tamami 1 serbest boyutlu (Faz 3 tespiti): cozum
uzayi (B, u) duzleminde afin, tum gecerlilik kisitlari lineer. Bu script
her hucre icin:
  1) B-yonunde recession testi (bolge B'de sinirsiz mi?)
  2) sinirliysa kose sayimiyla kesin B_max (kesirli aritmetik, yuvarlamasiz)
  3) b_max = floor(B_max)+1 <= 500 ise Faz 3'un tam taramasi zaten kapatti;
     b_max > 500 ise 501..b_max araligi burada tuketilir.
Hepsi temizse "taramayla kapali" etiketi "kanitli"ya yukselir:
b > b_max icin bolge BOS oldugundan tarama disinda nokta kalamaz.
"""

import json
import os
import sys
from collections import Counter
from fractions import Fraction
from math import floor

from phase2_cells import expressions, cell_system, rref
from phase3_synthesis import (CELLS, enum_cell_points_at_b, family_points,
                              load_families)

SCANNED_FULL = 500  # Faz 3 closure'in tam taradigi ust sinir (b<=500)


def cell_constraints(t, sigma):
    """Hucrenin gecerlilik kisitlari, (gB, gu, h) bicimi: gB*B + gu*u >= h.

    u := serbest d-bileseni. Doner: (kisitlar, serbest boyut).
    """
    E = expressions(t)
    m = 4 - t
    A, c, f = cell_system(E, sigma, m)
    rows, r, piv = rref(A, c, f, m)
    for i in range(r, 4):
        assert rows[i][m] == 0 and rows[i][m + 1] == 0, "her-B hucresi degil!"
    free = [j for j in range(m) if j not in piv]
    if len(free) != 1:
        return None, len(free)
    fc = free[0]
    dfun = [None] * m               # d_j = aB*B + a1 + au*u
    dfun[fc] = (Fraction(0), Fraction(0), Fraction(1))
    for k in range(r):
        dfun[piv[k]] = (rows[k][m], rows[k][m + 1], -rows[k][fc])

    def etr(j):
        M, P, Q = E[j]
        return (sum(Fraction(M[i]) * dfun[i][0] for i in range(m)) + P,
                sum(Fraction(M[i]) * dfun[i][1] for i in range(m)) + Q,
                sum(Fraction(M[i]) * dfun[i][2] for i in range(m)))

    ev = [etr(j) for j in range(8)]
    cons = []

    def ge(aB, a1, au, req):        # aB*B + a1 + au*u >= req
        cons.append((aB, au, Fraction(req) - a1))

    for i in range(7):              # siralama
        x1, y1, z1 = ev[sigma[i]]
        x2, y2, z2 = ev[sigma[i + 1]]
        ge(x1 - x2, y1 - y2, z1 - z2, 0)
    ge(*ev[sigma[7]], 0)            # son rakam >= 0
    xa, ya, za = ev[sigma[0]]
    ge(1 - xa, -ya, -za, 0)         # bas rakam <= B
    ge(*dfun[0], 1)                 # d0 >= 1
    ge(*dfun[m - 1], 1)             # kanal: son d >= 1
    ge(1 - dfun[0][0], -dfun[0][1], -dfun[0][2], 0)   # d0 <= B
    for i in range(m - 1):          # d azalan
        ge(dfun[i][0] - dfun[i + 1][0], dfun[i][1] - dfun[i + 1][1],
           dfun[i][2] - dfun[i + 1][2], 0)
    ge(1, 0, -1, 0)                 # u <= B  (0 <= u zaten d-zinciriyle; yine de:)
    ge(0, 1, 0, 0)                  # u >= 0
    ge(1, 0, 0, 1)                  # B >= 1
    return cons, 1


def recession_unbounded(cons):
    """dB=1 yonunde recession var mi: her kisit icin gB + gu*du >= 0."""
    lo = hi = None
    for gB, gu, _h in cons:
        if gu == 0:
            if gB < 0:
                return False
        else:
            v = -gB / gu
            if gu > 0:
                lo = v if lo is None else max(lo, v)
            else:
                hi = v if hi is None else min(hi, v)
    return lo is None or hi is None or lo <= hi


def max_B(cons):
    """Kose sayimiyla kesin sup B. Doner (feasible_mi, B_max)."""
    best = None
    n = len(cons)
    for i in range(n):
        gBi, gui, hi_ = cons[i]
        for j in range(i + 1, n):
            gBj, guj, hj_ = cons[j]
            det = gBi * guj - gBj * gui
            if det == 0:
                continue
            Bv = (hi_ * guj - hj_ * gui) / det
            uv = (gBi * hj_ - gBj * hi_) / det
            if all(gB * Bv + gu * uv >= h for gB, gu, h in cons):
                best = Bv if best is None else max(best, Bv)
    return (best is not None), best


def main():
    fams = load_families()
    cells = [cl for ch in CELLS.values() for cl in ch["underdet"]
             if cl["fixed_B"] is None]
    print(f"Faz 3b: {len(cells)} her-B belirsiz hucre, kesin LP kapanisi")

    unbounded, empty, dim_bad = [], 0, 0
    bmax_hist = Counter()
    extra_scan = []     # (hucre, b_max) — 500 ustune tasanlar
    global_bmax = 0
    for idx, cl in enumerate(cells):
        t, sigma = cl["t"], tuple(cl["sigma"])
        cons, dim = cell_constraints(t, sigma)
        if cons is None:
            dim_bad += 1
            continue
        # SIRA ONEMLI: once fizibilite. Bolge (B>=1, 0<=u<=B) icinde cizgi
        # iceremez -> sivri (pointed) -> bos-degilse kosesi VARDIR. Kose yoksa
        # bolge bostur; recession testi ancak bos-olmayan bolgede anlamlidir.
        feas, Bmax = max_B(cons)
        if not feas:
            empty += 1
            continue
        if recession_unbounded(cons):
            unbounded.append((t, sigma))
            continue
        b_max = floor(Bmax) + 1
        global_bmax = max(global_bmax, b_max)
        if b_max <= 60:
            bmax_hist["b_max<=60 (GT kapatti)"] += 1
        elif b_max <= SCANNED_FULL:
            bmax_hist["60<b_max<=500 (Faz 3 tam taramasi kapatti)"] += 1
        else:
            bmax_hist["b_max>500 (ek tarama)"] += 1
            extra_scan.append((t, sigma, b_max))
        if (idx + 1) % 200 == 0:
            print(f"  ilerleme: {idx + 1}/{len(cells)}", flush=True)

    print(f"\n  bos bolge (hicbir B'de gecerli nokta yok): {empty}")
    for k, v in sorted(bmax_hist.items()):
        print(f"  {k}: {v}")
    print(f"  en buyuk b_max: {global_bmax}")
    if dim_bad:
        print(f"  UYARI: 1-boyutlu olmayan hucre: {dim_bad}")
    if unbounded:
        print(f"  !!! B-yonunde SINIRSIZ hucre: {len(unbounded)} — "
              f"yapisal argüman gerekir:")
        for t, sg in unbounded[:20]:
            print(f"    t={t} sigma={sg}")

    # 500 ustune tasan hucrelerde tuketici tarama
    bad_pts = []
    for t, sigma, b_max in extra_scan:
        for b in range(SCANNED_FULL + 1, b_max + 1):
            pts, capped = enum_cell_points_at_b(t, sigma, b)
            assert not capped
            for d4 in pts:
                if d4 not in family_points(b, fams):
                    bad_pts.append((b, d4))
    if extra_scan:
        print(f"  ek tarama: {len(extra_scan)} hucre 501..b_max tuketildi; "
              f"aile-disi nokta: {len(bad_pts)}")
        for x in bad_pts:
            print("   !!!", x)

    ok = not unbounded and not dim_bad and not bad_pts
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "data", "phase3b_lp.json")
    with open(out, "w") as fh:
        json.dump({"cells": len(cells), "empty": empty,
                   "hist": dict(bmax_hist), "global_bmax": global_bmax,
                   "unbounded": len(unbounded), "extra_scan_bad": bad_pts},
                  fh)
    print(f"\nyazildi: {out}")
    if ok:
        print("SONUC: GECTI — her-B belirsiz hucrelerin tamami KESIN kapandi; "
              "'taramayla kapali' etiketi 'kanitli'ya yukselebilir.")
    else:
        print("SONUC: KALDI — yukaridaki istisnalari incele.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

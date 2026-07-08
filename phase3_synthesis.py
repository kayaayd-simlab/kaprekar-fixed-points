"""Faz 3 — gecerlilik, kapanis ve sentez.

Kullanim:
  python phase3_synthesis.py closure
    (1) kongruans birlesimi vs GT b<=60: NOKTA duzeyinde birebir karsilastirma
    (2) sabit-B belirsiz hucrelerin kapanisi — yalniz B0+1 > 60 olanlar
        (b<=60'i Faz 0 kaba kuvveti zaten eksiksiz kapatiyor)
    (3) her-B belirsiz hucrelerin b>60 taramasi: serbest boyuta gore derinlik
        (dim1: b<=500 + buyuk ornekler; dim2: b<=300; dim3+: b<=150)
    (4) kalinti sayimlari: periyot, kapsanan kalinti sayisi, tek-taban birlesimi

  python phase3_synthesis.py gtext
    Ground-truth'u b=61..100'e uzat (tam d-uzayi taramasi) ve aile tahminiyle
    NOKTA duzeyinde karsilastir. Tahmin: b>60'ta sporadik yok, her sey aile.
"""

import json
import os
import sys
from collections import Counter
from fractions import Fraction
from itertools import product
from math import ceil, floor, lcm

from core import scan_fixed_points, d_vector
from phase2_cells import expressions, cell_system, rref, validate_numeric, pad4

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "data", "groundtruth_n8.json")) as fh:
    GT = {int(b): v for b, v in json.load(fh).items()}
with open(os.path.join(HERE, "data", "cells_n8.json")) as fh:
    CELLS = json.load(fh)


def load_families():
    fams = []
    for t, ch in CELLS.items():
        for F in ch["families"]:
            fams.append({"t": int(t), "m": 4 - int(t), "D": F["D"],
                         "res": set(F["residues_B"]), "thr": F["thr_B"],
                         "x": [Fraction(s) for s in F["x"]],
                         "y": [Fraction(s) for s in F["y"]]})
    return fams


def load_sporadics():
    spor = set()
    for ch in CELLS.values():
        for key in ("sporadics", "window_hits"):
            for b, d in ch.get(key, []):
                spor.add((b, tuple(d)))
    return spor


def family_points(b, fams):
    """b tabaninda ailelerin urettigi d4 kumesi."""
    pts = set()
    B = b - 1
    for F in fams:
        if B >= F["thr"] and B % F["D"] in F["res"]:
            d = [F["x"][i] * B + F["y"][i] for i in range(F["m"])]
            assert all(v.denominator == 1 for v in d), (b, F)
            pts.add(pad4([int(v) for v in d], F["m"]))
    return pts


# ---------- (1) GT b<=60 birebir karsilastirma ----------

def check_gt60(fams, spor):
    total = fam_total = spor_pts = 0
    spor_bases, mism = [], []
    for b in range(2, 61):
        gset = {d_vector(p, 8) for p in GT.get(b, [])}
        fset = family_points(b, fams)
        sset = {d for (bb, d) in spor if bb == b}
        total += len(gset)
        fam_total += len(fset)
        spor_pts += len(gset - fset)
        if fset - gset:
            mism.append((b, "aile uyesi GT'de YOK", sorted(fset - gset)))
        if gset != (fset | sset):
            mism.append((b, "kume esitligi bozuk", sorted(gset ^ (fset | sset))))
        if gset and not fset:
            spor_bases.append(b)
    print("(1) GT b<=60 karsilastirmasi:")
    print(f"  GT nokta: {total} | aile uyesi: {fam_total} | "
          f"aile-disi (sporadik) nokta: {spor_pts}")
    print(f"  yalniz-sporadik tabanlar: {spor_bases}")
    if mism:
        for x in mism:
            print("  UYUSMAZLIK:", x)
        print("  SONUC: KALDI — dur, kimligini cikar!")
        return False
    print("  SONUC: GECTI — GT = aile uyeleri ∪ kapali sporadikler, birebir.")
    return True


# ---------- (2)+(3) belirsiz hucre kapanisi ----------

def enum_cell_points_at_b(t, sigma, b, cap=200000):
    """Belirsiz hucrenin b tabanindaki TUM gecerli sabit noktalari.

    Serbest degiskenler d_j'nin kendisi -> 0..B kutusu; son serbest
    degisken icin pivot sinirlarindan (0<=d_pivot<=B) aralik kirpma.
    Doner: (dogrulanmis d4 listesi, cap_asildi_mi)
    """
    E = expressions(t)
    m = 4 - t
    A, c, f = cell_system(E, sigma, m)
    rows, r, piv = rref(A, c, f, m)
    B = b - 1
    for i in range(r, 4):
        if rows[i][m] * B + rows[i][m + 1] != 0:
            return [], False  # bu B'de cozum yok
    free = [j for j in range(m) if j not in piv]
    dim = len(free)
    if dim == 0:
        return [], False
    if (B + 1) ** (dim - 1) > cap:
        return [], True
    pv = [(piv[k], rows[k][m] * B + rows[k][m + 1],
           [-rows[k][j] for j in free]) for k in range(r)]
    found = []
    for partial in product(range(B + 1), repeat=dim - 1):
        lo, hi = Fraction(0), Fraction(B)
        dead = False
        for _col, cst, cf in pv:
            val = cst + sum(cf[i] * partial[i] for i in range(dim - 1))
            a = cf[dim - 1]
            if a == 0:
                if not (0 <= val <= B):
                    dead = True
                    break
            elif a > 0:
                lo = max(lo, -val / a)
                hi = min(hi, (B - val) / a)
            else:
                lo = max(lo, (val - B) / (-a))
                hi = min(hi, val / (-a))
        if dead or lo > hi:
            continue
        for ul in range(ceil(lo), floor(hi) + 1):
            u = list(partial) + [ul]
            dfull = [0] * m
            ok = True
            for col, cst, cf in pv:
                v = cst + sum(cf[i] * u[i] for i in range(dim))
                if v.denominator != 1:
                    ok = False
                    break
                dfull[col] = int(v)
            if not ok:
                continue
            for i, j in enumerate(free):
                dfull[j] = u[i]
            d4 = pad4(dfull, m)
            if validate_numeric(d4, b):
                found.append(d4)
    return found, False


def closure_underdet(fams):
    cells = []
    for ch in CELLS.values():
        cells += ch["underdet"]
    fin = [cl for cl in cells if cl["fixed_B"] is not None]
    allb = [cl for cl in cells if cl["fixed_B"] is None]
    unknown, capped = [], 0

    # (2) sabit-B
    skip60 = proc = hits = 0
    big_b = Counter()
    for cl in fin:
        b0 = cl["fixed_B"] + 1
        if b0 <= 60:
            skip60 += 1
            continue
        proc += 1
        big_b[b0] += 1
        pts, cp = enum_cell_points_at_b(cl["t"], tuple(cl["sigma"]), b0)
        capped += cp
        for d4 in pts:
            hits += 1
            if d4 not in family_points(b0, fams):
                unknown.append((b0, d4, "sabitB"))
    print(f"\n(2) sabit-B belirsiz hucreler: {len(fin)} adet; "
          f"b<=60 (GT kapatiyor): {skip60}; b>60 islenen: {proc}")
    if big_b:
        print(f"  b>60 sabitlenen tabanlar: {dict(sorted(big_b.items()))}")
    print(f"  b>60'ta bulunan gecerli nokta: {hits} "
          f"(aile-disi: {len([u for u in unknown if u[2] == 'sabitB'])})")

    # (3) her-B
    def bases_for(dim):
        if dim <= 1:
            return list(range(61, 501)) + [601, 787, 997, 1201, 1499]
        if dim == 2:
            return list(range(61, 301)) + [401, 499, 997]
        return list(range(61, 151)) + [211, 499]

    dims = Counter()
    hits3 = 0
    for idx, cl in enumerate(allb):
        t, sigma, m = cl["t"], tuple(cl["sigma"]), 4 - cl["t"]
        E = expressions(t)
        A, c, f = cell_system(E, sigma, m)
        _rows, r, _piv = rref(A, c, f, m)
        dim = m - r
        dims[dim] += 1
        for b in bases_for(dim):
            pts, cp = enum_cell_points_at_b(t, sigma, b)
            capped += cp
            for d4 in pts:
                hits3 += 1
                if d4 not in family_points(b, fams):
                    unknown.append((b, d4, "herB"))
        if (idx + 1) % 100 == 0:
            print(f"  her-B ilerleme: {idx + 1}/{len(allb)}", flush=True)
    print(f"(3) her-B belirsiz hucreler: {len(allb)} adet; "
          f"serbest boyut dagilimi: {dict(sorted(dims.items()))}")
    print(f"  b>60 taramasinda bulunan gecerli nokta: {hits3} "
          f"(aile-disi: {len([u for u in unknown if u[2] == 'herB'])})")
    if capped:
        print(f"  UYARI: {capped} hucre-taban taramasi cap nedeniyle atlandi.")
    if unknown:
        print("  !!! AILE-DISI YENI NOKTALAR:")
        for u in sorted(set(unknown)):
            print("   ", u)
        return False
    print("  SONUC: belirsiz hucrelerden aile-disi hicbir nokta cikmadi.")
    return True


# ---------- (4) kalinti sayimlari ----------

def residue_counts(fams):
    P = 1
    for F in fams:
        P = lcm(P, F["D"])

    def member(x):
        return any((x - 1) % F["D"] in F["res"] for F in fams)

    all_cnt = sum(1 for x in range(P) if member(x))
    P2 = 2 * P
    odd_cnt = sum(1 for x in range(P2) if x % 2 == 1 and member(x))
    print(f"\n(4) kalinti sayimlari:")
    print(f"  tum tabanlar: periyot {P}, kapsanan {all_cnt}/{P} kalinti "
          f"(yogunluk {all_cnt / P:.4f})")
    print(f"  tek tabanlar: periyot {P2}, kapsanan {odd_cnt} tek kalinti "
          f"(tek tabanlarin orani {odd_cnt / (P2 / 2):.4f})")
    print(f"  (kiyas: n=6 tek tabanlarda periyot 630, 93 kalinti, oran "
          f"{93 / 315:.4f})")
    print("  tek-taban kongruans birlesimi (2D modulleri):")
    for F in sorted(fams, key=lambda F: F["D"]):
        for rr in sorted(F["res"]):
            br = (rr + 1) % F["D"]
            odd_r = br if br % 2 == 1 else br + F["D"]
            print(f"    b ≡ {odd_r} (mod {2 * F['D']})   "
                  f"[aile: b ≡ {br} (mod {F['D']}), t={F['t']}]")


# ---------- gtext ----------

def gtext(fams, lo=61, hi=100):
    print(f"GT uzatmasi b={lo}..{hi} (tam d-uzayi taramasi):")
    bad = []
    for b in range(lo, hi + 1):
        gset = {d_vector(p, 8) for p in scan_fixed_points(b, 8)}
        pred = family_points(b, fams)
        ok = gset == pred
        if not ok:
            bad.append((b, sorted(gset - pred), sorted(pred - gset)))
        print(f"  b={b}: bulunan={len(gset)} tahmin={len(pred)} "
              f"{'OK' if ok else 'UYUSMAZLIK!'}", flush=True)
    if bad:
        print("SONUC: KALDI — uyusmazliklar:")
        for x in bad:
            print("  ", x)
    else:
        print(f"SONUC: GECTI — b={lo}..{hi} tamaminda bulunan = aile tahmini, "
              f"sporadik yok.")
    return not bad


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "closure"
    fams = load_families()
    if mode == "closure":
        ok1 = check_gt60(fams, load_sporadics())
        ok2 = closure_underdet(fams)
        residue_counts(fams)
        sys.exit(0 if (ok1 and ok2) else 1)
    elif mode == "gtext":
        sys.exit(0 if gtext(fams) else 1)
    else:
        print("bilinmeyen mod:", mode)
        sys.exit(2)

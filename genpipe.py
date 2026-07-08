"""Genel cift-n Kaprekar boru hatti — n=6 sertlestirme (ileride n=10).

n=8 makinesinin (phase1/2/3/3b) n-parametreli genellemesi. Ayni mimari:
  - varlik iddialari  -> validate_numeric ile sayisal muhur (K(x)=x dogrudan)
  - yokluk iddialari  -> yalniz GEREKLI kisitlar, kapali (>=) esitsizlikler
  - kesin kesirli aritmetik, sifir kayan nokta

Akis: GT (b<=gtmax) -> kanal formulu dogrulamasi -> hucre taramasi ->
belirsiz hucre kapanisi (2D-LP + tuketici sayim) -> GT/uzatma karsilastirma
-> kongruans/kalinti ozeti -> RREF'siz verdikt denetimi.

Kullanim: python genpipe.py [n] [gtmax] [gtext_hi]   (varsayilan 6 60 150)
"""

import sys
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, permutations, product
from math import ceil, floor, lcm

from core import scan_fixed_points, value_from_d, to_digits, d_vector

CAP = 200000


# ---------- kanallar ve hucre sistemi ----------

def expressions(n, t):
    """Kanal t icin n ardil ifadenin lineer verisi (M, P, Q). m = n/2 - t."""
    m = n // 2 - t
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
    assert len(E) == n
    return E


def cell_system(E, sigma, m, h):
    A, c, f = [], [], []
    for i in range(h):
        Mt, Pt, Qt = E[sigma[i]]
        Mb, Pb, Qb = E[sigma[len(sigma) - 1 - i]]
        row = [Mt[j] - Mb[j] for j in range(m)]
        if i < m:
            row[i] -= 1
        A.append(row)
        c.append(Pb - Pt)
        f.append(Qb - Qt)
    return A, c, f


def rref(A, c, f, m, h):
    rows = [[Fraction(A[i][j]) for j in range(m)]
            + [Fraction(c[i]), Fraction(f[i])] for i in range(h)]
    r = 0
    piv = []
    for col in range(m):
        p = next((i for i in range(r, h) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][col]
        rows[r] = [v / pv for v in rows[r]]
        for i in range(h):
            if i != r and rows[i][col] != 0:
                fac = rows[i][col]
                rows[i] = [v - fac * w for v, w in zip(rows[i], rows[r])]
        piv.append(col)
        r += 1
        if r == h:
            break
    return rows, r, piv


def classify(rows, r, m, h):
    fixed = []
    for i in range(r, h):
        cc, ff = rows[i][m], rows[i][m + 1]
        if cc == 0 and ff == 0:
            continue
        if cc == 0:
            return "INCONSISTENT", None
        fixed.append(-ff / cc)
    if fixed:
        B0 = fixed[0]
        if any(v != B0 for v in fixed[1:]) or B0.denominator != 1 or B0 < 1:
            return "INCONSISTENT", None
        return ("UNIQUE_FINITE_B" if r == m else "UNDERDET_FINITE_B"), int(B0)
    return ("UNIQUE_ALL_B" if r == m else "UNDERDETERMINED"), None


# ---------- gecerlilik ----------

def padh(dv, m, h):
    return tuple(list(dv) + [0] * (h - m))


def validate_numeric(dvh, b, n):
    h = n // 2
    if not all(isinstance(v, int) for v in dvh):
        return False
    if not all(dvh[i] >= dvh[i + 1] for i in range(h - 1)):
        return False
    if not (b - 1 >= dvh[0] >= 1 and dvh[h - 1] >= 0):
        return False
    v = value_from_d(dvh, b, n)
    if v < b ** (n - 1):
        return False
    digs = to_digits(v, b)
    return len(digs) == n and d_vector(sorted(digs, reverse=True), n) == dvh


def eval_linear(E, x, y, m):
    out = []
    for (M, P, Q) in E:
        out.append((sum(Fraction(M[j]) * x[j] for j in range(m)) + P,
                    sum(Fraction(M[j]) * y[j] for j in range(m)) + Q))
    return out


def constraints(E, sigma, x, y, m, n):
    ev = eval_linear(E, x, y, m)
    C = []
    for i in range(n - 1):
        a1, b1 = ev[sigma[i]]
        a2, b2 = ev[sigma[i + 1]]
        C.append((a1 - a2, b1 - b2, 0))
    C.append((*ev[sigma[n - 1]], 0))
    a0c, a0k = ev[sigma[0]]
    C.append((1 - a0c, -a0k, 0))
    C.append((x[0], y[0], 1))
    C.append((x[m - 1], y[m - 1], 1))
    C.append((1 - x[0], -y[0], 0))
    for i in range(m - 1):
        C.append((x[i] - x[i + 1], y[i] - y[i + 1], 0))
    return C


def feasibility(C):
    lo, hi = 1, None
    for g1, g0, req in C:
        if g1 > 0:
            lo = max(lo, ceil(Fraction(req - g0, 1) / g1))
        elif g1 == 0:
            if g0 < req:
                return "DEAD", None, None
        else:
            hh = floor(Fraction(g0 - req, 1) / (-g1))
            hi = hh if hi is None else min(hi, hh)
    if hi is not None and hi < lo:
        return "DEAD", None, None
    return ("LIVE", lo, None) if hi is None else ("WINDOW", lo, hi)


# ---------- kanal taramasi ----------

def scan_channel(n, t, gtmax):
    E = expressions(n, t)
    h = n // 2
    m = h - t
    seen = set()
    counts = Counter()
    families = {}
    sporadics = set()
    window_hits = set()
    underdet = []
    for sigma in permutations(range(n)):
        key = tuple(E[j] for j in sigma)
        if key in seen:
            continue
        seen.add(key)
        A, c, f = cell_system(E, sigma, m, h)
        rows, r, piv = rref(A, c, f, m, h)
        cls, B0 = classify(rows, r, m, h)
        counts[cls] += 1
        if cls == "UNIQUE_ALL_B":
            x = [rows[k][m] for k in range(m)]
            y = [rows[k][m + 1] for k in range(m)]
            C = constraints(E, sigma, x, y, m, n)
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
                    counts["  LIVE_butunluk_bos"] += 1
                    continue
                fk = (tuple(x), tuple(y))
                if fk not in families:
                    families[fk] = {"t": t, "m": m, "D": D, "res": set(res),
                                    "thr": lo, "x": x, "y": y, "cells": 0}
                families[fk]["cells"] += 1
                families[fk]["thr"] = min(families[fk]["thr"], lo)
            elif status == "WINDOW":
                if hi - lo + 1 > CAP:
                    counts["  WINDOW_CAP_UYARI"] += 1
                    continue
                for B in range(max(lo, 1), hi + 1):
                    if any((x[i] * B + y[i]).denominator != 1
                           for i in range(m)):
                        continue
                    dv = padh([int(x[i] * B + y[i]) for i in range(m)], m, h)
                    if validate_numeric(dv, B + 1, n):
                        window_hits.add((B + 1, dv))
        elif cls == "UNIQUE_FINITE_B":
            x = [rows[k][m] for k in range(m)]
            y = [rows[k][m + 1] for k in range(m)]
            vals = [x[i] * B0 + y[i] for i in range(m)]
            if all(v.denominator == 1 for v in vals):
                dv = padh([int(v) for v in vals], m, h)
                if validate_numeric(dv, B0 + 1, n):
                    sporadics.add((B0 + 1, dv))
        else:
            if cls != "INCONSISTENT":
                underdet.append({"t": t, "sigma": sigma, "rank": r,
                                 "fixed_B": B0})
    return {"m": m, "cells": len(seen), "counts": counts,
            "families": families, "sporadics": sporadics,
            "windows": window_hits, "underdet": underdet}


# ---------- belirsiz hucre kapanisi ----------

def enum_cell_points(n, t, sigma, b, cap=CAP):
    E = expressions(n, t)
    h = n // 2
    m = h - t
    A, c, f = cell_system(E, sigma, m, h)
    rows, r, piv = rref(A, c, f, m, h)
    B = b - 1
    for i in range(r, h):
        if rows[i][m] * B + rows[i][m + 1] != 0:
            return [], False
    free = [j for j in range(m) if j not in piv]
    dim = len(free)
    if dim == 0 or (B + 1) ** (dim - 1) > cap:
        return [], dim != 0
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
            dv = padh(dfull, m, h)
            if validate_numeric(dv, b, n):
                found.append(dv)
    return found, False


def lp_cell(n, t, sigma):
    """dim-1 her-B hucresi icin (feasible, unbounded, B_max). Kesin 2D-LP."""
    E = expressions(n, t)
    h = n // 2
    m = h - t
    A, c, f = cell_system(E, sigma, m, h)
    rows, r, piv = rref(A, c, f, m, h)
    free = [j for j in range(m) if j not in piv]
    if len(free) != 1:
        return None
    fc = free[0]
    dfun = [None] * m
    dfun[fc] = (Fraction(0), Fraction(0), Fraction(1))
    for k in range(r):
        dfun[piv[k]] = (rows[k][m], rows[k][m + 1], -rows[k][fc])

    def etr(j):
        M, P, Q = E[j]
        return (sum(Fraction(M[i]) * dfun[i][0] for i in range(m)) + P,
                sum(Fraction(M[i]) * dfun[i][1] for i in range(m)) + Q,
                sum(Fraction(M[i]) * dfun[i][2] for i in range(m)))

    ev = [etr(j) for j in range(n)]
    cons = []

    def ge(aB, a1, au, req):
        cons.append((aB, au, Fraction(req) - a1))

    for i in range(n - 1):
        x1, y1, z1 = ev[sigma[i]]
        x2, y2, z2 = ev[sigma[i + 1]]
        ge(x1 - x2, y1 - y2, z1 - z2, 0)
    ge(*ev[sigma[n - 1]], 0)
    xa, ya, za = ev[sigma[0]]
    ge(1 - xa, -ya, -za, 0)
    ge(*dfun[0], 1)
    ge(*dfun[m - 1], 1)
    ge(1 - dfun[0][0], -dfun[0][1], -dfun[0][2], 0)
    for i in range(m - 1):
        ge(dfun[i][0] - dfun[i + 1][0], dfun[i][1] - dfun[i + 1][1],
           dfun[i][2] - dfun[i + 1][2], 0)
    ge(1, 0, -1, 0)
    ge(0, 1, 0, 0)
    ge(1, 0, 0, 1)

    best = None
    nn = len(cons)
    for i in range(nn):
        gBi, gui, hi_ = cons[i]
        for j in range(i + 1, nn):
            gBj, guj, hj_ = cons[j]
            det = gBi * guj - gBj * gui
            if det == 0:
                continue
            Bv = (hi_ * guj - hj_ * gui) / det
            uv = (gBi * hj_ - gBj * hi_) / det
            if all(gB * Bv + gu * uv >= hh for gB, gu, hh in cons):
                best = Bv if best is None else max(best, Bv)
    if best is None:
        return ("EMPTY", None)
    lo = hi = None
    for gB, gu, _h in cons:
        if gu == 0:
            if gB < 0:
                return ("BOUNDED", floor(best) + 1)
        else:
            v = -gB / gu
            if gu > 0:
                lo = v if lo is None else max(lo, v)
            else:
                hi = v if hi is None else min(hi, v)
    if lo is None or hi is None or lo <= hi:
        return ("UNBOUNDED", None)
    return ("BOUNDED", floor(best) + 1)


# ---------- yardimcilar ----------

def family_points(b, fams, h):
    pts = set()
    B = b - 1
    for F in fams:
        if B >= F["thr"] and B % F["D"] in F["res"]:
            d = [F["x"][i] * B + F["y"][i] for i in range(F["m"])]
            pts.add(padh([int(v) for v in d], F["m"], h))
    return pts


def frac_formula(xi, yi):
    den = lcm(xi.denominator, yi.denominator)
    a, bnum = xi * den, yi * den
    s = f"{int(a)}B" if a else ""
    if bnum or not s:
        s += f"{int(bnum):+d}" if s else f"{int(bnum)}"
    return f"({s})/{den}" if den != 1 else s


def solutions_desc(A, c, f, m, h, B):
    sols = []
    for asc in combinations_with_replacement(range(B + 1), m):
        d = asc[::-1]
        if all(sum(A[i][j] * d[j] for j in range(m)) == c[i] * B + f[i]
               for i in range(h)):
            sols.append(d)
    return sols


# ---------- ana akis ----------

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    gtmax = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    gtext_hi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    h = n // 2
    fail = 0
    print(f"=== genpipe n={n}, GT b<={gtmax}, uzatma b<={gtext_hi} ===")

    # 1) GT + kanal formulu dogrulamasi
    GT = {b: scan_fixed_points(b, n) for b in range(2, gtmax + 1)}
    tot = sum(len(v) for v in GT.values())
    kdist = Counter()
    bad_f = 0
    for b, fps in GT.items():
        for sd in fps:
            d = d_vector(sd, n)
            t = 0
            for v in reversed(d):
                if v != 0:
                    break
                t += 1
            kdist[h + t] += 1
            E = expressions(n, t)
            vals = sorted((sum(M[j] * d[j] for j in range(h - t)) + P * (b - 1)
                           + Q for (M, P, Q) in E), reverse=True)
            if vals != sd:
                bad_f += 1
    print(f"[1] GT: {tot} nokta; k dagilimi {dict(sorted(kdist.items()))}; "
          f"kanal formulu uyusmazligi: {bad_f}")
    fail += bad_f

    # 2) hucre taramalari
    res = {}
    all_fams = []
    spor = set()
    for t in range(h):
        r = scan_channel(n, t, gtmax)
        res[t] = r
        spor |= r["sporadics"] | r["windows"]
        print(f"[2] t={t} (k={h+t}): hucre={r['cells']} | " +
              " ".join(f"{k.strip()}={v}" for k, v in sorted(r["counts"].items())) +
              f" | belirsiz={len(r['underdet'])}")
        for F in sorted(r["families"].values(), key=lambda F: F["D"]):
            formula = ", ".join(frac_formula(F["x"][i], F["y"][i])
                                for i in range(F["m"]))
            cong = ",".join(str((rr + 1) % F["D"]) for rr in sorted(F["res"]))
            print(f"     AILE D={F['D']} b={cong}(mod {F['D']}) "
                  f"d=({formula}) esik b>={F['thr']+1}")
            all_fams.append(F)

    # 3) belirsiz hucre kapanisi
    n_open = 0
    stats = Counter()
    for t in range(h):
        for cl in res[t]["underdet"]:
            if cl["fixed_B"] is not None:
                b0 = cl["fixed_B"] + 1
                if b0 <= gtmax:
                    stats["sabitB_GT_kapatti"] += 1
                else:
                    pts, capped = enum_cell_points(n, t, cl["sigma"], b0)
                    stats["sabitB_enum"] += 1
                    for dv in pts:
                        if dv not in family_points(b0, all_fams, h):
                            print(f"  !!! sabitB aile-disi: b={b0} {dv}")
                            fail += 1
                continue
            out = lp_cell(n, t, cl["sigma"])
            if out is None:  # dim >= 2: tarama + bayrak
                stats["dim2+_tarama"] += 1
                for b in range(gtmax + 1, 401):
                    pts, capped = enum_cell_points(n, t, cl["sigma"], b)
                    for dv in pts:
                        if dv not in family_points(b, all_fams, h):
                            print(f"  !!! dim2 aile-disi: b={b} {dv}")
                            fail += 1
                n_open += 1
                continue
            status, b_max = out
            if status == "EMPTY":
                stats["herB_bos"] += 1
            elif status == "UNBOUNDED":
                stats["herB_SINIRSIZ"] += 1
                fail += 1
            else:
                stats[f"herB_sinirli"] += 1
                if b_max > gtmax:
                    for b in range(gtmax + 1, b_max + 1):
                        pts, _ = enum_cell_points(n, t, cl["sigma"], b)
                        for dv in pts:
                            if dv not in family_points(b, all_fams, h):
                                print(f"  !!! herB aile-disi: b={b} {dv}")
                                fail += 1
    print(f"[3] kapanis: {dict(stats)}; dim2+ (yalniz-tarama) hucre: {n_open}")

    # 4) GT karsilastirma + uzatma
    mism = 0
    spor_bases = []
    for b in range(2, gtmax + 1):
        gset = {d_vector(p, n) for p in GT[b]}
        fset = family_points(b, all_fams, h)
        sset = {d for (bb, d) in spor if bb == b}
        if fset - gset or gset != (fset | sset):
            mism += 1
            print(f"  !!! b={b} kume uyusmazligi: GT={sorted(gset)} "
                  f"aile={sorted(fset)} spor={sorted(sset)}")
        if gset and not fset:
            spor_bases.append(b)
    print(f"[4] GT b<={gtmax}: uyusmazlik={mism}; "
          f"yalniz-sporadik tabanlar={spor_bases}; "
          f"sporadik noktalar (aile-disi) hepsi b<="
          f"{max((b for b, _ in spor), default=0)}")
    fail += mism
    ext_bad = 0
    for b in range(gtmax + 1, gtext_hi + 1):
        gset = {d_vector(p, n) for p in scan_fixed_points(b, n)}
        if gset != family_points(b, all_fams, h):
            ext_bad += 1
            print(f"  !!! uzatma b={b} uyusmazligi")
    print(f"[4] uzatma b={gtmax+1}..{gtext_hi}: uyusmazlik={ext_bad}")
    fail += ext_bad

    # 5) kongruans ozeti
    P = 1
    for F in all_fams:
        P = lcm(P, F["D"])
    def member(b):
        return any((b - 1) % F["D"] in F["res"] for F in all_fams)
    allc = sum(member(x) for x in range(P))
    oddc = sum(1 for x in range(2 * P) if x % 2 == 1 and member(x))
    print(f"[5] periyot {P}, kapsam {allc}/{P}; tek tabanlar: 2P={2*P} "
          f"icinde {oddc} tek kalinti")
    print("    tek-taban kongruanslari:")
    for F in sorted(all_fams, key=lambda F: F["D"]):
        for rr in sorted(F["res"]):
            br = (rr + 1) % F["D"]
            if F["D"] % 2 == 0:
                if br % 2 == 1:
                    print(f"      b={br} (mod {F['D']})")
            else:
                r2 = br if br % 2 == 1 else br + F["D"]
                print(f"      b={r2} (mod {2*F['D']})   [aile b={br} mod {F['D']}]")

    # 6) RREF'siz verdikt denetimi
    rng = random.Random(11)
    bad = 0
    checked = 0
    for t in range(h):
        E = expressions(n, t)
        m = h - t
        for _ in range(100):
            sigma = tuple(rng.sample(range(n), n))
            A, c, f = cell_system(E, sigma, m, h)
            rows, r, piv = rref(A, c, f, m, h)
            cls, B0 = classify(rows, r, m, h)
            for B in (11, 16):
                checked += 1
                sols = solutions_desc(A, c, f, m, h, B)
                if cls == "INCONSISTENT" or (
                        cls in ("UNIQUE_FINITE_B", "UNDERDET_FINITE_B")
                        and B != B0):
                    ok = not sols
                elif cls == "UNIQUE_ALL_B" or (cls == "UNIQUE_FINITE_B"
                                               and B == B0):
                    vals = [rows[k][m] * B + rows[k][m + 1] for k in range(m)]
                    exp = []
                    if all(v.denominator == 1 and 0 <= v <= B for v in vals):
                        dd = tuple(int(v) for v in vals)
                        if all(dd[i] >= dd[i + 1] for i in range(m - 1)):
                            exp = [dd]
                    ok = sols == exp
                else:
                    ok = True
                if not ok:
                    bad += 1
                    print(f"  !!! denetim t={t} sigma={sigma} B={B} cls={cls}")
    print(f"[6] verdikt denetimi: {checked} hucre-B, uyusmazlik {bad}")
    fail += bad

    print(f"\nSONUC: {'GECTI — n=%d tamamen kapali' % n if fail == 0 else 'KALDI (%d sorun)' % fail}")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()

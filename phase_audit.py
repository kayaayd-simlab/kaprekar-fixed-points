"""Bagimsiz denetim (oz-elestiri sertlestirmesi).

A) NAIF tam-aralik kaba kuvvet: d-uzayi kisayolu KULLANMADAN, x'in tum
   araligi [b^(n-1), b^n) uzerinde K(x)=x dogrudan test edilir ve
   core.scan_fixed_points ile birebir karsilastirilir.
   Kapsam: n=8 icin b=2..8, n=6 icin b=2..10 (549945/631764 dis cengeli).
   Bu, d-uzayi esdegerligi + basamak/onde-sifir konvansiyonlarini
   bagimsiz dogrular.

B) HUCRE VERDIKT denetimi: rastgele hucrelerde, azalan d-konisi B=11 ve
   B=16'da TUKETILEREK A_sigma d = cB+f cozum kumesi dogrudan sayilir ve
   siniflandiricinin verdiktiyle karsilastirilir. RREF kodundan bagimsiz;
   ozellikle NEGATIF verdiktleri (INCONSISTENT / cozumsuz B) sinar —
   kanitin tamlik yonu bu negatiflere yaslanir.
"""

import random
import sys
from fractions import Fraction
from itertools import combinations_with_replacement

from core import scan_fixed_points, to_digits
from phase2_cells import cell_system, classify, expressions, rref

SAMPLES = 150
TEST_B = (11, 16)


# ---------- A ----------

def naive_scan(b, n):
    out = []
    for x in range(b ** (n - 1), b ** n):
        sd = sorted(to_digits(x, b), reverse=True)
        desc_v = 0
        asc_v = 0
        for dg in sd:
            desc_v = desc_v * b + dg
        for dg in reversed(sd):
            asc_v = asc_v * b + dg
        if desc_v - asc_v == x:
            out.append(sd)
    out.sort()
    return out


def part_a():
    bad = 0
    for n, bmax in ((8, 8), (6, 10)):
        for b in range(2, bmax + 1):
            nv = naive_scan(b, n)
            dv = scan_fixed_points(b, n)
            ok = nv == dv
            if not ok:
                bad += 1
                print(f"  A UYUSMAZLIK n={n} b={b}: naif={nv} d-uzayi={dv}")
            else:
                print(f"  A n={n} b={b}: {len(nv)} nokta, birebir OK",
                      flush=True)
    return bad == 0


# ---------- B ----------

def solutions_desc(A, c, f, m, B):
    sols = []
    for asc in combinations_with_replacement(range(B + 1), m):
        d = asc[::-1]
        if all(sum(A[i][j] * d[j] for j in range(m)) == c[i] * B + f[i]
               for i in range(4)):
            sols.append(d)
    return sols


def part_b():
    rng = random.Random(7)
    bad = checked = 0
    for t in range(4):
        E = expressions(t)
        m = 4 - t
        for _ in range(SAMPLES):
            sigma = tuple(rng.sample(range(8), 8))
            A, c, f = cell_system(E, sigma, m)
            rows, r, piv = rref(A, c, f, m)
            cls, B0 = classify(rows, r, m)
            for B in TEST_B:
                checked += 1
                sols = solutions_desc(A, c, f, m, B)
                if cls == "INCONSISTENT" or \
                   (cls in ("UNIQUE_FINITE_B", "UNDERDET_FINITE_B")
                        and B != B0):
                    if sols:
                        bad += 1
                        print(f"  B UYUSMAZLIK t={t} sigma={sigma} B={B}: "
                              f"verdikt={cls} ama cozum var: {sols[:3]}")
                elif cls == "UNIQUE_ALL_B" or \
                        (cls == "UNIQUE_FINITE_B" and B == B0):
                    vals = [rows[k][m] * B + rows[k][m + 1] for k in range(m)]
                    exp = []
                    if all(v.denominator == 1 and 0 <= v <= B for v in vals):
                        dd = tuple(int(v) for v in vals)
                        if all(dd[i] >= dd[i + 1] for i in range(m - 1)):
                            exp = [dd]
                    if sols != exp:
                        bad += 1
                        print(f"  B UYUSMAZLIK t={t} sigma={sigma} B={B}: "
                              f"verdikt={cls} beklenen={exp} bulunan={sols}")
                else:  # UNDERDETERMINED / UNDERDET_FINITE_B @ B0
                    free = [j for j in range(m) if j not in piv]
                    for d in sols:
                        for k in range(r):
                            want = rows[k][m] * B + rows[k][m + 1] - \
                                sum(rows[k][j] * d[j] for j in free)
                            if Fraction(d[piv[k]]) != want:
                                bad += 1
                                print(f"  B PARAM UYUSMAZLIGI t={t} "
                                      f"sigma={sigma} B={B} d={d}")
                                break
        print(f"  B kanal t={t}: {SAMPLES} hucre x {len(TEST_B)} B denetlendi",
              flush=True)
    print(f"  B toplam denetim: {checked} hucre-B, uyusmazlik: {bad}")
    return bad == 0


if __name__ == "__main__":
    print("A) Naif tam-aralik kaba kuvvet vs d-uzayi taramasi:")
    ok_a = part_a()
    print("\nB) Hucre verdikt denetimi (RREF'siz, tuketici):")
    ok_b = part_b()
    print(f"\nSONUC: A={'GECTI' if ok_a else 'KALDI'}  "
          f"B={'GECTI' if ok_b else 'KALDI'}")
    sys.exit(0 if (ok_a and ok_b) else 1)

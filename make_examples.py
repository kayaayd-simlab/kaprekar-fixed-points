"""Her hucre sinifindan BIR gercek ornek cikar (makale Bolum 3 icin).

Kay'in onerisi: dort hucre sinifinin (unique-all-B / unique-single-B /
inconsistent / underdetermined) her birinden calisilmis birer ornek.
Uydurma yok — genpipe'in kendi siniflandiricisindan gercek permutasyonlar
secilir ve lineer sistem A d = B c + e acikca yazdirilir. n=6 kullanilir
(3 bilinmeyen, okunur).
"""
from fractions import Fraction
from itertools import permutations

from genpipe import expressions, cell_system, rref, classify, constraints, feasibility

n = 6
h = n // 2


def names_for(t):
    m = h - t
    lbl = [f"d{i}" for i in range(m - 1)] + [f"d{m-1}-1"]
    lbl += ["B"] * (2 * t)
    lbl += [f"B-d{i}" for i in range(m - 1, 0, -1)] + ["b-d0"]
    return lbl


def system_str(A, c, f, m):
    lines = []
    for i in range(h):
        terms = " + ".join(f"{A[i][j]}*d{j}" for j in range(m) if A[i][j])
        lines.append(f"   {terms or '0'} = {c[i]}*B + {f[i]}")
    return "\n".join(lines)


want = {"UNIQUE_ALL_B_live": None, "UNIQUE_FINITE_B": None,
        "INCONSISTENT": None, "UNDERDETERMINED": None}

for t in (0, 1):
    m = h - t
    E = expressions(n, t)
    seen = set()
    for sigma in permutations(range(n)):
        key = tuple(E[j] for j in sigma)
        if key in seen:
            continue
        seen.add(key)
        A, c, f = cell_system(E, sigma, m, h)
        rows, r, piv = rref(A, c, f, m, h)
        cls, B0 = classify(rows, r, m, h)
        if cls == "UNIQUE_ALL_B" and want["UNIQUE_ALL_B_live"] is None and t == 0:
            x = [rows[k][m] for k in range(m)]
            y = [rows[k][m + 1] for k in range(m)]
            C = constraints(E, sigma, x, y, m, n)
            status, lo, hi = feasibility(C)
            if status == "LIVE":
                want["UNIQUE_ALL_B_live"] = (t, sigma, A, c, f, x, y, lo)
        elif cls in want and want[cls] is None:
            want[cls] = (t, sigma, A, c, f, rows, r, B0)

from math import lcm

order = ["UNIQUE_ALL_B_live", "UNIQUE_FINITE_B", "INCONSISTENT", "UNDERDETERMINED"]
for cls in order:
    v = want[cls]
    print("=" * 60)
    print("SINIF:", cls)
    if v is None:
        print("  (bulunamadi)")
        continue
    t, sigma, A, c, f = v[0], v[1], v[2], v[3], v[4]
    m = h - t
    lbl = names_for(t)
    print(f"  kanal t={t}, m={m} bilinmeyen; ifadeler:", lbl)
    print("  sigma =", sigma, " ->  sirali:", [lbl[j] for j in sigma])
    print("  sistem A d = B c + e:")
    print(system_str(A, c, f, m))
    if cls == "UNIQUE_ALL_B_live":
        x, y, lo = v[5], v[6], v[7]
        det = 1
        for val in x + y:
            det = lcm(det, val.denominator)
        print(f"  cozum: d_i = (alpha_i B + beta_i)/{det}")
        for i in range(m):
            print(f"    d{i} = ({x[i]*det}B + {y[i]*det})/{det}")
        print(f"  gecerlilik esigi: B >= {lo} (yani b >= {lo+1})")
    elif cls == "UNIQUE_FINITE_B":
        rows, r, B0 = v[5], v[6], v[7]
        print(f"  tam rank ama artik satir B'yi sabitliyor: yalniz B = {B0} "
              f"(b = {B0+1}) icin cozum")
    elif cls == "INCONSISTENT":
        rows, r = v[5], v[6]
        print(f"  rank(A) = {r}; artik satir tutarsiz:")
        for i in range(r, h):
            print(f"    0 = {rows[i][m]}*B + {rows[i][m+1]} "
                  f"(hicbir gecerli B icin saglanmaz)")
    elif cls == "UNDERDETERMINED":
        rows, r = v[5], v[6]
        print(f"  rank(A) = {r} < {m}: bir serbest parametre kaliyor")

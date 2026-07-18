"""REVIZE-V2 icin kalan sayisal veriler.

1) n=6 istisna noktalarinin TAM listesi (aile-disi; taban, d, rakamlar, kanal)
2) n=8 pencere vuruslarinin max tabani (cells_n8.json'dan)
3) n=8 canli hucre / aile tekillestirme sayilari (9 -> 5 dogrulamasi)
4) n=8 uzatma taramasi 61..100: kac tabanda nokta, toplam nokta
"""
import json
from fractions import Fraction
from core import scan_fixed_points, value_from_d, to_digits, d_vector


def tz(d):
    t = 0
    for v in reversed(d):
        if v: break
        t += 1
    return t


def fams_n6(b):
    out = set()
    B = b - 1
    if b % 2 == 0:
        out.add((b // 2, b // 2, 0))                       # palindromik M_b
    for num, den, mk in [((5*B+3, 3*B-1, B+2), 7, b % 7 == 6),
                          ((7*B+5, 5*B+1, B+2), 9, b % 9 == 8)]:
        if mk and all(x % den == 0 for x in num):
            out.add(tuple(x // den for x in num))
    if b % 15 == 10:
        out.add((3*b//5, (b-1)//3, b//5))
    return out


print("=== 1) n=6 istisna noktalari (aile-disi) ===")
tot = famtot = 0
for b in range(2, 61):
    gt = {d_vector(p, 6) for p in scan_fixed_points(b, 6)}
    fams = fams_n6(b)
    tot += len(gt); famtot += len(fams & gt)
    for d in sorted(gt - fams):
        v = value_from_d(list(d), b, 6)
        print(f"  b={b}  d={d}  t={tz(d)}  rakamlar(desc)={sorted(to_digits(v,b),reverse=True)}")
print(f"  GT toplam={tot}, aile uyesi={famtot}, istisna={tot-famtot}")

print("\n=== 2) n=8 pencere vuruslari max taban ===")
c = json.load(open("data/cells_n8.json"))
mx = 0; cnt = 0
for t in c:
    for b, d in c[t].get("window_hits", []):
        mx = max(mx, b); cnt += 1
print(f"  toplam pencere vurusu kaydi: {cnt}, max taban: {mx}")

print("\n=== 3) n=8 t=0 canli hucre -> aile tekillestirme ===")
fams = c["0"]["families"]
cells = [F["cells"] for F in fams]
print(f"  aile sayisi: {len(fams)}, hucre katkilari: {cells}, toplam: {sum(cells)}")
print(f"  (LIVE=9'dan 1'i butunluk-bos dusmustu; 9-1={sum(cells)} mi?)")

print("\n=== 4) n=8 uzatma 61..100 sayilari ===")
nb = 0; npts = 0
for b in range(61, 101):
    g = scan_fixed_points(b, 8)
    if g: nb += 1
    npts += len(g)
print(f"  nokta iceren taban sayisi: {nb}/40, toplam nokta: {npts}")

"""n=10 zemin gercegi taramasi — genel desen icin ilk bakis.

Tamamen kaba kuvvet (core.scan_fixed_points, d-uzayi). Guvenilir; hucre
makinesi/indirgeme YOK. Amac: n=10 konjekturunu (makale Bolum 6) sinamak.
  - t=1 aile boleni h-1 = 4 mu? (yani 4|b cift-taban avantajini geri
    getiriyor mu?)
  - t=0 tek-modullu aileler; moduller ikilenmesi.
Kullanim: python check_n10.py [BMAX]  (varsayilan 45)
"""
import sys
from collections import Counter, defaultdict
from core import scan_fixed_points, d_vector

BMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 45
n, h = 10, 5


def tz(d):
    t = 0
    for v in reversed(d):
        if v:
            break
        t += 1
    return t


hits = {}
rows = []
for b in range(2, BMAX + 1):
    fps = scan_fixed_points(b, n)
    if fps:
        hits[b] = len(fps)
    for sd in fps:
        d = d_vector(sd, n)
        t = tz(d)
        s = sum(sd)
        assert s % (b - 1) == 0, (b, sd)
        rows.append((b, t, s // (b - 1), d))

print(f"n=10, b=2..{BMAX}")
print(f"sabit noktali tabanlar: {sorted(hits)}")
print(f"taban basina sayi: {dict(sorted(hits.items()))}")

evens = [b for b in hits if b % 2 == 0]
odds = [b for b in hits if b % 2 == 1]
print(f"\nCIFT tabanlar: {sorted(evens)}")
print(f"  bunlarin 4'e bolunenleri: {sorted(b for b in evens if b % 4 == 0)}")
print(f"  4'e bolunup sabit noktasi OLMAYAN cift tabanlar: "
      f"{sorted(b for b in range(4, BMAX+1, 4) if b not in hits)}")
print(f"TEK tabanlar: {sorted(odds)}")

kdist = Counter(r[2] for r in rows)
print(f"\nk = ranktoplam/(b-1) dagilimi: {dict(sorted(kdist.items()))}")
ch = Counter(r[1] for r in rows)
print(f"kanal t dagilimi: {dict(sorted(ch.items()))}")

print("\n--- kanal bazinda d-vektorleri (aile avlamak icin) ---")
bych = defaultdict(list)
for b, t, k, d in rows:
    bych[t].append((b, d))
for t in sorted(bych):
    print(f"t={t} (k={h+t}):")
    for b, d in bych[t]:
        print(f"   b={b:2d}  d={d}")

"""Faz 1 — kanal ayristirmasi ve ardil formulu dogrulamasi.

Sembolik turetme (elle cozuldu, ozet):
n=8, sirali rakamlar a0 >= ... >= a7, d_i = a_i - a_{7-i} (i=0..3).
desc - asc sutunlari (buyukten kucuge): d0 d1 d2 d3 -d3 -d2 -d1 -d0.
Odunc zinciri sagdan cozulunce kanallar d'nin SONDAKI sifir sayisina
(t) gore ayrisir:

  t=0 (d3>=1):            [d0, d1, d2, d3-1, B-d3, B-d2, B-d1, b-d0]  toplam 4B
  t=1 (d3=0, d2>=1):      [d0, d1, d2-1, B, B, B-d2, B-d1, b-d0]      toplam 5B
  t=2 (d2=d3=0, d1>=1):   [d0, d1-1, B, B, B, B, B-d1, b-d0]          toplam 6B
  t=3 (d1=d2=d3=0, d0>=1):[d0-1, B, B, B, B, B, B, b-d0]              toplam 7B

Dogrulama: her ground-truth sabit noktasinin d-vektorunu cikar, kanal
formulunun rakam coklu-kumesini birebir yeniden urettigini kontrol et
(PLAN.md Faz 1 adim 2). Ayrica kanal/parite/d-vektoru kesitlerini bas.
"""

import json
import os
import sys
from collections import Counter

from core import d_vector

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "data", "groundtruth_n8.json")

EXPECTED_K = {0: 4, 1: 5, 2: 6, 3: 7}


def trailing_zeros(d):
    t = 0
    for x in reversed(d):
        if x != 0:
            break
        t += 1
    return t


def successor_digits(d, b):
    """Kanal formulu: d-vektorunden ardil rakam listesi (sirasiz)."""
    B = b - 1
    d0, d1, d2, d3 = d
    t = trailing_zeros(d)
    if t == 0:
        return [d0, d1, d2, d3 - 1, B - d3, B - d2, B - d1, b - d0]
    if t == 1:
        return [d0, d1, d2 - 1, B, B, B - d2, B - d1, b - d0]
    if t == 2:
        return [d0, d1 - 1, B, B, B, B, B - d1, b - d0]
    return [d0 - 1, B, B, B, B, B, B, b - d0]


def main():
    with open(DATA) as f:
        gt = {int(b): v for b, v in json.load(f).items()}

    fails = 0
    rows = []          # (b, t, k, d)
    for b, fps in sorted(gt.items()):
        for sd in fps:
            d = d_vector(sd, 8)
            t = trailing_zeros(d)
            k = sum(sd) // (b - 1)
            succ = sorted(successor_digits(d, b), reverse=True)
            if succ != sd:
                fails += 1
                print(f"FORMUL HATASI b={b} d={d} t={t}: "
                      f"formul={succ} != gercek={sd}")
            if k != EXPECTED_K[t]:
                fails += 1
                print(f"TOPLAM HATASI b={b} d={d}: k={k}, beklenen {EXPECTED_K[t]}")
            rows.append((b, t, k, d))

    n = len(rows)
    if fails:
        print(f"\nDURDU: {fails} uyusmazlik / {n} nokta. Turetmeyi duzelt.")
        sys.exit(1)
    print(f"Faz 1 dogrulama: GECTI — {n} noktanin tamami kanal formuluyle "
          f"birebir yeniden uretildi, k=4+t kurali istisnasiz.")

    ch_par = Counter((t, b % 2) for b, t, k, d in rows)
    print("\nkanal x parite (t, tek/cift) sayilari:")
    for (t, p), c in sorted(ch_par.items()):
        print(f"  t={t} {'tek ' if p else 'cift'} taban: {c}")

    print("\nTEK tabanlarin tam dokumu (b, t, d-vektoru):")
    for b, t, k, d in rows:
        if b % 2 == 1:
            print(f"  b={b:2d} t={t} d={d}")

    print("\nCIFT tabanlarin tam dokumu (b, t, d-vektoru):")
    for b, t, k, d in rows:
        if b % 2 == 0:
            print(f"  b={b:2d} t={t} d={d}")


if __name__ == "__main__":
    main()

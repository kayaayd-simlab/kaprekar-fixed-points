"""Faz 0 — zemin dogrulama (ground truth).

1) n=6 tarayiciyi bilinen sonucla dogrula; uyusmazsa cikis kodu 1 ile DUR.
2) n=8 taramasi b <= BMAX (varsayilan 60), cikti: data/groundtruth_n8.json
   format: {b: [sirali-rakam-listeleri]}
3) Ilk gozlemler: tek taban sizintilari, taban basina sayilar,
   rakam toplami katsayilari k = toplam / (b-1).

Kullanim: python phase0_bruteforce.py [BMAX]
"""

import json
import os
import sys
from collections import Counter

from core import scan_fixed_points

# Bilinen n=6 sonucu (PLAN.md Faz 0 adim 2):
KNOWN_ODD_N6 = [13, 17, 25, 27, 35, 41, 53, 55, 69]      # tek tabanlar b < 70
KNOWN_COUNTS_N6 = [2, 0, 3, 0, 3, 0, 2, 0, 2, 0, 1, 1, 1, 0, 1]  # b = 2..16


def verify_n6():
    counts_2_16 = []
    odd_hits = []
    for b in range(2, 70):
        fps = scan_fixed_points(b, 6)
        if b <= 16:
            counts_2_16.append(len(fps))
        if b % 2 == 1 and fps:
            odd_hits.append(b)
    ok = True
    if counts_2_16 != KNOWN_COUNTS_N6:
        ok = False
        print("n=6 DOGRULAMA HATASI: taban basina sayilar (b=2..16)")
        print("  beklenen:", KNOWN_COUNTS_N6)
        print("  bulunan :", counts_2_16)
    if odd_hits != KNOWN_ODD_N6:
        ok = False
        print("n=6 DOGRULAMA HATASI: sabit noktali tek tabanlar (b<70)")
        print("  beklenen:", KNOWN_ODD_N6)
        print("  bulunan :", odd_hits)
    if ok:
        print("n=6 dogrulama: GECTI (b=2..16 sayilari ve b<70 tek tabanlar birebir)")
    return ok


def run_n8(bmax):
    gt = {}
    for b in range(2, bmax + 1):
        gt[b] = scan_fixed_points(b, 8)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "data", "groundtruth_n8.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({str(b): v for b, v in gt.items()}, f)
    print(f"yazildi: {out}")

    # --- kompakt ozet ---
    counts = {b: len(v) for b, v in gt.items()}
    print(f"\nn=8, b=2..{bmax} taban basina sabit nokta sayilari:")
    print(" ", " ".join(f"{b}:{c}" for b, c in counts.items() if c))
    print("  (listede olmayan tabanlarda 0)")

    odd_hits = [b for b in gt if b % 2 == 1 and gt[b]]
    even_miss = [b for b in gt if b % 2 == 0 and not gt[b]]
    print(f"\nsabit noktali TEK tabanlar: {odd_hits}")
    print(f"sabit noktasiz CIFT tabanlar: {even_miss}")

    kdist = Counter()
    for b, fps in gt.items():
        for sd in fps:
            s = sum(sd)
            assert s % (b - 1) == 0, f"Lemma 1 ihlali! b={b} rakamlar={sd}"
            kdist[s // (b - 1)] += 1
    print(f"\nrakam toplami katsayilari k=toplam/(b-1) dagilimi: {dict(kdist)}")
    print("(Lemma 1 kontrolu: tum toplamlar (b-1)'in kati — assert gecti)")

    odd_k = Counter()
    for b in odd_hits:
        for sd in gt[b]:
            odd_k[sum(sd) // (b - 1)] += 1
    print(f"tek tabanlarda k dagilimi: {dict(odd_k)}")


if __name__ == "__main__":
    bmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    if not verify_n6():
        print("\nDURDU: n=6 dogrulamasi gecmeden n=8'e gecilmez (PLAN.md Faz 0).")
        sys.exit(1)
    run_n8(bmax)

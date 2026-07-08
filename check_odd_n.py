"""Tek basamak-sayilari icin varlik kontrolu (makale giris cumlesi icin).

Tek n'de desc-asc'nin orta sutunu sifir oldugundan core'un d-uzayi
taramasi aynen gecerlidir (value_from_d ve d_vector n//2 cift kullanir,
orta rakam katkisizdir). Iddialar:
  n=5: sabit nokta olan tabanlar tam olarak b = 3 (mod 6), b != 9
  n=7: yalniz b=4;   n=9: yalniz b=5   (Thakur, parcacik duzeyinde)
"""
from core import scan_fixed_points

for n, bmax in ((5, 60), (7, 40), (9, 30)):
    hits = [b for b in range(2, bmax + 1) if scan_fixed_points(b, n)]
    print(f"n={n}, b<={bmax}: {hits}")

pred5 = [b for b in range(2, 61) if b % 6 == 3 and b != 9]
hits5 = [b for b in range(2, 61) if scan_fixed_points(b, 5)]
print("n=5 iddiasi (b=3 mod 6, b!=9) birebir mi:", hits5 == pred5)

"""Kaprekar cekirdegi — tanimlarin TEK dogruluk kaynagi.

Notasyon (PLAN.md ile ayni):
  B := b - 1   (rakam tamamlayicisi)
  C := b + 1   (ikileme koordinati)
DIKKAT: B ile C'yi karistirma. b -> 2b+1 altinda B -> 2B+2 ama C -> 2C.

Sabit nokta tanimi: K_b(x) = x, x pozitif ve taban-b'de TAM n basamakli
(basta sifir yok). Repdigit -> 0 onemsizi otomatik dislanir (0 < b^(n-1)).

d-uzayi taramasinin dayanagi: K_b(x) yalniz x'in siralanmis rakamlarinin
tamamlayici cift farklarina baglidir:
  d_i = a_i - a_{n-1-i},  i = 0..n/2-1,  a_0 >= a_1 >= ... >= a_{n-1}
ve desc - asc = sum_i d_i * (b^(n-1-i) - b^i).
Siralilik geregi d_0 >= d_1 >= ... >= d_{n/2-1} >= 0 kendiliginden saglanir.
x sabit nokta  <=>  x = deger(d(x)); bu yuzden d-konisini taramak tamdir.
"""

from itertools import combinations_with_replacement


def to_digits(v, b):
    """v'nin taban-b rakamlari, en anlamlidan en anlamsiza."""
    if v == 0:
        return [0]
    ds = []
    while v:
        ds.append(v % b)
        v //= b
    return ds[::-1]


def value_from_d(d, b, n):
    """Fark vektoru d (uzunluk n//2) icin desc - asc degeri."""
    return sum(di * (b ** (n - 1 - i) - b ** i) for i, di in enumerate(d))


def d_vector(sorted_desc, n):
    """Buyukten kucuge sirali rakam listesinin fark vektoru."""
    return tuple(sorted_desc[i] - sorted_desc[n - 1 - i] for i in range(n // 2))


def scan_fixed_points(b, n):
    """Taban b'de TAM n basamakli tum Kaprekar sabit noktalari.

    d-uzayi taramasi, O(b^(n/2) / (n/2)!) aday. Donen deger:
    buyukten kucuge sirali rakam listeleri (sirali, tekrarsiz).
    """
    m = n // 2
    lo = b ** (n - 1)
    found = []
    for asc in combinations_with_replacement(range(b), m):
        d = asc[::-1]  # d0 >= d1 >= ... >= d_{m-1}
        if d[0] == 0:
            continue  # repdigit -> K = 0
        v = value_from_d(d, b, n)
        if v < lo:
            continue  # n basamaktan az: basta sifir demek, gecersiz
        digs = to_digits(v, b)
        if len(digs) != n:
            continue
        sd = sorted(digs, reverse=True)
        if d_vector(sd, n) == d:
            found.append(sd)
    found.sort()
    return found

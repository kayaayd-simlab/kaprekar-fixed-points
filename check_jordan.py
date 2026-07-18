"""V1/V2 — Jordan (1964) ailelerini bizim ailelerle carpistir.

REVIZE-V2.md'nin Jordan iddialarini BAGIMSIZ dogrula (Jordan'in metnine
degil, bizim kesin K_b hesabimiza dayanarak). Uyusmazlik cikarsa DUR.

Jordan konvansiyonu: taban = "n", rakam sayisi = "m". Bizde taban=b, uzunluk=n.
Jordan'in mod-15 ailesi (taban b=15g+10, m=2K): elle dogrulandi = bizim
b=10(15) ailesi. Burada makineyle teyit + digerleri.
"""
from fractions import Fraction
from core import value_from_d, to_digits, d_vector

FAIL = 0


def is_fp(d, b, n):
    """K_b(x)=x mi — dogrudan, kisayolsuz. d tam sayi tuple."""
    if any((not isinstance(x, int)) for x in d):
        return False
    if not (b - 1 >= d[0] >= 1) or d[-1] < 0:
        return False
    if any(d[i] < d[i + 1] for i in range(len(d) - 1)):
        return False
    v = value_from_d(d, b, n)
    if v < b ** (n - 1):
        return False
    digs = to_digits(v, b)
    return len(digs) == n and d_vector(sorted(digs, reverse=True), n) == tuple(d)


def frac_ok(*vals):
    return all(v.denominator == 1 for v in vals)


# ---- bizim aileler (kesirli), h=n//2 ----
def fam_mod15(b, n):           # b=10(15) genel aile (= Jordan mod-15)
    # makale formulu B=b-1 ile: d0=(3B+3)/5 = 3b/5, orta B/3=(b-1)/3,
    # son (B+1)/5 = b/5.  (Ilk surumde b/B karistirilmisti — tuzak #1!)
    h = n // 2
    vals = [Fraction(3*b, 5)] + [Fraction(b-1, 3)]*(h-2) + [Fraction(b, 5)]
    return tuple(int(x) for x in vals) if frac_ok(*vals) else None

def fam_mod7_n6(b):            # n=6 b=6(7)
    B = Fraction(b-1)
    vals = [ (5*B+3)/7, (3*B-1)/7, (B+2)/7 ]
    return tuple(int(x) for x in vals) if frac_ok(*vals) else None

def fam_mod9_n6(b):            # n=6 b=8(9)
    B = Fraction(b-1)
    vals = [ (7*B+5)/9, (5*B+1)/9, (B+2)/9 ]
    return tuple(int(x) for x in vals) if frac_ok(*vals) else None

def fam_mod17a_n8(b):          # n=8 b=11(17)
    B = Fraction(b-1)
    vals = [ (11*B+9)/17, (7*B-2)/17, (5*B+1)/17, (3*B+4)/17 ]
    return tuple(int(x) for x in vals) if frac_ok(*vals) else None


print("=== A) Jordan'in n=55 CIFT ornegi (m=6) ===")
# sirali desc rakamlardan d: d_i = a_i - a_{5-i}
seq1 = [43, 36, 33, 22, 18, 10]     # d beklenen (33,18,11)
seq2 = [46, 39, 31, 23, 16, 7]      # d beklenen (39,23,8)
for seq, tag in [(seq1, "mod-15"), (seq2, "mod-7")]:
    d = d_vector(seq, 6)
    ok = is_fp(list(d), 55, 6)
    print(f"  {tag}: sirali={seq} d={d} sabit-nokta? {'EVET' if ok else 'HAYIR'}")
    if not ok: FAIL += 1
print(f"  bizim mod-15(b=55) = {fam_mod15(55,6)}  (Jordan seq1 d=(33,18,11))")
print(f"  bizim mod-7 (b=55) = {fam_mod7_n6(55)}  (Jordan seq2 d=(39,23,8))")
if fam_mod15(55,6) != (33,18,11): FAIL += 1
if fam_mod7_n6(55) != (39,23,8): FAIL += 1

print("\n=== B) Jordan R_13 = {10,9,7,5,4,1}, taban 13, m=6 ===")
d13 = d_vector([10,9,7,5,4,1], 6)
ok = is_fp(list(d13), 13, 6)
print(f"  d={d13} sabit-nokta? {'EVET' if ok else 'HAYIR'};  bizim mod-7(b=13)={fam_mod7_n6(13)}")
if not ok or fam_mod7_n6(13) != d13: FAIL += 1

print("\n=== C) mod-15 ailesi = Jordan, cift n=6..12, g=0..40 ===")
allc = True
for n in (6, 8, 10, 12):
    for g in range(0, 41):
        b = 15*g + 10
        d = fam_mod15(b, n)
        # Jordan R_n formulu: {7+12g,[6+10g]x(K-2),6+9g,4+6g,[3+5g]x(K-2),1+3g}
        K = n // 2
        Rsorted = [7+12*g] + [6+10*g]*(K-2) + [6+9*g, 4+6*g] + [3+5*g]*(K-2) + [1+3*g]
        jd = d_vector(sorted(Rsorted, reverse=True), n)
        if d != jd or not is_fp(list(d), b, n):
            allc = False; FAIL += 1
            print(f"  !!! n={n} g={g} b={b}: bizim {d} vs Jordan {jd}")
print(f"  n=6..12, g=0..40: {'HEPSI OZDES ve sabit-nokta' if allc else 'UYUSMAZLIK'}")

print("\n=== D) Jordan mod-51 (n=8) BIZIM b=11(17) ailesinin ALT-dizisi mi? ===")
# 28 = 11 (mod 17)? 28 = 1 (mod 3)?
print(f"  28 mod 17 = {28%17} (11 olmali); 28 mod 3 = {28%3} (1 olmali)")
print("  yani Jordan mod-51 = bizim b=11(17) KESIS b=1(3), 1/3 yogunluk.")
# gercek genisleme: b=11(17) ama 1(3) OLMAYAN uyeler yine sabit-nokta mi?
extension = []
for b in range(11, 400):
    if b % 17 == 11 and b % 3 != 1:      # bizde var, Jordan mod-51'de YOK
        d = fam_mod17a_n8(b)
        if d and is_fp(list(d), b, 8):
            extension.append(b)
print(f"  b=11(17) ama Jordan mod-51 disi, gercek n=8 sabit-nokta veren tabanlar: {extension[:8]}...")
print(f"  -> bizim aile Jordan'i GERCEKTEN genisletiyor: {'EVET' if extension else 'HAYIR'}")
if not extension: FAIL += 1

print("\n=== E) Corollary aritmetigi ===")
from math import gcd
def lcm(a,b): return a*b//gcd(a,b)
L = 1
for m in (3,15,17,21): L = lcm(L, m)
print(f"  lcm(3,15,17,21) = {L}  (Jordan Cor.3 mod-1785 ile ayni mi: {L==1785})")
print(f"  55 mod 15 = {55%15} (10?), 55 mod 7 = {55%7} (6?) -> Cor.2 mod-105 = mod15 KESIS mod7")
if L != 1785: FAIL += 1
if not (55%15==10 and 55%7==6): FAIL += 1

print(f"\nSONUC: {'GECTI - tum Jordan iddialari bizim kodla dogrulandi' if FAIL==0 else f'KALDI ({FAIL} uyusmazlik) - METNI DEGISTIRME'}")

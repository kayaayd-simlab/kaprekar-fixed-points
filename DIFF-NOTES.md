# DIFF-NOTES — v1 → v2 (July 2026)

Record of every change made in revision v2 of *Bases admitting six- and
eight-digit Kaprekar fixed points*, with reasons. No theorem, proof, table
formula, or computation changed; v2 changes the historical framing, the
attribution, and adds previously requested data points to the text.

## Trigger

J. H. Jordan, "Self-producing sequences of digits", *Amer. Math. Monthly*
71 (1964), 61–64, was located and read in full (primary source). Jordan
constructs infinite families of bases admitting even-length Kaprekar
fixed points — including some of ours — and explicitly leaves the general
characterization open ("a general formula would be desirable").

Every Jordan-related claim below was machine-verified in exact arithmetic
(`check_jordan.py`, verdict `SONUC: GECTI`) before any text was touched:

- Jordan's `n = 10 + 15g` family (his Theorem 1, Case 2) is *identical*
  to our `b ≡ 10 (mod 15)` family for n = 6 (K = 3) and n = 8 (K = 4),
  checked for g = 0..40 / b ≤ 1000.
- Jordan's `n = 13 + 21g` parametrization coincides with our
  `b ≡ 13 (mod 21)` family (n = 8), b ≤ 1000.
- Jordan's `n = 28 + 51g` progression is a one-third-density
  subprogression of our `b ≡ 11 (mod 17)` family; the containment is
  strict (b = 11, 45, 62, … are members of ours outside his).
- His R_13 example and his base-55 double example match our family
  members at b = 13 and b = 55 digit-for-digit.
- lcm(3, 15, 17, 21) = 1785 = the modulus in his Corollary 3 = our n = 8
  density period.

## Changes in the manuscript (paper/kaprekar_kfp_n6_n8.tex)

1. **Introduction reframed.** Old claim "the even lengths n ≥ 6 have
   remained open" replaced: the existence direction goes back to Jordan
   (1964) (mod 15 / 21 / 51 families, the b = 13 six-digit example, the
   b = 55 double point); what remained open since 1964 is whether those
   lists are *complete*. The paper is now framed as completing the
   classification ("only if") for the first two even lengths. Reason:
   accuracy of the priority claim.
2. **Abstract.** Added: "The existence halves of these classifications
   refine infinite families constructed by Jordan in 1964; the
   completeness halves are, to our knowledge, new."
3. **Convention footnote.** Jordan works with digit multisets and allows
   leading zeros; we classify positive integers. The difference matters
   only marginally (e.g. his m = 3 result includes b = 2, empty in our
   convention).
4. **Table 1 and Table 2 captions** now carry origin notes, only at the
   verified level: mod-15 = Jordan's family; mod-21 the same progression
   as his; our mod-17 (residue 11) contains his mod-51 as a strict
   subprogression; the mod-9, general mod-7, 2|b, 3|b, 12 (mod 15) and
   14 (mod 17) families "appear to be new".
5. **Reference order fixed:** "Prichett and Hasse" → "Hasse and
   Prichett" (verified against the 1979 Lapenta–Ludington–Prichett
   bibliography), and the LLP sentence now notes the line going back to
   Jordan, whose base-ten corollary prefigures Prichett–Ludington–Lapenta.
6. **n = 5 sentence:** the 3|b direction noted as consistent with
   Jordan's odd-length construction (m = 5, K = 3).
7. **Remark (n = 10):** the cross-length persistence of the mod-15
   family acknowledged as implicit in Jordan's K-parametrized family.
8. **New reference** \bibitem{Jordan64}, cited 5 times; cite/bibitem
   integrity checked (12/12 keys, no orphans).
9. **n = 6 exceptional points now listed explicitly** (previously only
   "confined to b ≤ 10"): difference vectors (1,1,1) at b = 2; (3,1,1)
   and (3,3,1) at b = 4; (5,3,1) at b = 6. Theorem statement tightened
   to "four exceptional points confined to b ∈ {2,4,6}". Source:
   fresh exact scan (`check_v2_data.py`), GT 52 = 48 family + 4.
10. **n = 8 cell-census sentence expanded** with verified numbers:
    deduplication criterion made precise (cells sharing an identical
    solution merge; the b ≡ 10 (mod 15) family arises in 4 cells via its
    tied B/3 components; four families in one cell each; one live cell
    eliminated by integrality), and the 505 bounded windows quantified
    (15 window hits in total, none beyond b = 14).
11. **Extension-scan numbers added** (one line): for 61 ≤ b ≤ 100,
    22 of 40 bases admit eight-digit fixed points, 26 points in all,
    each a predicted family member.
12. **t = 3 off-by-one footnote** added to the one-way-door paragraph:
    the ancillary code uses d0 ≥ 1 where d0 ≥ 2 would be sharp — the
    safe direction (can only over-scan), and the channel is empty anyway.

## Changes in README.md

- "machine-checkable proof pipeline" → "fully reproducible
  exact-arithmetic computational proof pipeline" (avoids suggesting a
  Lean/Coq-style formal verification).
- `genpipe.py` description now states its scope precisely: complete
  proof when every underdetermined cell has free dimension ≤ 1 (the case
  for n = 6 and n = 8); higher-dimensional cells only scanned to
  b ≤ 400 and flagged via `n_open`.

## What did NOT change

Both theorems, all family tables and d-vector formulas, the cell
censuses, the LP closure, the audits, all code in the proof path, and
all data files. `check_jordan.py` and `check_v2_data.py` are new,
verification-only additions.

## Suggested arXiv v2 comment

> v2: historical framing corrected — the existence families refine
> constructions of J. H. Jordan (Amer. Math. Monthly 71 (1964), 61–64);
> results unchanged, now stated as a completeness theorem. Added explicit
> n=6 exceptional points and minor verified data.

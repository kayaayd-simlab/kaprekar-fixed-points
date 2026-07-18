# Six- and eight-digit Kaprekar fixed points: a complete base classification

This repository contains the fully reproducible exact-arithmetic computational proof pipeline behind the paper

> **Bases admitting six- and eight-digit Kaprekar fixed points: a complete congruence classification**
> Aydın Kaya (independent researcher), 2026.

Everything here is **exact**: all computations use Python's `fractions.Fraction` and arbitrary-precision integers. There is no floating-point arithmetic anywhere in the proof path. The point of publishing the code is simple — anyone who wants to check the results can run them and watch each stage print a `PASS`/`FAIL` verdict.

## The results

For a base `b ≥ 2` and a number with exactly `n` digits in base `b`, the **Kaprekar map** sorts the digits into descending and ascending order and subtracts. A **fixed point** is a number left unchanged by this map. (This is weaker than being a *Kaprekar constant* like 6174 in base 10 — a fixed point only has to be stable, not to attract every other number.)

**Theorem (n = 6).** A base `b` admits a six-digit Kaprekar fixed point **iff**

```
2 | b   or   b ≡ 6 (mod 7)   or   b ≡ 8 (mod 9)   or   b ≡ 10 (mod 15).
```

**Theorem (n = 8).** A base `b` admits an eight-digit Kaprekar fixed point **iff**

```
3 | b   or   b ≡ 10,12 (mod 15)   or   b ≡ 11,14 (mod 17)
        or   b ≡ 13 (mod 21)      or   b ∈ {2, 4, 8}.
```

In both cases every fixed point is given by an explicit family, linear in `b`, together with a finite set of exceptions confined to `b ≤ 10`. See the paper for the family tables and the structural comparison between the two lengths.

A concrete illustration: base 10 has exactly two eight-digit fixed points, `63317664` and `97508421`. The first is the smallest member of the infinite `b ≡ 10 (mod 15)` family; the second belongs to no family at all — a genuine small-base exception.

## How the proof works

1. The Kaprekar map depends only on the differences between digits at symmetric positions. Resolving the borrow chain gives an exact *successor formula* (elementary; no computer needed).
2. Each ordering of the `n` output expressions is a **cell** — a small linear system `A·d = B·c + e` over the rationals. Solving all `n!` cells exactly classifies every possible fixed point.
3. Cells with a free parameter are closed by an **exact two-variable linear program** (vertex enumeration over `ℚ`), which *proves* rather than checks that no larger base hides a surprise.
4. Two safeguards keep it airtight: every **existence** claim is sealed by directly evaluating `K(x)=x`; every **emptiness** claim uses only provably necessary inequalities. An off-by-one can cost efficiency but never correctness.
5. Everything is anchored to an exhaustive ground-truth scan (`b ≤ 60`), an extension scan beyond the construction range, and an independent audit that re-derives cell verdicts through a completely different route.

## Files

All Python scripts live at the repository root because they import one another; `data/` must stay alongside them.

| File | What it does |
|------|--------------|
| `core.py` | The Kaprekar map and the difference-vector ("d-space") ground-truth scanner. |
| `genpipe.py` | **General even-`n` pipeline.** Runs the whole classification for any even `n`. The result is a complete proof when every underdetermined cell has free dimension ≤ 1 (the case for `n = 6` and `n = 8`); higher-dimensional cells are only scanned up to `b ≤ 400` and reported via the `n_open` flag. Usage: `python genpipe.py 6 60 150` or `python genpipe.py 8 60 100`. |
| `phase0_bruteforce.py` | `n=8` ground-truth scan + verification against the known `n=6` result. |
| `phase1_channels.py` | `n=8` channel decomposition / successor-formula check. |
| `phase2_cells.py` | `n=8` full cell classification (exact rational RREF over all `8!` cells). |
| `phase3_synthesis.py` | `n=8` closure of underdetermined cells + extension comparison. |
| `phase3b_lp.py` | Exact 2-variable LP closure of the free-parameter cells. |
| `phase_audit.py` | Independent audit: naive full-range brute force + RREF-free verdict re-derivation. |
| `check_odd_n.py` | Existence scan for odd lengths `n = 5, 7, 9` (context for the introduction). |
| `data/groundtruth_n8.json` | All `n=8` fixed points for `b ≤ 60`. |
| `data/cells_n8.json` | The complete `n=8` cell classification. |
| `data/phase3b_lp.json` | Output of the exact LP closure. |
| `paper/kaprekar_kfp_n6_n8.tex` | The manuscript (LaTeX, `amsart`). |
| `RESULTS.md`, `RESULTS_n6.md`, `PLAN.md` | Detailed working notes (in Turkish) documenting the full process. |

## Reproducing the results

Requires only **Python 3** — no third-party packages (exact arithmetic uses the standard-library `fractions` module).

```bash
python genpipe.py 6 60 150     # reproduces the n=6 theorem end to end
python genpipe.py 8 60 100     # runs the n=8 pipeline structure
python phase0_bruteforce.py 60
python phase2_cells.py
python phase3_synthesis.py closure
python phase3_synthesis.py gtext
python phase3b_lp.py
python phase_audit.py
```

Each script ends with a machine-checkable verdict. The scripts were written in Turkish, so the verdict line reads **`SONUC: GECTI`** (= *PASSED*) or **`SONUC: KALDI`** (= *FAILED*). A clean run prints `GECTI` everywhere.

As one cross-check worth highlighting: the `n=6` run reproduces the cell census `568 / 140 / 12` (unique / inconsistent / underdetermined) found independently in the author's original 2026 computation — two separate implementations landing on the same cell topology.

## On the use of AI

This work was done in an extended collaboration with Anthropic's Claude models, and I'd rather state that plainly than bury it. The six-digit classification was originally worked out with Claude Opus; the eight-digit generalization, the exact-closure arguments, the independent audits, and the write-up were developed with Claude (Fable 5).

I directed the research, set the verification standards, and take full responsibility for the contents. What makes me comfortable publishing this openly is exactly what's in this repository: every mathematical claim is verified in exact arithmetic, cross-validated against an independent brute-force scan, and audited by re-deriving results through a different computational route. The code is here precisely so that the proof stands on its own, regardless of how it was written. Check it.

## License

MIT — see [LICENSE](LICENSE). Use, run, and verify freely.

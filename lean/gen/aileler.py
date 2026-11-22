"""n=8 altı aile için Lean ispatı üretir (RESULTS.md Bölüm 2)."""
import sympy as sp, itertools
m = sp.symbols('m')
R = sp.Rational
# (ad, kanal, modül, kalıntı, d-vektörü B cinsinden)
F = [
 ("aile1",1,3,0, lambda B:[(2*B+2)/3,(2*B-1)/3,(B+1)/3]),
 ("aile2",0,15,10,lambda B:[(3*B+3)/5,B/3,B/3,(B+1)/5]),
 ("aile3",0,15,12,lambda B:[(13*B+7)/15,(11*B-1)/15,(7*B-2)/15,(B+4)/15]),
 ("aile4",0,17,11,lambda B:[(11*B+9)/17,(7*B-2)/17,(5*B+1)/17,(3*B+4)/17]),
 ("aile5",0,17,14,lambda B:[(15*B+9)/17,(13*B+1)/17,(9*B+2)/17,(B+4)/17]),
 ("aile6",0,21,13,lambda B:[(5*B+3)/7,(3*B-1)/7,B/3,(B+2)/7]),
]
def lin(e):
    e=sp.expand(e); a=e.coeff(m,1); c=e.coeff(m,0)
    assert a.is_integer and c.is_integer and a>=0 and c>=0, e
    return int(a),int(c)
def s(v): return f"{v[0]}*m+{v[1]}"
def val(v,mm): return v[0]*mm+v[1]

out=[]
for name,t,M,r,dv in F:
    r0 = r if r>0 else M          # ilk taban (aile1: 3)
    b = M*m + r0; B = b-1
    d = [sp.nsimplify(x) for x in dv(sp.Symbol('B'))]
    d = [x.subs('B',B) for x in d]
    if t==0: L=[d[0],d[1],d[2],d[3]-1,B-d[3],B-d[2],B-d[1],b-d[0]]
    else:    L=[d[0],d[1],d[2]-1,B,B,B-d[2],B-d[1],b-d[0]]
    L=[lin(x) for x in L]
    bl=lin(b); bs=f"({s(bl)})"
    # m0: tüm karşılaştırmalar kesinleşsin
    m0=0
    for p,q in itertools.combinations(set(L),2):
        # p-q lineer; işaret değiştiği noktadan sonrası sabit
        for mm in range(0,500):
            sg=[ (val(p,k)<=val(q,k), val(q,k)<=val(p,k)) for k in range(mm,mm+400)]
            if all(x==sg[0] for x in sg): m0=max(m0,mm); break
    asc=sorted(L,key=lambda v:val(v,m0+1000)); desc=asc[::-1]
    # ödünç zinciri
    e=[];ee=0
    for k in range(8):
        ee=sp.expand(ee*(M*m+r0)+(desc[k][0]*m+desc[k][1])-(L[k][0]*m+L[k][1])-(asc[k][0]*m+asc[k][1]))
        assert ee.is_integer and ee>=0, (name,k,ee); e.append(int(ee))
    assert e[-1]==0
    Ln="L"+name[4:]
    fd = "fromD0" if t==0 else "fromD1"
    chain=[f"  have h1 : ({s(desc[0])}) = ({s(L[0])}) + ({s(asc[0])}) + {e[0]} := by omega"]
    for k in range(1,8):
        chain.append(f"  have h{k+1} := borrow_step (b := {bs}) (d := {s(desc[k])}) (x := {s(L[k])}) (s := {s(asc[k])}) (e' := {e[k]}) h{k} (by omega)")
    small = ""
    if m0>0:
        cases=" | ".join(["h"]*1)
        small=f"""  rcases Nat.lt_or_ge m {m0} with h | h
  · have : {' ∨ '.join(f'm = {i}' for i in range(m0))} := by omega
    rcases this with {' | '.join(['rfl']*m0)} <;> decide
  · exact {name}_sabit_pos m h"""
    else:
        small=f"  exact {name}_sabit_pos m (Nat.zero_le m)"
    out.append(f'''
/-! ------------------------------------------------------------
  ## {name.capitalize()} (t={t}): b ≡ {r} (mod {M}), yani b = {M}m + {r0}
  Basamaklar: [{", ".join(s(v) for v in L)}]
  Ödünç zinciri: {e}{"" if m0==0 else f"   (m < {m0} durumları ayrıca kontrol edildi)"}
  ------------------------------------------------------------ -/

def {Ln} (m : Nat) : List Nat := [{", ".join(s(v) for v in L)}]

theorem {name}_eq (m : Nat) : {name} {bs} = {Ln} m := by
  simp only [{name}, {fd}, {Ln}, List.cons.injEq, and_true]
  omega

theorem {name}_sabit_pos (m : Nat) (hm : {m0} ≤ m) :
    kaprekar {bs} 8 (ofDigits {bs} ({Ln} m)) = ofDigits {bs} ({Ln} m) := by
  simp only [kaprekar, {Ln}, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
{chr(10).join(chain)}
  omega

theorem {name}_sabit (m : Nat) :
    kaprekar {bs} 8 (ofDigits {bs} ({Ln} m)) = ofDigits {bs} ({Ln} m) := by
{small}

/-- {name.capitalize()}: koşulu sağlayan HER b ≥ {r0} tabanında sabit nokta. -/
theorem {name}_her_taban (b : Nat) (hb : b % {M} = {r}) (h : {r0} ≤ b) :
    kaprekar b 8 (ofDigits b ({name} b)) = ofDigits b ({name} b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = {M}*m + {r0} := ⟨(b - {r0}) / {M}, by omega⟩
  rw [{name}_eq]
  exact {name}_sabit m

theorem {name}_basamak_gecerli (m : Nat) :
    ({Ln} m).all (· < {bs}) = true ∧ ({Ln} m).head? ≠ some 0 := by
  simp only [{Ln}, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega
''')
    print(name, "m0 =", m0, "ödünç =", e)

src=open('Kaprekar.lean').read()
base=src.split('/-! ## Teorem 1')[0]
fam=src.split('/-! ============================================================\n  # Makale')[1].split('/-! Örnek')[0]
fam='/-! ============================================================\n  # Makale'+fam
header='''/-
  Kaprekar sabit noktaları, n = 8: altı ailenin VARLIK yönü, her taban için.
  Kaynak: kaprekar-fixed-points / RESULTS.md, Bölüm 2.
  Lean 4.24, Mathlib yok. native_decide ve sorry kullanılmıyor.
-/
'''
lem='''
/-! # Yardımcı lemmalar -/

/-- Basamak ayırma: r < b ise (q*b + r)'nin son basamağı r, kalanı q. -/
theorem digits_step (b n q r : Nat) (hr : r < b) :
    digits b (n+1) (q*b + r) = r :: digits b n q := by
  have hb : 0 < b := by omega
  simp only [digits]
  have h1 : (q*b + r) % b = r := by
    rw [Nat.add_comm, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hr]
  have h2 : (q*b + r) / b = q := by
    rw [Nat.add_comm, Nat.add_mul_div_right _ _ hb, Nat.div_eq_of_lt hr, Nat.zero_add]
  rw [h1, h2]

theorem digits_one (b r : Nat) (hr : r < b) : digits b 1 r = [r] := by
  simp only [digits, Nat.mod_eq_of_lt hr]

/-- Ödünç adımı: D = X + S + e ve e*b + d = x + s + e' ise, bir basamak sonra
    ilişki e' ödüncüyle sürer. "Büyük − küçük = sayı" eşitliği bununla kurulur. -/
theorem borrow_step {b D X S d x s e e' : Nat} (h : D = X + S + e)
    (hd : e*b + d = x + s + e') : D*b + d = (X*b + x) + (S*b + s) + e' := by
  subst h; rw [Nat.add_mul, Nat.add_mul]; omega
'''
fin='\n'+'\n'.join(f'#print axioms {n}_her_taban' for n,*_ in F)+'\n'
open('Aileler.lean','w').write(header+base.split('-/',1)[1]+fam+lem+''.join(out)+fin)

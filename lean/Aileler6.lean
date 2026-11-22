/-
  Kaprekar sabit noktaları, n = 6: dört ailenin VARLIK yönü, her taban için.
  Kaynak: kaprekar-fixed-points / RESULTS_n6.md, Bölüm 1.
  Lean 4.24, Mathlib yok. native_decide ve sorry kullanılmıyor.
-/


/-- x'in b tabanındaki n basamağı, en düşük basamak başta olacak şekilde. -/
def digits (b : Nat) : Nat → Nat → List Nat
  | 0,     _ => []
  | n + 1, x => (x % b) :: digits b n (x / b)

/-- Basamak listesinden sayıyı geri kur (ilk eleman en yüksek basamak). -/
def ofDigits (b : Nat) (ds : List Nat) : Nat :=
  ds.foldl (fun acc d => acc * b + d) 0

/-- Basit araya ekleyerek sıralama (artan). -/
def insertSorted (a : Nat) : List Nat → List Nat
  | []      => [a]
  | h :: t  => if a ≤ h then a :: h :: t else h :: insertSorted a t

def sortAsc : List Nat → List Nat
  | []     => []
  | h :: t => insertSorted h (sortAsc t)

/-- Kaprekar fonksiyonu. -/
def kaprekar (b n x : Nat) : Nat :=
  let asc := sortAsc (digits b n x)
  ofDigits b asc.reverse - ofDigits b asc

/-- Bütün basamaklar aynı mı? (1111, 2222 gibi) -/
def repdigit (b n x : Nat) : Bool :=
  match digits b n x with
  | []     => true
  | d :: t => t.all (· == d)

/-- k kez uygulama. -/
def iter (f : Nat → Nat) : Nat → Nat → Nat
  | 0,     x => x
  | k + 1, x => iter f k (f x)


/-! # n = 6 kanal ardıl formülleri (B := b - 1)
   t=0: [d0, d1, d2-1, B-d2, B-d1, b-d0]
   t=1: [d0, d1-1, B, B, B-d1, b-d0] -/
def fromD0_6 (b d0 d1 d2 : Nat) : List Nat :=
  let B := b - 1
  [d0, d1, d2 - 1, B - d2, B - d1, b - d0]

def fromD1_6 (b d0 d1 : Nat) : List Nat :=
  let B := b - 1
  [d0, d1 - 1, B, B, B - d1, b - d0]

/-- Bilinen 10 tabanı örnekleri -/
theorem k549945 : kaprekar 10 6 549945 = 549945 := by decide
theorem k631764 : kaprekar 10 6 631764 = 631764 := by decide

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

/-- RESULTS_n6.md formülü -/
def altiA (b : Nat) : List Nat := let B := b - 1
  fromD1_6 b ((B+1)/2) ((B+1)/2)

/-! ------------------------------------------------------------
  ## Altia (t=1): b ≡ 0 (mod 2), yani b = 2m + 2
  Basamaklar: [1*m+1, 1*m+0, 2*m+1, 2*m+1, 1*m+0, 1*m+1]
  Ödünç zinciri: [0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def LaltiA (m : Nat) : List Nat := [1*m+1, 1*m+0, 2*m+1, 2*m+1, 1*m+0, 1*m+1]

theorem altiA_eq (m : Nat) : altiA (2*m+2) = LaltiA m := by
  simp only [altiA, fromD1_6, LaltiA, List.cons.injEq, and_true]
  omega

theorem altiA_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (2*m+2) 6 (ofDigits (2*m+2) (LaltiA m)) = ofDigits (2*m+2) (LaltiA m) := by
  simp only [kaprekar, LaltiA, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (2*m+1) = (1*m+1) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (2*m+2)) (d := 2*m+1) (x := 1*m+0) (s := 1*m+0) (e' := 1) h1 (by omega)
  have h3 := borrow_step (b := (2*m+2)) (d := 1*m+1) (x := 2*m+1) (s := 1*m+1) (e' := 1) h2 (by omega)
  have h4 := borrow_step (b := (2*m+2)) (d := 1*m+1) (x := 2*m+1) (s := 1*m+1) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (2*m+2)) (d := 1*m+0) (x := 1*m+0) (s := 2*m+1) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (2*m+2)) (d := 1*m+0) (x := 1*m+1) (s := 2*m+1) (e' := 0) h5 (by omega)
  omega

theorem altiA_sabit (m : Nat) :
    kaprekar (2*m+2) 6 (ofDigits (2*m+2) (LaltiA m)) = ofDigits (2*m+2) (LaltiA m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact altiA_sabit_pos m h

/-- Altia: koşulu sağlayan HER b ≥ 2 tabanında sabit nokta. -/
theorem altiA_her_taban (b : Nat) (hb : b % 2 = 0) (h : 2 ≤ b) :
    kaprekar b 6 (ofDigits b (altiA b)) = ofDigits b (altiA b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 2*m + 2 := ⟨(b - 2) / 2, by omega⟩
  rw [altiA_eq]
  exact altiA_sabit m

theorem altiA_basamak_gecerli (m : Nat) :
    (LaltiA m).all (· < (2*m+2)) = true ∧ (LaltiA m).head? ≠ some 0 := by
  simp only [LaltiA, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-- RESULTS_n6.md formülü -/
def altiB (b : Nat) : List Nat := let B := b - 1
  fromD0_6 b ((5*B+3)/7) ((3*B-1)/7) ((B+2)/7)

/-! ------------------------------------------------------------
  ## Altib (t=0): b ≡ 6 (mod 7), yani b = 7m + 6
  Basamaklar: [5*m+4, 3*m+2, 1*m+0, 6*m+4, 4*m+3, 2*m+2]
  Ödünç zinciri: [0, 0, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def LaltiB (m : Nat) : List Nat := [5*m+4, 3*m+2, 1*m+0, 6*m+4, 4*m+3, 2*m+2]

theorem altiB_eq (m : Nat) : altiB (7*m+6) = LaltiB m := by
  simp only [altiB, fromD0_6, LaltiB, List.cons.injEq, and_true]
  omega

theorem altiB_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (7*m+6) 6 (ofDigits (7*m+6) (LaltiB m)) = ofDigits (7*m+6) (LaltiB m) := by
  simp only [kaprekar, LaltiB, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (6*m+4) = (5*m+4) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (7*m+6)) (d := 5*m+4) (x := 3*m+2) (s := 2*m+2) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (7*m+6)) (d := 4*m+3) (x := 1*m+0) (s := 3*m+2) (e' := 1) h2 (by omega)
  have h4 := borrow_step (b := (7*m+6)) (d := 3*m+2) (x := 6*m+4) (s := 4*m+3) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (7*m+6)) (d := 2*m+2) (x := 4*m+3) (s := 5*m+4) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (7*m+6)) (d := 1*m+0) (x := 2*m+2) (s := 6*m+4) (e' := 0) h5 (by omega)
  omega

theorem altiB_sabit (m : Nat) :
    kaprekar (7*m+6) 6 (ofDigits (7*m+6) (LaltiB m)) = ofDigits (7*m+6) (LaltiB m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact altiB_sabit_pos m h

/-- Altib: koşulu sağlayan HER b ≥ 6 tabanında sabit nokta. -/
theorem altiB_her_taban (b : Nat) (hb : b % 7 = 6) (h : 6 ≤ b) :
    kaprekar b 6 (ofDigits b (altiB b)) = ofDigits b (altiB b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 7*m + 6 := ⟨(b - 6) / 7, by omega⟩
  rw [altiB_eq]
  exact altiB_sabit m

theorem altiB_basamak_gecerli (m : Nat) :
    (LaltiB m).all (· < (7*m+6)) = true ∧ (LaltiB m).head? ≠ some 0 := by
  simp only [LaltiB, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-- RESULTS_n6.md formülü -/
def altiC (b : Nat) : List Nat := let B := b - 1
  fromD0_6 b ((7*B+5)/9) ((5*B+1)/9) ((B+2)/9)

/-! ------------------------------------------------------------
  ## Altic (t=0): b ≡ 8 (mod 9), yani b = 9m + 8
  Basamaklar: [7*m+6, 5*m+4, 1*m+0, 8*m+6, 4*m+3, 2*m+2]
  Ödünç zinciri: [0, 0, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def LaltiC (m : Nat) : List Nat := [7*m+6, 5*m+4, 1*m+0, 8*m+6, 4*m+3, 2*m+2]

theorem altiC_eq (m : Nat) : altiC (9*m+8) = LaltiC m := by
  simp only [altiC, fromD0_6, LaltiC, List.cons.injEq, and_true]
  omega

theorem altiC_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (9*m+8) 6 (ofDigits (9*m+8) (LaltiC m)) = ofDigits (9*m+8) (LaltiC m) := by
  simp only [kaprekar, LaltiC, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (8*m+6) = (7*m+6) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (9*m+8)) (d := 7*m+6) (x := 5*m+4) (s := 2*m+2) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (9*m+8)) (d := 5*m+4) (x := 1*m+0) (s := 4*m+3) (e' := 1) h2 (by omega)
  have h4 := borrow_step (b := (9*m+8)) (d := 4*m+3) (x := 8*m+6) (s := 5*m+4) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (9*m+8)) (d := 2*m+2) (x := 4*m+3) (s := 7*m+6) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (9*m+8)) (d := 1*m+0) (x := 2*m+2) (s := 8*m+6) (e' := 0) h5 (by omega)
  omega

theorem altiC_sabit (m : Nat) :
    kaprekar (9*m+8) 6 (ofDigits (9*m+8) (LaltiC m)) = ofDigits (9*m+8) (LaltiC m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact altiC_sabit_pos m h

/-- Altic: koşulu sağlayan HER b ≥ 8 tabanında sabit nokta. -/
theorem altiC_her_taban (b : Nat) (hb : b % 9 = 8) (h : 8 ≤ b) :
    kaprekar b 6 (ofDigits b (altiC b)) = ofDigits b (altiC b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 9*m + 8 := ⟨(b - 8) / 9, by omega⟩
  rw [altiC_eq]
  exact altiC_sabit m

theorem altiC_basamak_gecerli (m : Nat) :
    (LaltiC m).all (· < (9*m+8)) = true ∧ (LaltiC m).head? ≠ some 0 := by
  simp only [LaltiC, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-- RESULTS_n6.md formülü -/
def altiD (b : Nat) : List Nat := let B := b - 1
  fromD0_6 b ((3*B+3)/5) (B/3) ((B+1)/5)

/-! ------------------------------------------------------------
  ## Altid (t=0): b ≡ 10 (mod 15), yani b = 15m + 10
  Basamaklar: [9*m+6, 5*m+3, 3*m+1, 12*m+7, 10*m+6, 6*m+4]
  Ödünç zinciri: [0, 0, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def LaltiD (m : Nat) : List Nat := [9*m+6, 5*m+3, 3*m+1, 12*m+7, 10*m+6, 6*m+4]

theorem altiD_eq (m : Nat) : altiD (15*m+10) = LaltiD m := by
  simp only [altiD, fromD0_6, LaltiD, List.cons.injEq, and_true]
  omega

theorem altiD_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (15*m+10) 6 (ofDigits (15*m+10) (LaltiD m)) = ofDigits (15*m+10) (LaltiD m) := by
  simp only [kaprekar, LaltiD, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (12*m+7) = (9*m+6) + (3*m+1) + 0 := by omega
  have h2 := borrow_step (b := (15*m+10)) (d := 10*m+6) (x := 5*m+3) (s := 5*m+3) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (15*m+10)) (d := 9*m+6) (x := 3*m+1) (s := 6*m+4) (e' := 1) h2 (by omega)
  have h4 := borrow_step (b := (15*m+10)) (d := 6*m+4) (x := 12*m+7) (s := 9*m+6) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (15*m+10)) (d := 5*m+3) (x := 10*m+6) (s := 10*m+6) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (15*m+10)) (d := 3*m+1) (x := 6*m+4) (s := 12*m+7) (e' := 0) h5 (by omega)
  omega

theorem altiD_sabit (m : Nat) :
    kaprekar (15*m+10) 6 (ofDigits (15*m+10) (LaltiD m)) = ofDigits (15*m+10) (LaltiD m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact altiD_sabit_pos m h

/-- Altid: koşulu sağlayan HER b ≥ 10 tabanında sabit nokta. -/
theorem altiD_her_taban (b : Nat) (hb : b % 15 = 10) (h : 10 ≤ b) :
    kaprekar b 6 (ofDigits b (altiD b)) = ofDigits b (altiD b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 15*m + 10 := ⟨(b - 10) / 15, by omega⟩
  rw [altiD_eq]
  exact altiD_sabit m

theorem altiD_basamak_gecerli (m : Nat) :
    (LaltiD m).all (· < (15*m+10)) = true ∧ (LaltiD m).head? ≠ some 0 := by
  simp only [LaltiD, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

#print axioms altiA_her_taban
#print axioms altiB_her_taban
#print axioms altiC_her_taban
#print axioms altiD_her_taban

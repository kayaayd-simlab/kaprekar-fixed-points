/-
  Kaprekar sabit noktaları, n = 8: altı ailenin VARLIK yönü, her taban için.
  Kaynak: kaprekar-fixed-points / RESULTS.md, Bölüm 2.
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

/-! ============================================================
  # Makale: n = 8 için altı aile (RESULTS.md, Bölüm 2)
  B := b - 1. d-vektöründen sabit nokta, kanal ardıl formülüyle kurulur:
   t=0: [d0, d1, d2, d3-1, B-d3, B-d2, B-d1, b-d0]
   t=1: [d0, d1, d2-1, B, B, B-d2, B-d1, b-d0]
  ============================================================ -/

def fromD0 (b d0 d1 d2 d3 : Nat) : List Nat :=
  let B := b - 1
  [d0, d1, d2, d3 - 1, B - d3, B - d2, B - d1, b - d0]

def fromD1 (b d0 d1 d2 : Nat) : List Nat :=
  let B := b - 1
  [d0, d1, d2 - 1, B, B, B - d2, B - d1, b - d0]

/-- Aile 1 (t=1): b ≡ 0 (mod 3) -/
def aile1 (b : Nat) : List Nat := let B := b - 1
  fromD1 b ((2*B+2)/3) ((2*B-1)/3) ((B+1)/3)
/-- Aile 2 (t=0): b ≡ 10 (mod 15) -/
def aile2 (b : Nat) : List Nat := let B := b - 1
  fromD0 b ((3*B+3)/5) (B/3) (B/3) ((B+1)/5)
/-- Aile 3 (t=0): b ≡ 12 (mod 15) -/
def aile3 (b : Nat) : List Nat := let B := b - 1
  fromD0 b ((13*B+7)/15) ((11*B-1)/15) ((7*B-2)/15) ((B+4)/15)
/-- Aile 4 (t=0): b ≡ 11 (mod 17) -/
def aile4 (b : Nat) : List Nat := let B := b - 1
  fromD0 b ((11*B+9)/17) ((7*B-2)/17) ((5*B+1)/17) ((3*B+4)/17)
/-- Aile 5 (t=0): b ≡ 14 (mod 17) -/
def aile5 (b : Nat) : List Nat := let B := b - 1
  fromD0 b ((15*B+9)/17) ((13*B+1)/17) ((9*B+2)/17) ((B+4)/17)
/-- Aile 6 (t=0): b ≡ 13 (mod 21) -/
def aile6 (b : Nat) : List Nat := let B := b - 1
  fromD0 b ((5*B+3)/7) ((3*B-1)/7) (B/3) ((B+2)/7)

/-- Basamak listesi gerçekten tam 8 basamaklı bir sayıyı mı tanımlıyor,
    ve o sayı b tabanında Kaprekar sabit noktası mı? -/
def gecerliSabit (b : Nat) (ds : List Nat) : Bool :=
  ds.length == 8 && ds.all (· < b) && ds.head? != some 0 &&
  (let x := ofDigits b ds; kaprekar b 8 x == x)


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

/-! ------------------------------------------------------------
  ## Aile1 (t=1): b ≡ 0 (mod 3), yani b = 3m + 3
  Basamaklar: [2*m+2, 2*m+1, 1*m+0, 3*m+2, 3*m+2, 2*m+1, 1*m+1, 1*m+1]
  Ödünç zinciri: [0, 0, 1, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L1 (m : Nat) : List Nat := [2*m+2, 2*m+1, 1*m+0, 3*m+2, 3*m+2, 2*m+1, 1*m+1, 1*m+1]

theorem aile1_eq (m : Nat) : aile1 (3*m+3) = L1 m := by
  simp only [aile1, fromD1, L1, List.cons.injEq, and_true]
  omega

theorem aile1_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (3*m+3) 8 (ofDigits (3*m+3) (L1 m)) = ofDigits (3*m+3) (L1 m) := by
  simp only [kaprekar, L1, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (3*m+2) = (2*m+2) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (3*m+3)) (d := 3*m+2) (x := 2*m+1) (s := 1*m+1) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (3*m+3)) (d := 2*m+2) (x := 1*m+0) (s := 1*m+1) (e' := 1) h2 (by omega)
  have h4 := borrow_step (b := (3*m+3)) (d := 2*m+1) (x := 3*m+2) (s := 2*m+1) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (3*m+3)) (d := 2*m+1) (x := 3*m+2) (s := 2*m+1) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (3*m+3)) (d := 1*m+1) (x := 2*m+1) (s := 2*m+2) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (3*m+3)) (d := 1*m+1) (x := 1*m+1) (s := 3*m+2) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (3*m+3)) (d := 1*m+0) (x := 1*m+1) (s := 3*m+2) (e' := 0) h7 (by omega)
  omega

theorem aile1_sabit (m : Nat) :
    kaprekar (3*m+3) 8 (ofDigits (3*m+3) (L1 m)) = ofDigits (3*m+3) (L1 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile1_sabit_pos m h

/-- Aile1: koşulu sağlayan HER b ≥ 3 tabanında sabit nokta. -/
theorem aile1_her_taban (b : Nat) (hb : b % 3 = 0) (h : 3 ≤ b) :
    kaprekar b 8 (ofDigits b (aile1 b)) = ofDigits b (aile1 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 3*m + 3 := ⟨(b - 3) / 3, by omega⟩
  rw [aile1_eq]
  exact aile1_sabit m

theorem aile1_basamak_gecerli (m : Nat) :
    (L1 m).all (· < (3*m+3)) = true ∧ (L1 m).head? ≠ some 0 := by
  simp only [L1, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-! ------------------------------------------------------------
  ## Aile2 (t=0): b ≡ 10 (mod 15), yani b = 15m + 10
  Basamaklar: [9*m+6, 5*m+3, 5*m+3, 3*m+1, 12*m+7, 10*m+6, 10*m+6, 6*m+4]
  Ödünç zinciri: [0, 0, 0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L2 (m : Nat) : List Nat := [9*m+6, 5*m+3, 5*m+3, 3*m+1, 12*m+7, 10*m+6, 10*m+6, 6*m+4]

theorem aile2_eq (m : Nat) : aile2 (15*m+10) = L2 m := by
  simp only [aile2, fromD0, L2, List.cons.injEq, and_true]
  omega

theorem aile2_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (15*m+10) 8 (ofDigits (15*m+10) (L2 m)) = ofDigits (15*m+10) (L2 m) := by
  simp only [kaprekar, L2, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (12*m+7) = (9*m+6) + (3*m+1) + 0 := by omega
  have h2 := borrow_step (b := (15*m+10)) (d := 10*m+6) (x := 5*m+3) (s := 5*m+3) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (15*m+10)) (d := 10*m+6) (x := 5*m+3) (s := 5*m+3) (e' := 0) h2 (by omega)
  have h4 := borrow_step (b := (15*m+10)) (d := 9*m+6) (x := 3*m+1) (s := 6*m+4) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (15*m+10)) (d := 6*m+4) (x := 12*m+7) (s := 9*m+6) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (15*m+10)) (d := 5*m+3) (x := 10*m+6) (s := 10*m+6) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (15*m+10)) (d := 5*m+3) (x := 10*m+6) (s := 10*m+6) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (15*m+10)) (d := 3*m+1) (x := 6*m+4) (s := 12*m+7) (e' := 0) h7 (by omega)
  omega

theorem aile2_sabit (m : Nat) :
    kaprekar (15*m+10) 8 (ofDigits (15*m+10) (L2 m)) = ofDigits (15*m+10) (L2 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile2_sabit_pos m h

/-- Aile2: koşulu sağlayan HER b ≥ 10 tabanında sabit nokta. -/
theorem aile2_her_taban (b : Nat) (hb : b % 15 = 10) (h : 10 ≤ b) :
    kaprekar b 8 (ofDigits b (aile2 b)) = ofDigits b (aile2 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 15*m + 10 := ⟨(b - 10) / 15, by omega⟩
  rw [aile2_eq]
  exact aile2_sabit m

theorem aile2_basamak_gecerli (m : Nat) :
    (L2 m).all (· < (15*m+10)) = true ∧ (L2 m).head? ≠ some 0 := by
  simp only [L2, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-! ------------------------------------------------------------
  ## Aile3 (t=0): b ≡ 12 (mod 15), yani b = 15m + 12
  Basamaklar: [13*m+10, 11*m+8, 7*m+5, 1*m+0, 14*m+10, 8*m+6, 4*m+3, 2*m+2]
  Ödünç zinciri: [0, 0, 0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L3 (m : Nat) : List Nat := [13*m+10, 11*m+8, 7*m+5, 1*m+0, 14*m+10, 8*m+6, 4*m+3, 2*m+2]

theorem aile3_eq (m : Nat) : aile3 (15*m+12) = L3 m := by
  simp only [aile3, fromD0, L3, List.cons.injEq, and_true]
  omega

theorem aile3_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (15*m+12) 8 (ofDigits (15*m+12) (L3 m)) = ofDigits (15*m+12) (L3 m) := by
  simp only [kaprekar, L3, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (14*m+10) = (13*m+10) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (15*m+12)) (d := 13*m+10) (x := 11*m+8) (s := 2*m+2) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (15*m+12)) (d := 11*m+8) (x := 7*m+5) (s := 4*m+3) (e' := 0) h2 (by omega)
  have h4 := borrow_step (b := (15*m+12)) (d := 8*m+6) (x := 1*m+0) (s := 7*m+5) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (15*m+12)) (d := 7*m+5) (x := 14*m+10) (s := 8*m+6) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (15*m+12)) (d := 4*m+3) (x := 8*m+6) (s := 11*m+8) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (15*m+12)) (d := 2*m+2) (x := 4*m+3) (s := 13*m+10) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (15*m+12)) (d := 1*m+0) (x := 2*m+2) (s := 14*m+10) (e' := 0) h7 (by omega)
  omega

theorem aile3_sabit (m : Nat) :
    kaprekar (15*m+12) 8 (ofDigits (15*m+12) (L3 m)) = ofDigits (15*m+12) (L3 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile3_sabit_pos m h

/-- Aile3: koşulu sağlayan HER b ≥ 12 tabanında sabit nokta. -/
theorem aile3_her_taban (b : Nat) (hb : b % 15 = 12) (h : 12 ≤ b) :
    kaprekar b 8 (ofDigits b (aile3 b)) = ofDigits b (aile3 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 15*m + 12 := ⟨(b - 12) / 15, by omega⟩
  rw [aile3_eq]
  exact aile3_sabit m

theorem aile3_basamak_gecerli (m : Nat) :
    (L3 m).all (· < (15*m+12)) = true ∧ (L3 m).head? ≠ some 0 := by
  simp only [L3, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-! ------------------------------------------------------------
  ## Aile4 (t=0): b ≡ 11 (mod 17), yani b = 17m + 11
  Basamaklar: [11*m+7, 7*m+4, 5*m+3, 3*m+1, 14*m+8, 12*m+7, 10*m+6, 6*m+4]
  Ödünç zinciri: [0, 0, 0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L4 (m : Nat) : List Nat := [11*m+7, 7*m+4, 5*m+3, 3*m+1, 14*m+8, 12*m+7, 10*m+6, 6*m+4]

theorem aile4_eq (m : Nat) : aile4 (17*m+11) = L4 m := by
  simp only [aile4, fromD0, L4, List.cons.injEq, and_true]
  omega

theorem aile4_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (17*m+11) 8 (ofDigits (17*m+11) (L4 m)) = ofDigits (17*m+11) (L4 m) := by
  simp only [kaprekar, L4, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (14*m+8) = (11*m+7) + (3*m+1) + 0 := by omega
  have h2 := borrow_step (b := (17*m+11)) (d := 12*m+7) (x := 7*m+4) (s := 5*m+3) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (17*m+11)) (d := 11*m+7) (x := 5*m+3) (s := 6*m+4) (e' := 0) h2 (by omega)
  have h4 := borrow_step (b := (17*m+11)) (d := 10*m+6) (x := 3*m+1) (s := 7*m+4) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (17*m+11)) (d := 7*m+4) (x := 14*m+8) (s := 10*m+6) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (17*m+11)) (d := 6*m+4) (x := 12*m+7) (s := 11*m+7) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (17*m+11)) (d := 5*m+3) (x := 10*m+6) (s := 12*m+7) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (17*m+11)) (d := 3*m+1) (x := 6*m+4) (s := 14*m+8) (e' := 0) h7 (by omega)
  omega

theorem aile4_sabit (m : Nat) :
    kaprekar (17*m+11) 8 (ofDigits (17*m+11) (L4 m)) = ofDigits (17*m+11) (L4 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile4_sabit_pos m h

/-- Aile4: koşulu sağlayan HER b ≥ 11 tabanında sabit nokta. -/
theorem aile4_her_taban (b : Nat) (hb : b % 17 = 11) (h : 11 ≤ b) :
    kaprekar b 8 (ofDigits b (aile4 b)) = ofDigits b (aile4 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 17*m + 11 := ⟨(b - 11) / 17, by omega⟩
  rw [aile4_eq]
  exact aile4_sabit m

theorem aile4_basamak_gecerli (m : Nat) :
    (L4 m).all (· < (17*m+11)) = true ∧ (L4 m).head? ≠ some 0 := by
  simp only [L4, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-! ------------------------------------------------------------
  ## Aile5 (t=0): b ≡ 14 (mod 17), yani b = 17m + 14
  Basamaklar: [15*m+12, 13*m+10, 9*m+7, 1*m+0, 16*m+12, 8*m+6, 4*m+3, 2*m+2]
  Ödünç zinciri: [0, 0, 0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L5 (m : Nat) : List Nat := [15*m+12, 13*m+10, 9*m+7, 1*m+0, 16*m+12, 8*m+6, 4*m+3, 2*m+2]

theorem aile5_eq (m : Nat) : aile5 (17*m+14) = L5 m := by
  simp only [aile5, fromD0, L5, List.cons.injEq, and_true]
  omega

theorem aile5_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (17*m+14) 8 (ofDigits (17*m+14) (L5 m)) = ofDigits (17*m+14) (L5 m) := by
  simp only [kaprekar, L5, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (16*m+12) = (15*m+12) + (1*m+0) + 0 := by omega
  have h2 := borrow_step (b := (17*m+14)) (d := 15*m+12) (x := 13*m+10) (s := 2*m+2) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (17*m+14)) (d := 13*m+10) (x := 9*m+7) (s := 4*m+3) (e' := 0) h2 (by omega)
  have h4 := borrow_step (b := (17*m+14)) (d := 9*m+7) (x := 1*m+0) (s := 8*m+6) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (17*m+14)) (d := 8*m+6) (x := 16*m+12) (s := 9*m+7) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (17*m+14)) (d := 4*m+3) (x := 8*m+6) (s := 13*m+10) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (17*m+14)) (d := 2*m+2) (x := 4*m+3) (s := 15*m+12) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (17*m+14)) (d := 1*m+0) (x := 2*m+2) (s := 16*m+12) (e' := 0) h7 (by omega)
  omega

theorem aile5_sabit (m : Nat) :
    kaprekar (17*m+14) 8 (ofDigits (17*m+14) (L5 m)) = ofDigits (17*m+14) (L5 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile5_sabit_pos m h

/-- Aile5: koşulu sağlayan HER b ≥ 14 tabanında sabit nokta. -/
theorem aile5_her_taban (b : Nat) (hb : b % 17 = 14) (h : 14 ≤ b) :
    kaprekar b 8 (ofDigits b (aile5 b)) = ofDigits b (aile5 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 17*m + 14 := ⟨(b - 14) / 17, by omega⟩
  rw [aile5_eq]
  exact aile5_sabit m

theorem aile5_basamak_gecerli (m : Nat) :
    (L5 m).all (· < (17*m+14)) = true ∧ (L5 m).head? ≠ some 0 := by
  simp only [L5, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

/-! ------------------------------------------------------------
  ## Aile6 (t=0): b ≡ 13 (mod 21), yani b = 21m + 13
  Basamaklar: [15*m+9, 9*m+5, 7*m+4, 3*m+1, 18*m+10, 14*m+8, 12*m+7, 6*m+4]
  Ödünç zinciri: [0, 0, 0, 1, 1, 1, 1, 0]   (m < 1 durumları ayrıca kontrol edildi)
  ------------------------------------------------------------ -/

def L6 (m : Nat) : List Nat := [15*m+9, 9*m+5, 7*m+4, 3*m+1, 18*m+10, 14*m+8, 12*m+7, 6*m+4]

theorem aile6_eq (m : Nat) : aile6 (21*m+13) = L6 m := by
  simp only [aile6, fromD0, L6, List.cons.injEq, and_true]
  omega

theorem aile6_sabit_pos (m : Nat) (hm : 1 ≤ m) :
    kaprekar (21*m+13) 8 (ofDigits (21*m+13) (L6 m)) = ofDigits (21*m+13) (L6 m) := by
  simp only [kaprekar, L6, ofDigits, List.foldl, Nat.zero_mul, Nat.zero_add]
  rw [digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_step _ _ _ _ (by omega),
      digits_step _ _ _ _ (by omega), digits_one _ _ (by omega)]
  simp (disch := omega) only [sortAsc, insertSorted, if_pos, if_neg, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.foldl, Nat.zero_mul, Nat.zero_add]
  have h1 : (18*m+10) = (15*m+9) + (3*m+1) + 0 := by omega
  have h2 := borrow_step (b := (21*m+13)) (d := 15*m+9) (x := 9*m+5) (s := 6*m+4) (e' := 0) h1 (by omega)
  have h3 := borrow_step (b := (21*m+13)) (d := 14*m+8) (x := 7*m+4) (s := 7*m+4) (e' := 0) h2 (by omega)
  have h4 := borrow_step (b := (21*m+13)) (d := 12*m+7) (x := 3*m+1) (s := 9*m+5) (e' := 1) h3 (by omega)
  have h5 := borrow_step (b := (21*m+13)) (d := 9*m+5) (x := 18*m+10) (s := 12*m+7) (e' := 1) h4 (by omega)
  have h6 := borrow_step (b := (21*m+13)) (d := 7*m+4) (x := 14*m+8) (s := 14*m+8) (e' := 1) h5 (by omega)
  have h7 := borrow_step (b := (21*m+13)) (d := 6*m+4) (x := 12*m+7) (s := 15*m+9) (e' := 1) h6 (by omega)
  have h8 := borrow_step (b := (21*m+13)) (d := 3*m+1) (x := 6*m+4) (s := 18*m+10) (e' := 0) h7 (by omega)
  omega

theorem aile6_sabit (m : Nat) :
    kaprekar (21*m+13) 8 (ofDigits (21*m+13) (L6 m)) = ofDigits (21*m+13) (L6 m) := by
  rcases Nat.lt_or_ge m 1 with h | h
  · have : m = 0 := by omega
    rcases this with rfl <;> decide
  · exact aile6_sabit_pos m h

/-- Aile6: koşulu sağlayan HER b ≥ 13 tabanında sabit nokta. -/
theorem aile6_her_taban (b : Nat) (hb : b % 21 = 13) (h : 13 ≤ b) :
    kaprekar b 8 (ofDigits b (aile6 b)) = ofDigits b (aile6 b) := by
  obtain ⟨m, rfl⟩ : ∃ m, b = 21*m + 13 := ⟨(b - 13) / 21, by omega⟩
  rw [aile6_eq]
  exact aile6_sabit m

theorem aile6_basamak_gecerli (m : Nat) :
    (L6 m).all (· < (21*m+13)) = true ∧ (L6 m).head? ≠ some 0 := by
  simp only [L6, List.all_cons, List.all_nil, List.head?_cons, ne_eq, Option.some.injEq,
    Bool.and_true, Bool.and_eq_true, decide_eq_true_eq]
  omega

#print axioms aile1_her_taban
#print axioms aile2_her_taban
#print axioms aile3_her_taban
#print axioms aile4_her_taban
#print axioms aile5_her_taban
#print axioms aile6_her_taban

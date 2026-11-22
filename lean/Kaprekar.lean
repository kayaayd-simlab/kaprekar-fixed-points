/-
  Kaprekar fonksiyonu: Lean 4 ile ilk adım
  Sadece Lean çekirdeği kullanılıyor (Mathlib yok).

  K_b,n(x) = (x'in b tabanındaki n basamağı büyükten küçüğe dizilince oluşan sayı)
           - (küçükten büyüğe dizilince oluşan sayı)
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

/-! ## Teorem 1: 6174, 10 tabanında 4 basamaklı Kaprekar sabit noktasıdır. -/
theorem k6174 : kaprekar 10 4 6174 = 6174 := by decide

/-! ## Teorem 2: 495, 10 tabanında 3 basamaklı Kaprekar sabit noktasıdır. -/
theorem k495 : kaprekar 10 3 495 = 495 := by decide

/-! ## Teorem 3 (Kaprekar 1949): Bütün basamakları aynı olmayan her 4 basamaklı sayı
    en fazla 7 adımda 6174'e ulaşır. 10.000 durumun hepsi tek tek kontrol ediliyor. -/
theorem kaprekar_4digit :
    ∀ x, x < 10000 → repdigit 10 4 x = false → iter (kaprekar 10 4) 7 x = 6174 := by
  native_decide

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

/-! Örnek: 10 tabanında Aile 2'nin ilk üyesi 63317664'tür. -/
theorem aile2_taban10 : ofDigits 10 (aile2 10) = 63317664 := by decide
theorem k63317664 : kaprekar 10 8 63317664 = 63317664 := by decide

/-! ## Varlık teoremi (sonlu aralıkta): her aile, koşulunu sağlayan
    her b < 3000 tabanı için gerçekten bir sabit nokta veriyor. -/
theorem aile1_varlik : ∀ b, b < 3000 → b ≥ 3  → b % 3 = 0  → gecerliSabit b (aile1 b) = true := by native_decide
theorem aile2_varlik : ∀ b, b < 3000 → b ≥ 10 → b % 15 = 10 → gecerliSabit b (aile2 b) = true := by native_decide
theorem aile3_varlik : ∀ b, b < 3000 → b ≥ 12 → b % 15 = 12 → gecerliSabit b (aile3 b) = true := by native_decide
theorem aile4_varlik : ∀ b, b < 3000 → b ≥ 11 → b % 17 = 11 → gecerliSabit b (aile4 b) = true := by native_decide
theorem aile5_varlik : ∀ b, b < 3000 → b ≥ 14 → b % 17 = 14 → gecerliSabit b (aile5 b) = true := by native_decide
theorem aile6_varlik : ∀ b, b < 3000 → b ≥ 13 → b % 21 = 13 → gecerliSabit b (aile6 b) = true := by native_decide

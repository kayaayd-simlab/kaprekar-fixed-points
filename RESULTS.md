# Sekiz Basamaklı Kaprekar Sabit Noktaları: Taban Sınıflandırması

*n=6 sonucunun n=8'e genellenmesi — sentez raporu (Faz 3 sonu, Temmuz 2026).*

Notasyon: $B := b-1$. Sıralı rakamlar $a_0\ge\cdots\ge a_7$ için
$d_i = a_i - a_{7-i}$ ($i=0..3$). Kanal $t$ := $d$-vektörünün sondaki sıfır
sayısı; rakam toplamı her zaman $(4+t)\,B$.

---

## 1. Ana teorem (n=8)

> **Teorem.** Taban $b\ge2$, tam sekiz basamaklı bir Kaprekar sabit noktası
> barındırır **ancak ve ancak**
> $$3\mid b \;\lor\; b\equiv 10,12\ (\mathrm{mod}\ 15) \;\lor\;
>   b\equiv 11,14\ (\mathrm{mod}\ 17) \;\lor\; b\equiv 13\ (\mathrm{mod}\ 21)
>   \;\lor\; b\in\{2,4,8\}.$$

> **Sonuç (tek tabanlar).** Tek taban $b$ için sabit nokta var ⟺
> $$b\equiv 3\ (6)\ \lor\ b\equiv 25,27\ (30)\ \lor\ b\equiv 11,31\ (34)
>   \ \lor\ b\equiv 13\ (42).$$
> n=6'daki yapı korunur: her ailenin modülü tek-taban kısıtıyla **ikiye
> katlanır** ($D \to 2D$; 15→30, 17→34, 21→42, 3→6).

**Yoğunluk.** Kongrüans birleşiminin periyodu $\mathrm{lcm}(3,15,17,21)=1785$;
kapsanan kalıntı $900/1785 = 60/119 \approx 0{,}5042$. Tüm aileler
**parite-kör** olduğundan (modüllerin hepsi tek) tek tabanlarda da, çift
tabanlarda da oran aynı $60/119$'dur. Kıyas — n=6: çift tabanlar %100, tek
tabanlar $93/315=31/105\approx0{,}2952$.

---

## 2. Altı aile

$d$-vektörleri ($B=b-1$; $t>0$ için eksik bileşenler 0):

| # | Kanal | Kongrüans | $d$-vektörü | Eşik / ilk üyeler |
|:-:|:-:|:-:|:--|:--|
| 1 | t=1 (k=5) | $b\equiv0\ (3)$ | $\left(\frac{2B+2}{3},\frac{2B-1}{3},\frac{B+1}{3}\right)$ | $b\ge3$: 3, 6, 9, … |
| 2 | t=0 (k=4) | $b\equiv10\ (15)$ | $\left(\frac{3B+3}{5},\frac{B}{3},\frac{B}{3},\frac{B+1}{5}\right)$ | $b\ge10$: 10, 25, 40, 55, … |
| 3 | t=0 (k=4) | $b\equiv12\ (15)$ | $\left(\frac{13B+7}{15},\frac{11B-1}{15},\frac{7B-2}{15},\frac{B+4}{15}\right)$ | $b\ge12$: 12, 27, 42, 57, … |
| 4 | t=0 (k=4) | $b\equiv11\ (17)$ | $\left(\frac{11B+9}{17},\frac{7B-2}{17},\frac{5B+1}{17},\frac{3B+4}{17}\right)$ | $b\ge11$: 11, 28, 45, 62, … |
| 5 | t=0 (k=4) | $b\equiv14\ (17)$ | $\left(\frac{15B+9}{17},\frac{13B+1}{17},\frac{9B+2}{17},\frac{B+4}{17}\right)$ | $b\ge14$: 14, 31, 48, 65, … |
| 6 | t=0 (k=4) | $b\equiv13\ (21)$ | $\left(\frac{5B+3}{7},\frac{3B-1}{7},\frac{B}{3},\frac{B+2}{7}\right)$ | $b\ge13$: 13, 34, 55, 76, … |

Sabit nokta, $d$'den kanal ardıl formülüyle kurulur (Faz 1):
- t=0: $[\,d_0, d_1, d_2, d_3{-}1,\ B{-}d_3, B{-}d_2, B{-}d_1, b{-}d_0\,]$
- t=1: $[\,d_0, d_1, d_2{-}1,\ B, B,\ B{-}d_2, B{-}d_1, b{-}d_0\,]$

**Örnek (taban 10).** $b=10$, Aile 2'nin ilk üyesi: $d=(6,3,3,2)$ →
$63317664$ (bilinen 8-basamaklı Kaprekar sabiti). İkinci sabit $97508421$
($d=(9,7,5,1)$) hiçbir aileye ait değildir — aşağıdaki sonlu sporadik
kümenin üyesidir.

**Determinant tayfı:** $\{3, 15, 15, 17, 17, 21\}$ (n=6: $\{7, 9, 15\}$).

---

## 3. Sporadikler (aile-dışı, tamamı $b\le10$)

9 nokta, yalnız 5 tabanda; $\{2,4,8\}$ tabanları *sadece* sporadik içerir:

| $b$ | $d$-vektörleri |
|:-:|:--|
| 2 | (1,1,1,1), (1,1,1,0), (1,1,0,0) |
| 4 | (3,1,1,1), (3,3,1,1), (3,3,3,1) |
| 6 | (5,5,3,1) |
| 8 | (7,5,3,1) |
| 10 | (9,7,5,1) |

Bunlar, eşitsizlikleri yalnız sonlu bir $B$ penceresinde sağlanan
hücrelerden gelir; tüm pencereler kesin üst sınırlıdır ve tüketilerek
taranmıştır.

---

## 4. Kanıt iskeleti ve mekanik envanter

**İndirgeme (Faz 1).** Ödünç zinciri çözülünce dört kanal: $t=0..3$, rakam
toplamı $(4+t)B$. 46 ground-truth noktasının tamamı kanal formülleriyle
birebir yeniden üretildi.

**Hücre taraması (Faz 2).** Her kanalda 8 ardıl ifadenin her sıralaması bir
hücre; sabit nokta koşulu $A_\sigma d = B c_\sigma + e_\sigma$. Kesirli
aritmetikle (tam, yuvarlamasız) sınıflandırma:

| Kanal | Ayrık hücre | Tekil (her B) | Yaşayan aile | Pencere | Tutarsız | Belirsiz |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| t=0 | 40 320 | 33 344 | **5** | 505 | 5 152 | 1 824 |
| t=1 | 20 160 | 2 344 | **1** | 159 | 14 932 | 162 |
| t=2 | 1 680 | 76 | 0 | 24 | 1 472 | 0 |
| t=3 | 56 | 2 | 0 | 1 | 48 | 0 |

t=2 kanalı yalnız $b=2$'ye, t=3 kanalı boşluğa kapanır (belirsiz hücre yok
→ bu iki kanal **tamamen kanıtlı** biçimde kapalı).

**Geçerlilik (Lemma B analoğu).** Altı ailenin sıralama+aralık+bütünlük
eşitsizlikleri $B$'de lineer; kesin eşikler hesaplandı, her ailenin ilk
üyeleri eşik üstünde ve sayısal doğrulandı → her aile üyesi geçerli sabit
noktadır (⇐ yönü).

**Tamlık (⇒ yönü) kapanışı (Faz 3).**
- $b\le60$: tam kaba kuvvet ground-truth ile **sıfır uyuşmazlık** (46 nokta
  = 37 aile üyesi ∪ 9 sporadik).
- $b=61..100$: tam d-uzayı taraması, nokta düzeyinde birebir "bulunan =
  aile tahmini"; yeni sporadik yok.
- Sabit-B belirsiz hücreler (1 162): hepsinin sabitlendiği $B$ değeri
  $b\le60$ bölgesinde → ground-truth kapatıyor.
- Her-B belirsiz hücreler (824, tamamı 1 serbest boyutlu): $b=61..500$ tam
  tarama + $b\in\{601,787,997,1201,1499\}$ örnekleri — **aile-dışı sıfır
  nokta**. Ardından Faz 3b ile kesin kapanış: her hücrenin $(B,u)$ kısıt
  çokyüzlüsü kesirli 2B-LP ile incelendi (bölge $B\ge1$, $0\le u\le B$
  içinde çizgi içeremez → sivri → boş-değilse köşesi var; köşe sayımı tam).
  Sonuç: 779 hücrede bölge **boş**, 45 hücrede $B_{\max}\le3$ (yani
  $b\le4$, ground-truth kapsamında), $B$-yönünde sınırsız hücre **yok** →
  bu hücrelerden hiçbir tabanda aile-dışı nokta çıkamaz, **kanıtla**.

---

## 5. n=6 ile yapısal karşılaştırma

| | n=6 | n=8 |
|:--|:--|:--|
| Kanal sayısı | 2 ($3B$, $4B$) | 4 ($4B..7B$); üst iki kanal ölü/sonlu |
| Çift tabanlar | hepsi (palindromik tanık) | artık evrensel DEĞİL (16, 20, 22, … boş) |
| Parite rolü | kanal ayırıyor | aileler parite-kör |
| "Kolay" evrensel aile | $4B$ kanalı, $2\mid b$ | $5B$ kanalı, $3\mid b$ |
| Aile sayısı / det | 3 / $\{7,9,15\}$ | 6 / $\{3,15,15,17,17,21\}$ |
| Tek-taban modül ikilenmesi | $\det\to2\det$ (14, 18, 30) | **korunuyor** (6, 30, 34, 42) |
| Periyot / kapsama (tek) | 630 / 93 (%29,5) | 3570 / 900 (%50,4) |

Ana sorunun cevabı: n=6'nın yapısı (det → 2·det modülü, aritmetik dizi
birleşimi) **korunuyor**; ama "her çift taban dolu" simetrisi kırılıyor,
onun yerini "$3\mid b$ dolu" alıyor ve tek/çift ayrımı aile düzeyinde
kayboluyor.

---

## 6. Dürüst defter (statü etiketleri)

- **Kanıtlı:** kanal ayrıştırması ve ardıl formüller; hücre sınıflandırması
  (kesin kesirli aritmetik); altı ailenin geçerliliği (⇐ yönü); t=2/t=3
  kanallarının kapanışı; pencere hücrelerinin sonluluğu ve tüketilmesi;
  sabit-B belirsizlerin kapanışı ($b\le60$ tam tarama ile); **her-B belirsiz
  824 hücrenin kapanışı** (Faz 3b kesin LP: 779 boş bölge, 45'inde
  $B_{\max}\le3$, sınırsız hücre yok). Teoremin iki yönü de mekanik olarak
  kapalıdır; n=6'da açık bırakılan "belirsiz hücreleri sembolik kapatma"
  formalitesinin n=8 karşılığı **açık değildir**.
- **Not:** tüm kanıt adımları makine-doğrulamalıdır (kesirli aritmetik,
  yuvarlamasız); insan-okur kanıt metni (lemma-lemma yazım) henüz
  üretilmedi — istenirse RESULTS.md'den türetilebilir.
- **Bağımsız denetim (`phase_audit.py`, öz-eleştiri sonrası):**
  (A) d-uzayı kısayolu kullanılmadan naif tam-aralık kaba kuvvet
  (n=8 b≤8, n=6 b≤10, taban-10 dış çengeli dahil) — scanner ile birebir;
  (B) 600 rastgele hücrede, B=11 ve 16'da azalan d-konisi tüketilerek
  çözüm kümeleri RREF'siz sayıldı — sınıflandırıcı verdiktleriyle 1200/1200
  uyum. Ortak-mod (RREF) riski böylece bağımsız yoldan da kapatıldı.
- **Bilinen zararsız kusur:** t=3 kanalında "8 basamak" kısıtı d0≥2 yerine
  d0≥1 kodlanmıştır (baş rakam d0−1 olduğundan off-by-one). Hata güvenli
  yöndedir: yokluk argümanlarında kısıtı zayıflatır (bölgeyi büyütür),
  sahte adaylar ise sayısal doğrulamadan (v ≥ b⁷) geçemez; t=3 zaten hiç
  nokta üretmemiştir. Sonuçlara etkisi yoktur.

## 7. Literatür kapısı (Faz 4)

Tarama, sonuç elde edildikten SONRA yapıldı (önyargı önleme). İki tur:
hızlı tarama + derin tur (birincil kaynak künye doğrulamalı; durum
etiketleri: [B]=birincil kaynaktan, [S]=yalnız arama parçacığından).

**Bizim eksenin (n sabit, taban değişken) soy ağacı:**
- **Hasse & Prichett (1978),** *J. Reine Angew. Math.* 299/300 — **n=4**
  için taban sınıflandırması; en yakın tarihsel öncül. [S]
- **Ludington (1979)** — her tabanda sonlu sayıda Kaprekar sabiti. [S]
- **n=5 sonucu** — DÜZELTME (makale yazımı sırasında): "b≡3 (mod 6),
  b≠9" iddiası **Kaprekar SABİTİ** (çeken tek sabit nokta) içindir,
  sabit nokta VARLIĞI için değil; kendi taramamız n=5 sabit noktalarının
  b≤60'ta tam olarak {2} ∪ 3ℤ tabanlarında var olduğunu gösterdi.
  Ayrıca ilk taramanın atfettiği arXiv:1710.06308 yanlış eşleşme
  (D. Hanover, 3-basamak). Makalede ayrım açıkça kuruldu. [B — kendi
  hesabımız + arXiv özeti]
- **Thakur,** "Kaprekar phenomena", Ropar Conf. Proc., RMS Lecture Notes
  No. 26 (2019), 1–10 — **TAM METİN OKUNDU** (3 Temmuz 2026, yazarla
  yazışma sonrası; pypdf ile çıkarıldı, `data/lit/thakur_kaprekar_extracted.txt`).
  [B, birincil kaynak] Keyfi tabanda n=5,7,9 için tam teoremler (7 ve 9
  basamak yalnız birer tabanda: 4 ve 5); n=6,8 için yalnız **ampirik
  veri** ("guesses" başlığı altında): n=6'da Kaprekar FENOMENİ (güçlü
  anlamda, tekil global çekici) yalnız B=13,17'de (B≤39); n=8'de yalnız
  B=3'te (B≤17). **Çapraz doğrulama:** bu üç taban, bizim ailelerimizin
  TAM İLK ÜYELERİ (13≡13 mod14, 17≡17 mod18, 3≡0 mod3) — çelişki değil,
  mantıksal gereklilik (Kaprekar fenomeni ⊂ sabit nokta varlığı).
  **Kritik:** kendi Açık Sorular bölümünde (5.5-ii) "FP(B,D) ne zaman
  boş değil" karakterizasyonunu AÇIKÇA çözülmemiş olarak listeliyor —
  yani bizim teoremimiz onun kendi açık sorusunu yanıtlıyor. Makaleye
  eklendi (`\cite{Thakur19}` + Bölüm 6'da çapraz doğrulama notu).

**Komşu eksen (taban sabit, n değişken):**
- **Kay & Downes-Ward,** "Fixed Points and Cycles of the Kaprekar
  Transformation: 1. Odd Bases", *J. Integer Sequences* 25 (2022), 22.6.7
  [B]; "2. Even Bases", arXiv:2408.12257 (2024) [B, özet düzeyi]. Taban
  sabitlenir; taban-8 bölümü n≥8 basamak sayılarına değinir ama soru
  bizimkinin devriğidir; tamlık kanıtı yalnız taban 4'te.
- **Prichett–Ludington–Lapenta** (1981, *Fibonacci Quart.* 19(1) 45–52)
  ve **Iwasaki** (2024, *Fibonacci Quart.* 62(4)) — yalnız taban 10. [S]
- **Chen–Ono–Schwartz–Thakur,** arXiv:2606.20439 (Haziran 2026) [B] —
  n=4, tek tabanlarda çevrim uzunluğu; varlık kongrüansı vermiyor; bu
  hattın (Schwartz–Thakur) aktif olduğunun işareti.

**OEIS:** A099009 (taban-10 sabit noktaları; 63317664 ve 97508421 orada)
ve taban-başına aile A163205, A164997, …, A165094 (taban 8), A165114 —
hepsi taban-sabit eksende. **Bizim eksende ("8-basamaklı sabit nokta
barındıran tabanlar") dizi bulunamadı**; taban dizimiz (2,3,4,6,8,…) ve
tek alt dizisi OEIS aramalarında eşleşme vermedi. [S — OEIS doğrudan
erişimi 403 verdi, arama motoru üzerinden]

**Konum ve güven:** n=8 taban-kongrüans karakterizasyonu erişilebilir
kaynakların hiçbirinde yok; konuya en yakın iki program (Hasse–Prichett
soyu ve Thakur) çift n≥6'yı açıkça dışarıda bırakıyor. Kay–Downes-Ward'ın
iki makalesi **tam metin okunarak** kontrol edildi (yerel PDF'ler,
`data/lit/`): her iki makaledeki tüm kongrüans ifadeleri ya tabanın
fonksiyonu ya da SABİT taban içinde basamak sayısının fonksiyonu; "Even
Bases" makalesinin taban-8 bölümü (§5) sorumuzun tam devriği (b=8 sabit,
n değişken) ve hiçbir yerde çapraz-taban n=8 ifadesi, mod 15/17/21
kongrüansı ya da {2,4,8} sporadik kümesi geçmiyor. **Hüküm: sonuç
bildiğimiz kadarıyla YENİ; güven yüksek.** (Kalan tek erişilemeyen tam
metin Thakur ön-baskısı; ancak parçacıklarında kapsamı n=3,5,7,9 olarak
açıkça beyan ediliyor.) Yakın-komşu/örtüşme riski izlenecek yazarlar:
Kay & Downes-Ward ve Schwartz–Thakur çevresi (arXiv:2606.20439 hattı
aktif).

## 8. Tek cümlelik özet

> n=6'da üç aritmetik diziye çöken sızıntı, n=8'de altı diziye genişler;
> parite duvarı yıkılır, $2\mid b$ tahtı $3\mid b$'ye geçer, ama iskelet —
> koni determinantları, bütünlük kongrüansları, tek tabanda modül
> ikilenmesi — olduğu gibi ayakta kalır.

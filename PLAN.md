# Kaprekar n=8: Sekiz Basamaklı Sabit Noktaların Taban Sınıflandırması

## Bağlam ve amaç

Bu proje, kanıtlanmış bir n=6 sonucunun n=8'e genellenmesidir. n=6 sonucu (referans, bilinen):

- **Çift tabanlar:** her çift taban b=2h, palindromik sabit nokta içerir; sıralı rakamlar (h, h-1, b-1, b-1, h-1, h).
- **Tek tabanlar:** b tek tabanında 6-basamaklı Kaprekar sabit noktası vardır ⟺ b≡13 (mod 14) ∨ b≡17 (mod 18) ∨ b≡25 (mod 30). Üç aile, üç sıralama konisinin determinantlarından (7, 9, 15) doğar; tek-taban kısıtı modülleri iki katına çıkarır (14, 18, 30). Birleşim lcm=630 periyodiktir ve 630 kalıntının 93'ünü kaplar.

**Ana soru (n=8):** Hangi tabanlar sekiz basamaklı Kaprekar sabit noktası barındırır? Tek tabanlar için kongrüans karakterizasyonu nedir? n=6'daki yapı (det → 2·det modülü, aritmetik dizi birleşimi) korunuyor mu?

## Tanımlar (koda tek yerde sabitle — `core.py`)

- Kaprekar dönüşümü K_b(x): x'in taban-b rakamlarını büyükten küçüğe (desc) ve küçükten büyüğe (asc) diz, K = desc − asc.
- Sabit nokta: K_b(x) = x, x pozitif, taban-b'de TAM 8 basamaklı (başta sıfır yok). Repdigit → 0 önemsizi otomatik dışlanır.
- **B := b − 1.** (DİKKAT: C := b + 1 ikileme koordinatıdır; B ile C'yi asla karıştırma. b→2b+1 altında B→2B+2 ama C→2C.)
- Sıralı rakamlar a0 ≥ a1 ≥ ... ≥ a7 için fark koordinatları: d0=a0−a7, d1=a1−a6, d2=a2−a5, d3=a3−a4.
- Sabit noktanın rakam toplamı her zaman B'nin katıdır (Lemma 1, n'den bağımsız, bilinen).

## Faz 0 — Zemin doğrulama (ground truth) [ÖNCE BU]

`phase0_bruteforce.py`:
1. n=6 kaba kuvvet tarayıcı yaz: verilen b için tüm sabit noktaları fark-koordinat uzayında tara (d-uzayı taraması; b^6 tam sayı taraması DEĞİL — d-uzayı O(b^3), yeterli).
2. Bilinen n=6 sonucuyla doğrula: tek tabanlar b<70'te sabit noktalı olanlar TAM OLARAK [13,17,25,27,35,41,53,55,69] olmalı; taban başına sayılar b=2'den [2,0,3,0,3,0,2,0,2,0,1,1,1,0,1,...] ile başlamalı. Uyuşmazsa DUR, boru hattını düzelt.
3. Aynı tarayıcıyı n=8'e genelle (d-uzayı O(b^4); b≤60 hedef, gerekirse b≤40 ile başla).
4. Çıktıları `data/groundtruth_n8.json` dosyasına yaz: {b: [sıralı-rakam-listeleri]}.
5. İlk gözlemler: hangi tek tabanlar sızıyor? Taban başına sayılar? Rakam toplamları hangi k(b−1) değerlerinde?

## Faz 1 — Ardıl formülü (kanal ayrıştırması)

`phase1_channels.py`:
1. n=8 için çıkarma işleminin ödünç (borrow) zincirini sembolik çöz. n=6'da sonuç şuydu: tüm d_i≥1 iken ardıl rakamlar [d0, d1, d2−1, B−d2, B−d1, b−d0].
2. n=8 kanalları: (a) d3≥1 tam kanal; (b) d3=0; (c) d2=d3=0; ... Her kanal için ardıl rakam formülünü türet ve Faz 0 verisiyle SAYISAL DOĞRULA (her ground-truth sabit noktasının d-vektörünü çıkar, formülün onu yeniden ürettiğini kontrol et).
3. Her kanalın rakam toplamı k(b−1): hangi k'lar mümkün? (n=6'da k=3 ve k=4 idi.)
4. Hangi kanallar tek tabana açık? (n=6'da d2=0 kanalı parite gereği yalnız çift tabana açıktı — benzer parite argümanları ara.)

## Faz 2 — Hücre taraması (asıl büyük hesap)

`phase2_cells.py`:
1. Tam kanal (tüm d_i≥1) için: 8 ardıl ifadenin her permütasyonu (8! = 40320) bir sıralama hücresi. Her hücrede sabit nokta koşulu 4 bilinmeyenli lineer sistem: A_σ·d = B·c_σ + e_σ.
2. sympy.linsolve ile sınıflandır: tekil çözüm / tutarsız / belirsiz (serbest parametreli). ARA SONUÇLARI ÖNBELLEĞE YAZ (`data/cells_n8.json`): her 1000 hücrede bir diske kaydet, kesintiden devam edebilsin.
3. Paralelleştir (multiprocessing, chunk'lara böl). Tekil çözümlerde d_i = (α_i·B + β_i)/det formunu ve det değerini kaydet.
4. Tekil hücreleri ele: hangileri sonsuz aile (eşitsizlikler büyük B'de sağlanıyor), hangileri küçük-b sınırına çöküyor? Determinant spektrumunu çıkar.
5. Diğer kanalları (d3=0 vb.) aynı makineden geçir.

## Faz 3 — Geçerlilik ve sentez

`phase3_synthesis.py`:
1. Yaşayan (sonsuz-aile) hücreler için Lemma B analoğu: sıralama+aralık+bütünlük eşitsizliklerini sembolik çöz, B eşiklerini bul, her ailenin ilk üyesinin eşiği aştığını doğrula.
2. Bütünlük (integrality) koşullarından kongrüansları çıkar: her aile için b ≡ r (mod m). Tek-taban kısıtının modülleri nasıl değiştirdiğine dikkat (n=6'da 2× idi).
3. Kongrüans birleşimini Faz 0 ground-truth ile BİREBİR karşılaştır (b≤60 tüm tabanlar). TEK BİR uyuşmazlık bile varsa dur, kimliğini çıkar (n=6'da tek hit b=6 çıkmıştı ve çift/sınır durumuydu — aynı disiplin).
4. Belirsiz hücreleri boş sayma: serbest parametre üzerinde geniş tarama (b≤500) + mümkünse yapısal argüman.
5. Sentez raporu `RESULTS.md`: teorem taslağı, aileler tablosu (det, kongrüans, d-vektör formülleri), periyot (lcm), kalıntı sayısı, n=6 ile yapısal karşılaştırma.

## Faz 4 — Literatür kapısı (sonuç ÇIKTIKTAN sonra)

Sonuç elde edilmeden literatüre bakma (önyargı olmasın). Çıktıktan sonra: Kay & Downes-Ward (JIS 2022 tek tabanlar; arXiv 2408.12257 çift tabanlar), Prichett–Ludington–Lapenta çizgisi, Iwasaki 2024. n=8 tek-taban karakterizasyonu yazılmış mı? RESULTS.md'ye dürüst atıf bölümü ekle.

## Tuzak uyarıları (n=6 deneyiminin dersleri)

1. **B=b−1 / C=b+1 karışıklığı:** tek kaynak `core.py`, her dosya oradan import etsin.
2. **Belirsiz hücreleri varsayımla kapatma** — tara ve tek hit çıkarsa kimliğini çıkar.
3. **Her sembolik sonucu sayısal zemine vur** — Faz 0 ground-truth her fazın hakemi.
4. **Sıralama hücrelerinde eşitlik sınırları** (a_i = a_{i+1}) belirsiz hücrelere düşer; komşu tekil hücre argümanıyla ele.
5. sympy yavaşsa lambdify ile sayısala çevir; sembolik yalnız sınıflandırma ve formül çıkarma için.
6. 40320 hücre × sympy çağrısı saatler sürebilir: paralel + önbellek + devam-edebilirlik ŞART.

## Başarı ölçütü

- Faz 0 n=6 doğrulaması birebir geçer.
- n=8 için tek-taban kongrüans birleşimi, b≤60 ground-truth ile sıfır uyumsuzluk.
- RESULTS.md'de: aileler tablosu, determinant spektrumu, periyot/kalıntı sayısı, n=6 karşılaştırması, dürüst "kanıtlı / taramayla kapalı / açık" statü etiketleri.

# n=6 Sertleştirme Raporu (genpipe ile tam kapanış)

*n=6 sonucunun, n=8 makinesinin (genpipe.py) aynı titizlik standardından
geçirilmesi — Temmuz 2026. Koşu: `python genpipe.py 6 60 150`, tüm
kontroller GEÇTİ.*

## 1. Teorem (n=6, her iki parite, altta yatan biçim)

Taban $b\ge2$, tam altı basamaklı Kaprekar sabit noktası barındırır ⟺
$$2\mid b \;\lor\; b\equiv 6\ (7) \;\lor\; b\equiv 8\ (9) \;\lor\;
  b\equiv 10\ (15).$$
Sporadik-yalnız taban **yoktur** (aile-dışı sporadik noktalar vardır ama
hepsi $b\le10$ ve o tabanlar zaten aile üyesidir). Tek tabanlara
kısıtlanınca modüller ikilenir ve bilinen sonuç birebir çıkar:
$$b\equiv 13\ (14)\ \lor\ b\equiv 17\ (18)\ \lor\ b\equiv 25\ (30).$$

| Kanal | Kongrüans | $d$-vektörü | Eşik |
|:-:|:-:|:--|:--|
| t=1 (k=4) | $b\equiv0\ (2)$ | $\left(\frac{B+1}{2},\frac{B+1}{2}\right)$ — palindromik $M_b$ | $b\ge2$ |
| t=0 (k=3) | $b\equiv6\ (7)$ | $\left(\frac{5B+3}{7},\frac{3B-1}{7},\frac{B+2}{7}\right)$ | $b\ge6$ |
| t=0 (k=3) | $b\equiv8\ (9)$ | $\left(\frac{7B+5}{9},\frac{5B+1}{9},\frac{B+2}{9}\right)$ | $b\ge8$ |
| t=0 (k=3) | $b\equiv10\ (15)$ | $\left(\frac{3B+3}{5},\frac{B}{3},\frac{B+1}{5}\right)$ | $b\ge10$ |

Periyot 630, kapsam 408/630 (≈%64,8); tek kalıntılar 186/630 = %29,5
(bilinen 93/315 ile özdeş).

## 2. Kapatılan iki formalite

1. **12 belirsiz hücre** (orijinal çalışmada 8 büyük asal tabanda ampirik
   kapatılmıştı): kesin 2D-LP ile **her b için** kapandı — 11'inin kısıt
   bölgesi boş, 1'i sınırlı ve GT kapsamında. 28 sabit-B belirsiz hücrenin
   tamamı $b\le60$'a düşüyor (GT kapatır). Sınırsız hücre yok.
2. **"Tek tabanda $d_2=0$ kanalı boş"** artık ampirik gözlem değil,
   sınıflandırma teoremi: t=1 kanalında belirsiz hücre yok, tek yaşayan
   aile $D=2$, kalıntı $b\equiv0$ (çift) → tek taban üyesi imkânsız;
   pencere/sporadikler sonlu ve tüketildi (hepsi $b\le10$).

## 3. Bağımsız çapraz doğrulama (dikkat çekici)

Orijinal n=6 çalışması (bağımsız, farklı kod tabanı): 720 sıralamadan
**568 tekil / 140 tutarsız / 12 belirsiz**. genpipe (bu koşu):
UNIQUE_ALL_B = **568**, INCONSISTENT + UNDERDET_FINITE_B = 112+28 =
**140**, UNDERDETERMINED = **12** — üç sayı da birebir. İki bağımsız
gerçekleştirme aynı hücre topolojisini buldu.

## 4. Mekanik envanter

- GT $b\le60$: 52 nokta; k dağılımı {3: 22, 4: 30}; kanal formülü
  uyuşmazlığı 0; GT = aile ∪ sporadik birebir; uzatma $b=61..150$
  nokta düzeyinde birebir (yeni sporadik yok).
- Hücreler: t=0: 720 (3 aile, 34 pencere), t=1: 360 (1 aile, belirsiz 0),
  t=2: 30 (aile yok, yalnız küçük-b penceresi) — k=5 kanalı asimptotik boş.
- RREF'siz verdikt denetimi: 600 hücre-B, uyuşmazlık 0.

**Statü: n=6 teoremi, n=8 ile aynı standartta, her parçasıyla
makine-kanıtlı ve bağımsız denetimli. Makale yazımına hazır.**

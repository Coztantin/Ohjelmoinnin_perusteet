> [!NOTE]
> Materiaali on luotu ChatGPT:n ja Copilotin avulla

# Viikko 5 - Tehtävä B: Kolmen viikon sähkönkulutus ja -tuotanto (kWh) tiedostoon

Tehtävänäsi on laatia Python-ohjelma, joka:

1. **Lukee tiedot tiedostoista `viikko41.csv`, `viikko42.csv` ja `viikko43.csv`**
2. **Laskee jokaiselle viikonpäivälle** (ma–su) samankaltaisen yhteenvedon kuin tehtävässä A:

   * vaiheittaisen **sähkönkulutuksen** (vaihe 1–3) **kWh-yksikössä**
   * vaiheittaisen **sähköntuotannon** (vaihe 1–3) **kWh-yksikössä**
3. **Tallentaa kaikki yhteenvedot tiedostoon `yhteenveto.txt`** selkeänä, käyttäjäystävällisenä raporttina (ei pelkkää raakadataa).

Tiedostot sisältävät viikkojen 41, 42 ja 43 tuntikohtaiset mittaukset:

* aika (päivämäärä ja kellonaika)
* kulutus kolmeen vaiheeseen jaettuna (Wh)
* tuotanto kolmeen vaiheeseen jaettuna (Wh)

Sinun tehtäväsi on **muuntaa Wh → kWh** ja esittää tulokset **kahden desimaalin tarkkuudella**, käyttäen **pilkkua desimaalierottimena** raportissa.

> [!NOTE]
> Halutessa työn voi tehdä **`pareittain (max. kaksi)`**. Tällöin kohdassa [Palautusohje Itslearningiin](#-palautusohje-itslearningiin) pari tekee vain yhden palautuksen, johon on yhdistetty molemmat.

---

## ⚖️ Yksikkö: Wh → kWh

Tiedostoissa arvot ovat **Wh**. Raportissa (`yhteenveto.txt`) kaikki energia-arvot tulee esittää **kWh**-yksikössä.

---

## 1️⃣ Ohjelman toiminnallisuus

Ohjelman tulee:

1. **Lukea kaikki kolme CSV-tiedostoa**: `viikko41.csv`, `viikko42.csv`, `viikko43.csv`.
2. **Laskea jokaiselle viikolle** (41, 42, 43) **päiväkohtaiset summat**:

   * viikonpäivä suomeksi (maanantai, tiistai, …)
   * päivän päivämäärä muodossa **pv.kk.vuosi** (esim. `13.10.2025`)
   * kulutus vaiheittain 1–3 (kWh, 2 desimaalia, pilkku desimaalina)
   * tuotanto vaiheittain 1–3 (kWh, 2 desimaalia, pilkku desimaalina)
3. **Kirjoittaa yhteenvedot tiedostoon `yhteenveto.txt`** seuraavalla ajatuksella:

* Raportissa on **selkeä otsikko jokaiselle viikolle**, esim.:

```text
Viikon 41 sähkönkulutus ja -tuotanto (kWh, vaiheittain)
Päivä        Pvm         Kulutus [kWh]              Tuotanto [kWh]
                         v1      v2      v3         v1      v2      v3
---------------------------------------------------------------------------
maanantai    06.10.2025  12,35   1,56    2,78       0,01   0,39    0,52
tiistai      07.10.2025  ...
...
sunnuntai    12.10.2025  ...
```

* Sama rakenne **viikoille 42 ja 43** saman raportin sisällä.
* Raportin lopussa **saa** olla esim. **lyhyt yhteenveto kaikista viikoista** (kokonaiskulutus ja -tuotanto), jos se helpottaa ohjelman rakentamista (tai teet sen bonus-ideana ⭐).

Tarkkaa tekstimuotoa ei ole betonoitu, mutta raportin tulee olla:

* **luettava ja looginen**
* **selkeästi jäsennelty** (otsikot, taulukkomaiset rivit, väliotsikot viikoille)

---

## 2️⃣ Funktioiden käyttö (pakollinen vaatimus)

Ohjelma pitää rakentaa **funktioiden varaan**, ei ”kaikki koodi suoraan tiedoston juureen”.

* Käytä **funktiota**, esim.:

```py
def lue_data(tiedoston_nimi: str) -> list:
    """Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa."""
    ...
```

* Funktiota, joka laskee **päiväkohtaiset yhteenvedot** yhdelle viikolle.
* Funktiota, joka **muodostaa rivit raporttia varten** (merkkijonoiksi).
* Funktiota, joka **kirjoittaa raportin** tiedostoon `yhteenveto.txt`.

* Tee myös **pääfunktio**, esimerkiksi:

```py
def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee viikkoyhteenvedot ja kirjoittaa raportin tiedostoon."""
    ...
```

* Lopussa:

```py
if __name__ == "__main__":
    main()
```

### 📚 Docstring-vaatimus

Jokaisella funktiolla tulee olla **docstring**, joka kertoo **mitä funktio tekee** lyhyesti ja selkeästi.

```py
def esimerkki(arvo: int) -> float:
    """Muuntaa kokonaisluvun liukuluvuksi ja palauttaa arvon kerrottuna kymmenellä."""
    ...
```

### 🔤 Tietotyyppivihjeet (type hints)

Kaikissa funktioissa tulee käyttää **tietotyyppivihjeitä**:

* parametrien tyypit
* palautusarvon tyyppi

Esimerkiksi:

```py
from datetime import datetime
from typing import List, Dict

def muunna_aika(aika_str: str) -> datetime:
    """Muuntaa ISO-muotoisen aikaleiman datetime-olioksi."""
    ...
```

---

## 3️⃣ MIT Copyright -merkintä

Kooditiedoston alkuun tulee laittaa **copyright- ja lisenssimerkintä**, esimerkiksi:

```py
# Copyright (c) 2025 Oma Nimi
# License: MIT
```

---

## 4️⃣ Päivämäärä & aika – käsittele **tietotyyppeinä**, älä tekstinä

**Tärkeä periaate:** Jos käytät **ehtolauseita** (`if`) tai vertailuja päivämäärien / aikojen kanssa, **älä vertaile raakatekstiä**, vaan käytä **oikeita tietotyyppejä** (`datetime`, `date`).

❌ Huono tapa (merkkijonovertailu):

```py
if aika_str[:10] == "2025-10-13":
    ...
```

--

✅ Parempi tapa:

```py
from datetime import datetime, date

aika = datetime.fromisoformat(aika_str)  # esim. "2025-10-13T00:00:00"
paiva = aika.date()

# esim. vertaillaan toiseen date-olioon
if paiva == date(2025, 10, 13):
    ...
```

---

## 5️⃣ Suomalaisten esitystapojen korostus

Raportissa (`yhteenveto.txt`):

1. **Päivämäärä**

   * Muoto: **pv.kk.vuosi**
   * Esim. `13.10.2025`
   * Voit muodostaa sen esimerkiksi:

   ```py
   pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"
   ```

2. **Desimaaliluvut** (kWh-arvot):

   * Esitetään **pilkulla**, ei pisteellä
   * Pyöristetään **kahteen desimaaliin**
   * Esimerkki:

   ```py
   arvo_kwh = 1.2345
   arvo_str = f"{arvo_kwh:.2f}"   # "1.23"
   arvo_str = arvo_str.replace(".", ",")  # "1,23"
   ```

---

## 6️⃣ Ohjelmoinnin perusrakenteet (pakolliset)

Ohjelmassa tulee käyttää ainakin:

* **Muuttujia** (esim. päiväkohtaiset summat, viikkotasoiset summat)
* **Listoja tai muita tietorakenteita** (esim. listat viikon päivistä)
* **Toistorakennetta** (`for`) rivien ja päivien läpikäyntiin
* **Ehtolauseita** (`if`) – erityisesti:

  * päivien ryhmittelyyn / valintaan
  * **mahdollisesti** ”parhaan / huonoimman” päivän valintaan
* **Funktioita**, joissa on:

  * docstring
  * tietotyyppivihjeet

Lisäksi tarvitaan:

* **Tiedoston kirjoittamista** (`open("yhteenveto.txt", "w", encoding="utf-8")`) käyttäen `with`-rakennetta, jotta tiedosto **sulkeutuu varmasti oikein**.

---

## 7️⃣ Bonus-ideat (vapaaehtoiset ⭐)

Halutessasi voit lisäksi:

1. **Laskea nettokulutuksen** (kulutus − tuotanto) joka päivälle ja näyttää sen raportissa.
2. **Korostaa parhaan päivän** (esim. pienin nettokulutus) tähdellä tai lisätekstillä.
3. **Lisätä koko viikon tason yhteenvedon** jokaiselle viikolle (kokonaiskulutus ja -tuotanto vaiheittain).
4. **Lisätä koko kolmen viikon yhteenvedon** raportin loppuun.
5. **Lisätä yksinkertaisen valikon** (esim. kysy käyttäjältä: ”Luodaanko raportti kaikista viikoista vai vain yhdestä viikosta?”).

---

## 📤 Palautusohje Itslearningiin

Palauta:

1. **Linkki GitHub-repoon**, jossa on:

   * Python-kooditiedosto (esim. `viikko5_tehtava_b.py`)
   * `yhteenveto.txt` (ohjelman generoima raportti) → **Varmista että tiedosto on saatavilla**
2. **Kuvankaappaus** VS Coden terminaalista tai hakemistorakenteesta, josta näkyy:

   * että ohjelma on ajettu
   * että tiedosto `yhteenveto.txt` on luotu

> [!NOTE]
> Jos työ on tehty **pareittain**, tehkää yksi yhteinen repo ja yksi yhteinen palautus, johon lisätään **molemmat**.

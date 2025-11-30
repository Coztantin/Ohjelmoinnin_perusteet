> [!NOTE]
> Materiaali on luotu ChatGPT:n ja Copilotin avulla

# 🐍 Varaustietojen käsitty (Osa A ja B)

## 🎯 Tavoite

Tehtävän tavoitteena on harjoitella:

* tietotyyppimuunnoksia Pythonisssa käyttäen erillistä funkiota
* listojen käsittelyä ja varausdatan rakenteistamista
* varausdatan tulostamista käyttäen silmuikoita ja ehtolauseita

> [!NOTE]
> Halutessa työn voi tehdä **`pareittain (max. kaksi)`**. Tällöin kohdassa [Palautusohje Itslearningiin](#-palautusohje-itslearningiin) pari tekee vain yhden palautuksen, johon on yhdistetty molemmat.

---

## 📄 Kuvaus

Sinulle on annettu:

* tekstitiedosto [**`varaukset.txt`**](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Oppimistehtavat/Viikko4/varaukset.txt), jossa jokainen rivi sisältää yhden varauksen tiedot.
* Python-skripti [**`lue_varaukset.py`**](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Oppimistehtavat/Viikko4/lue_varaukset.py), jossa on valmiiksi toteutettuja toiminnallisuuksia varauksien lukemiseen (mm. funktio `muunna_varaustiedot`)

**Esimerkkirivi `varaukset.txt` tiedostossa:**

```
201|Muumi Muumilaakso|muumi@valkoinenlaakso.org|0509876543|2025-11-12|09:00|2|18.50|True|Metsätila 1|2025-08-12 14:33:20
```

Rivillä on seuraavat tiedot:

| Sarake                 | Selite               | Tietotyyppi, jota tavoitellaan |
| ---------------------- | -------------------- | ------------------------------ |
| 1  `varausId`          | Varausnumero         | `int`                          |
| 2  `nimi`              | Varaajan nimi        | `str`                          |
| 3  `sähköposti`        | Varaajan sähköposti  | `str`                          |
| 4  `puhelin`           | Varaajan puhelin     | `str`                          |
| 5  `varauksenPvm`      | Varauspäivä          | `datetime.date`                |
| 6  `varauksenKlo`      | Aloitusaika          | `datetime.time`                |
| 7  `varauksenKesto`    | Tuntimäärä           | `int`                          |
| 8  `hinta`             | Tuntihinta (€)       | `float`                        |
| 9  `varausVahvistettu` | Vahvistettu          | `bool`                         |
| 10 `varattuTila`       | Varauskohde          | `str`                          |
| 11 `varausLuotu`       | Milloin varaus luotu | `datetime.datetime`            |

---

## 🧠 Osa A: `muunna_varaustiedot` kuntoon

Tässä osassa keskitytään yhden varausrivin muuntamiseen oikeisiin tietotyyppeihin..

> [!TIP]
> Aikaisemmista tehtävistä poiketen tässä funktio tekee heti lukemisen jälkeen muunnoksen ja ohjelma jatkaa muunnettujen tietojen kanssa.

---

### 1️⃣ Valmistelut

1. Kopioi tiedosto **`varaukset.txt`** omaan Git-repoosi ja kansioon `Viikko4`.
2. Kopioi Python-skripti **`lue_varaukset.py`** samaan `Viikko4`-kansioon.
3. Varmista, että ohjelma käynnistyy komennolla → `ohjelma tulostaa varaukset ja muuttamattomat tietotyypit`:

   ```bash
   python lue_varaukset.py
   ```
---

### 2️⃣ Funktio `muunna_varaustiedot`

Skriptissä on funktio nimeltä **`muunna_varaustiedot`**, joka saa parametrina **yhdestä rivistä splitatun listan**. Esim.:

```python
["201", "Muumi Muumilaakso", "muumi@valkoinenlaakso.org", "0509876543", "2025-11-12", "09:00:00", "2", "18.50", "True", "Metsätila 1", "2025-08-12 14:33:20"]
```

**Tehtäväsi on muuttaa funktiota `muunna_varaustiedot` niin, että se palauttaa listan, jossa sarakkeet ovat seuraavissa tietotyypeissä:**

```text
varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu

int | str | str | str | date | time | int | float | bool | str | datetime
```

> [!TIP]
> Käytä apuna Pythonin `datetime`-kirjastoa:

```python
from datetime import datetime, date, time
```

> [!TIP]
> Esimerkkejä muunnoksista (voit sovittaa omaan koodiisi):

```python
# 1) varausId: str -> int
varaus_id = int(rivi[0])

# 5) varauksenPvm: "2025-11-12" -> datetime.date
varauksen_pvm = datetime.strptime(rivi[4], "%Y-%m-%d").date()

# 6) varauksenKlo: "09:00" -> datetime.time
varauksen_klo = datetime.strptime(rivi[5], "%H:%M").time()

# 8) hinta: "18.50" -> float
hinta = float(rivi[7])

# 9) varausVahvistettu: "True"/"False" -> bool
varaus_vahvistettu = (rivi[8] == "True")

# 11) varausLuotu: "2025-08-12 14:33:20" -> datetime.datetime
varaus_luotu = datetime.strptime(rivi[10], "%Y-%m-%d %H:%M:%S")
```

**Lopuksi** funktio palauttaa listan, jossa kentät ovat oikeassa järjestyksessä ja tietotyypeissä.

> [!TIP]
> Esim. (ei ole pakko käyttää juuri tätä muuttujanimitystä ja/tapaa, mutta idea on sama):

```python
return [
    varaus_id, nimi, sahkoposti, puhelin,
    varauksen_pvm, varauksen_klo,
    varauksen_kesto, hinta,
    varaus_vahvistettu, varattu_tila,
    varaus_luotu
]
```

---

### 3️⃣ Testaus

Varmista, että ohjelma käynnistyy komennolla → `ohjelma tulostaa varaukset ja muutetut tietotyypit`:

```bash
python lue_varaukset.py
```
---

### 🧩 Vihjeitä

* Tutustu edellisten tehtävien: [viikko2](../Viikko2/README.md) ja [viikko3](../Viikko3/README.md) vihjeisiin
* Tutustu viikon 2 työpajalla tehtyyn ohjelmaan, joka löytyy [tästä linkistä](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Testikoodeja/Viikon2Tyopaja/lue_varaukset.py)
* Tutustu viikon 3 työpajalla tehtyyn ohjelmaan, joka löytyy [tästä linkistä](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Testikoodeja/Viikon3Tyopaja/lue_varaukset.py)
* **Katso Panoptosta viikon 3 työpajan tallenne**
* Tee muunnokset **pienissä paloissa**:

  * ensin `int` ja `float`
  * sitten `bool`
  * lopuksi `datetime.date`, `datetime.time` ja `datetime`
* Jos `datetime.strptime` antaa virheen, tarkista tarkasti:

  * millainen merkkijono tulee tiedostosta
  * että formaattimerkkijono (`"%Y-%m-%d %H:%M:%S"`) vastaa tarkalleen merkkijonon muotoa
* Voit lisätä väliaikaisia `print`-komentoja debuggausta varten (esim. `print(rivi[4], type(varauksen_pvm))`).
* **Jos et pääse eteenpäin, tule työpajaan! 😉**

---

## 🧠 Osa B: Varausten käsittely silmukoilla ja ehtolauseilla

Tässä osassa rakennat ohjelman, joka tulostaa **kerralla viisi erilaista yhteenvetoa** varauksista. Kaikkien tulosteiden tulee tulla **samassa ohjelman suorituksessa (eli annettaessa komento python lue_Varaukset.py kaikki tulostuvat tässä yhteydessä)**, järjestyksessä 1–5.

> [!IMPORTANT]
> Osan A tulostetta ei tarvita palautukseen. Pelkästään osasta B syntyvät tulosteet palautettavaan kuvakaappaukseen.

---

### 🧩 Vihjeitä

* Tutustu viikon 4 työpajalla tehtyyn ohjelmaan, joka löytyy [tästä linkistä](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Testikoodeja/Viikon4ATyopaja/lue_varaukset.py)
* **Katso Panoptosta viikon 4 työpajan tallenne**
* Pyri etenemään pienen askelin testaten aina, että onnistuiko muutokset vai ei.
* **Jos et pääse eteenpäin, tule työpajaan! 😉**

---

### 1️⃣ Tuloste: Kaikki vahvistetut varaukset

Tuloste alkaa otsikolla:

```
1) Vahvistetut varaukset
```

Ja jokainen varaus tulostuu muodossa:

```
- Nimi, Varattu tila, pv.kk.vvvv klo hh.mm
```

Esimerkkityyli:

```
1) Vahvistetut varaukset
- Muumi Muumilaakso, Metsätila 1, 12.11.2025 klo 09.00
- Pikku Myy Myrsky, Punainen huone, 22.10.2025 klo 15.45
```

---

### 2️⃣ Tuloste: Pitkät varaukset (kesto vähintään 3 h)

Otsikko:

```
2) Pitkät varaukset (≥ 3 h)
```

Muoto:

```
- Nimi, pv.kk.vvvv klo hh.mm, kesto X h, Varattu tila
```

---

### 3️⃣ Tuloste: Varaus vahvistettu vai ei?

Otsikko:

```
3) Varausten vahvistusstatus
```

Muoto:

```
Nimi → Vahvistettu
Nimi → EI vahvistettu
```

---

### 4️⃣ Tuloste: Yhteenveto vahvistetuista ja ei-vahvistetuista

Otsikko:

```
4) Yhteenveto vahvistuksista
```

Muoto:

```
- Vahvistettuja varauksia: X kpl
- Ei-vahvistettuja varauksia: Y kpl
```

---

### 5️⃣ Tuloste: Vahvistettujen varausten kokonaistulot (pilkulla!)

Otsikko:

```
5) Vahvistettujen varausten kokonaistulot
```

Muoto:

```
Vahvistettujen varausten kokonaistulot: 243,50 €
```

Huomaa rahasumman pilkku:

```python
summa_str = f"{summa:.2f}".replace(".", ",")
```

---

### 🔍 Miltä koko tuloste voisi näyttää? (Esimerkki)

> Tämä on vain hahmotelma, ei liitetyn tiedoston todellista sisältöä.

```
1) Vahvistetut varaukset
- Muumi Muumilaakso, Metsätila 1, 12.11.2025 klo 09.00
- Hemuli Kasvikerääjä, Kasvitutkimuslabra, 5.11.2025 klo 10.30

2) Pitkät varaukset (≥ 3 h)
- Pikku Myy Myrsky, 22.10.2025 klo 15.45, kesto 3 h, Punainen huone
- Nipsu Rahapulainen, 18.9.2025 klo 13.00, kesto 4 h, Varastotila N

3) Varausten vahvistusstatus
Muumi Muumilaakso → Vahvistettu
Niiskuneiti Muumilaakso → EI vahvistettu
Pikku Myy Myrsky → Vahvistettu

4) Yhteenveto vahvistuksista
- Vahvistettuja varauksia: 3 kpl
- Ei-vahvistettuja varauksia: 2 kpl

5) Vahvistettujen varausten kokonaistulot
Vahvistettujen varausten kokonaistulot: 243,50 €
```

---

### 💎1️⃣ Bonustuloste (valinnainen): Kallein varaus

Tuloste:

```text
Kallein varaus:
- Nimi: Muumi Muumilaakso
- Varattu tila: Metsätila 1
- Päivä: 12.11.2025
- Kellonaika: 09.00
- Kesto: 3 h
- Kokonaishinta: 55,50 €
```

---

### 💎2️⃣ Bonustuloste (valinnainen): Varausten määrä per päivä

Tuloste:

```text
Varausten määrä päivittäin:
- 18.9.2025: 1 kpl
- 22.10.2025: 1 kpl
- 5.11.2025: 1 kpl
- 12.11.2025: 2 kpl
```

---

### 💎3️⃣ Bonustuloste (valinnainen): Suodata varaukset tietyn tilan mukaan

Esim. käyttäjä antaa syötteen:

> [!TIP]
> Käytä funktiota `input("Anna tilan nimi: ")`

```text
Anna tilan nimi: Metsätila 1
```

Tuloste:

```text
Varaukset tilaan 'Metsätila 1':
- Muumi Muumilaakso, 12.11.2025 klo 09.00, kesto 3 h
- Niiskuneiti Muumilaakso, 1.12.2025 klo 14.15, kesto 2 h
```

---

### 💎4️⃣ Bonustuloste (valinnainen): Vain tulevat varaukset tiettyyn päivään asti

Esim. käyttäjä antaa syötteen:

> [!TIP]
> Käytä funktiota `input("Anna päivämäärä (pp.kk.vvvv): ")`

```text
Anna päivämäärä (pp.kk.vvvv): 1.10.2025
```

Tuloste:

```text
Varaukset annetun päivän jälkeen:
- Hemuli Kasvikerääjä, 5.11.2025 klo 10.30, Kasvitutkimuslabra
- Muumi Muumilaakso, 12.11.2025 klo 09.00, Metsätila 1
- Niiskuneiti Muumilaakso, 1.12.2025 klo 14.15, Kukkahuone
```

---

### 💎5️⃣ Bonustuloste (valinnainen): Keskimääräinen kesto vahvistetuille varauksille

Tuloste:

```text
Vahvistettujen varausten keskimääräinen kesto: 2,7 h
```

---

## 📤 Palautusohje Itslearningiin

Palauta **linkki GitHub-repoon** ja **kuvankaappaus konsolista**, jossa näkyy ohjelman suoritus ja tulostus.

> [!NOTE]
> Ota kuvakaappaus ilman bonustehtäviä ja osan A tulostetta.

Lisää palautukseen myös lyhyt teksti:
> Mitä jäi päällimmäisenä tehtävästä mieleen?

---

## 💬 Hyvä fiilis tekemiseen!

**Muista:** kaikki ohjelmoijat aloittavat jostain. Tärkeintä ei ole täydellinen koodi, vaan **oppiminen, kokeilu ja oivallus**. Pidä hauskaa ja tutki, miten ihan oikeita asioita ihan oikeasti tehdään! 🚀💡😎

---

## 💡 Yleisimmät virheet ja ratkaisut

| Virhe | Syy | Ratkaisu |
|-------|-----|----------|
| “Tiedostoa ei löydy” | Skriptiä ajetaan väärässä kansiossa | Siirry kansioon jossa skripti on |
| “Tiedostoa ei löydy” | Tiedostoja ei ole kopioitu | Kopioi tiedostot kansioosi |
| “Tiedostoa ei löydy” | Tiedostot on nimetty väärin | Varmista tiedostojen nimien oikeellisuus |
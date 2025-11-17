> [!NOTE]
> Materiaali on luotu ChatGPT:n ja Copilotin avulla.

# 🐍  Funktioiden käyttö

## 🎯 Tavoite

Tehtävän tavoitteena on harjoitella:

* funktioiden käyttöä Pythonissa
* tietotyyppimuunnoksien tekoa funktioiden sisällä
* ohjelman rakentamista, joka lukee ja tulostaa varausrivin rakenteellisesti

> [!NOTE]
> Halutessa työn voi tehdä **`pareittain (max. kaksi)`**. Tällöin kohdassa [Palautusohje Itslearningiin](#-palautusohje-itslearningiin) pari tekee vain yhden palautuksen, johon on yhdistetty molemmat.

---

## 📄 Kuvaus

* Sinulle on annettu tekstitiedosto **`varaukset.txt`**, jossa oleva rivi sisältää yhden varauksen tiedot.  
* Lisäksi sinulle on annettu Python-skripti **`lue_varaukset.py`**, joka lukee tiedostossa **`varaukset.txt`** olevat varaukset.  
* Tietoja on eroteltu pystypalkilla `|`. → Ohjelmassa on rivillä 32 `varaus = varaus.split('|')` → käytössä listatyyppinen muuttuja `varaus`

---

**Esimerkkirivi `varaukset.txt` tiedostossa:**

```
123|Anna Virtanen|2025-10-31|10:00|2|19.95|True|Kokoustila A|0401234567|anna.virtanen@example.com
```

---

Rivillä on seuraavat tiedot:

| Sarake | Selite         | Tietotyyppi                 |
| ------ | -------------- | --------------------------- |
| 1      | Varausnumero   | `int`                       |
| 2      | Varaajan nimi  | `str`                       |
| 3      | Varauspäivä    | `datetime.date`                  |
| 4      | Aloitusaika    | `datetime.time`             |
| 5      | Tuntimäärä     | `int`                       |
| 6      | Tuntihinta (€) | `float`                     |
| 7      | Maksettu       | `bool`                      |
| 8      | Varauskohde    | `str`                       |
| 9      | Puhelinnumero  | `str`                       |
| 10     | Sähköposti     | `str`                       |

---

## 🧠 Tehtäväohjeet

1. Kopioi tiedosto nimeltä **`varaukset.txt`** omaan `Git repoosi` ja kansioon `Viikko3`.
2. Kopioi Python-skripti nimeltä **`lue_varaukset.py`** omaan `Git repoosi` ja kansioon `Viikko3`.
3. Muokkaa skriptiä niin, että se tekee suoritettaessa seuraavaan tulosteen:

    ```
    Varausnumero: 123
    Varaaja: Anna Virtanen
    Päivämäärä: 31.10.2025
    Aloitusaika: 10.00
    Tuntimäärä: 2
    Tuntihinta: 19,95 €
    Kokonaishinta: 39,90 €
    Maksettu: Kyllä
    Kohde: Kokoustila A
    Puhelin: 0401234567
    Sähköposti: anna.virtanen@example.com
    ```
4. Ohjelmassa on **oma funktio jokaiselle tietotyypille ja tulostukselle** → Toteuta seuraavat funktiot:

    ```python
    def hae_varausnumero(varaus): ...
    def hae_varaaja(varaus): ...
    def hae_paiva(varaus): ...
    def hae_aloitusaika(varaus): ...
    def hae_tuntimaara(varaus): ...
    def hae_tuntihinta(varaus): ...
    def laske_kokonaishinta(varaus): ...
    def hae_maksettu(varaus): ...
    def hae_kohde(varaus): ...
    def hae_puhelin(varaus): ...
    def hae_sahkoposti(varaus): ...
    def laske_kokonaishinta(varaus): ...
    ```

---

### 🧩 Vihjeitä

* Tutustu edellisen [tehtävän](../Viikko2/README.md) vihjeisiin
* Viikon 2 työpajalla tehtyyn ohjelmaan, joka löytyy [tästä linkistä](https://github.com/vheikkiniemi/OhjelmoinninPerusteet2025S/blob/main/Testikoodeja/Viikon2Tyopaja/lue_varaukset.py)

---

## 🚀 Bonustehtävää (valinnaisia)

💎 **A)** Muuta tiedoston `varaukset.txt` sisältöä ja testaa, että tulostus on oikea  
💎 **B)** Tee funktio `tulosta_varaus(varaus)`, jota kutsutaan pääohjelmassa `main()` → `tulosta_varaus(varaus)` hoitaa tulostuksen kutsumalla tehtyjä funktioita  
💎 **C)** Lisää (*älä poista print-funkiota*) funktioihin `palautusarvo` → Esimerkkinä `laske_kokonaishinta(varaus)` → `return kokonaishinta`  
💎 **D)** Lisää funktioihin `tyyppivihjeet` → Esimerkkinä `laske_kokonaishinta(varaus: list[str]) -> float`  
💎 **E)** Lisää tiedostoon `varaukset.txt` useampi varaus ja tulosta kaikki rivit tiedostosta.  

---

## 📤 Palautusohje Itslearningiin

Palauta **linkki GitHub-repoon** ja **kuvankaappaus konsolista**, jossa näkyy ohjelman suoritus ja tulostus.

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
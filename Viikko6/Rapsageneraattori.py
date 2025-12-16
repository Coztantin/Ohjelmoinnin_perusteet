# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee csv-tiedostot ja tulostaa näistä raportin tekstitiedostoon, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import date, datetime
from datetime import timezone
import time
import csv
import glob
from typing import List, Dict, Optional
from typing import Dict, Any
from collections import defaultdict

tunti_lista= []
viikonpaivat = []
tiedostot = []
tiedostolista = []
viikko = []
paivaobjekti_lista = []
Yksi_paiva = {}

viikonpaivat_kaantaja_en_fi = {
    "Monday": "Maanantai",
    "Tuesday": "Tiistai",
    "Wednesday": "Keskiviikko",
    "Thursday": "Torstai",
    "Friday": "Perjantai",
    "Saturday": "Lauantai",
    "Sunday": "Sunnuntai"
}
kuukaudet_kaantaja_en_fi = {
    "January": "Tammikuu",
    "February": "Helmikuu",
    "March": "Maaliskuu",
    "April": "Huhtikuu",
    "May": "Toukokuu",
    "June": "Kesäkuu",
    "July": "Heinäkuu",
    "August": "Elokuu",
    "September": "Syyskuu",
    "October": "Lokakuu",
    "November": "Marraskuu",
    "December": "Joulukuu"
}

def luetiedostot() -> list:
    '''Hakee kaikki csv-tiedostot annetusta kansiosta.'''
    print(" ")
    print("Luetaan kansiosta *.csv tiedostot.")

    tiedostolista = sorted(glob.glob("*.csv"))
    print("Kansiossa olevat tiedostot:", tiedostolista)
    return tiedostolista
    
def kasittele_Viikkodata(tiedostolista:list[str]) -> Dict[datetime,Dict[str,Any]]:
    '''Lukee tiedostot ja muodostaa kaikista listan arvoista sanakirjoina. Koska kyseessä on suhteellisen pieni tiedostokoko (alle 500KB), vaikka siihen lisättäisiin viimeinen
    kuukausi dataa, voidaan kaikki tiedot lukea kerralla muistiin. Tekoälyn mukaan, jos tiedostokoko olisi yli 10-50MB TAI yli 100 000 riviä, tulisi harkita eri lähestymistapaa.
    Turha lähtee pilkkomaan.'''

    kaikki_tunnit = {}
    
    for tiedosto in tiedostolista:
        print(f"Käsitellään tiedostoa:{tiedosto}")

        with open(tiedosto, "r", newline="", encoding="utf-8") as f:
            rivit = f.readlines()[1:]  # Ohitetaan otsikkorivi
            for rivi in rivit:

                rivi= rivi.strip().split(";")
                ajankohta_obj = datetime.strptime(rivi[0], "%Y-%m-%dT%H:%M:%S.%f%z") # Muutetaan aikaleima objektiksi
                vko_nro = ajankohta_obj.isocalendar().week
                kk_nro = ajankohta_obj.month
                viikonpaiva = viikonpaivat_kaantaja_en_fi[ajankohta_obj.strftime("%A")]
                pvm_tunti = ajankohta_obj
                #Luodaan sanakirja jokaiselle ajalle, vaiheelle ja muokataan se sopivaksi.
                kaikki_tunnit[pvm_tunti] = {
                    "Vuosi": ajankohta_obj.year,
                    "Kuukausi": kk_nro,
                    "Viikko": vko_nro,
                    "Päivä": viikonpaiva,
                    "Kulutus nettona (kWh)": float(rivi[1].replace(",", ".")),
                    "Tuotanto nettona (kWh)": float(rivi[2].replace(",", ".")),
                    "Vuorokauden keskilämpötila": float(rivi[3].replace(",", "."))
                }
    return kaikki_tunnit

def paivalaskut(kaikki_tunnit: Dict[datetime,Dict[str,Any]]):
    '''Antaa päiville päivämäärät, tekee viikkolistan ja summaa tuntien arvot päiville.'''

    #Tehdään yhdelle vuorokaudelle sanakirja, josta tehdään sitten lista eri päivämäärille.
    Yksi_paiva= defaultdict(lambda: {
        "Vuosi": "",
        "Kuukausi": "",
        "Viikko": "",
        "Päivä": "",
        "Aika": "",
        "Kulutus nettona (kWh)": 0.0,
        "Tuotanto nettona (kWh)": 0.0,
        "Vuorokauden keskilämpötila": None
        })
    
    #Käydään tunnit läpi ja tehdään päivämäärä sanakirja, ja lisätään arvot oikeille päiville.
    for paivaobj, arvot in kaikki_tunnit.items():
      
        pvm = paivaobj.date()
        vko_nimi = f"vko{pvm.isocalendar().week}"

        paiva = Yksi_paiva[pvm]
        paiva["Vuosi"] = pvm.year
        paiva["Kuukausi"] = pvm.month
        paiva["Viikko"] = vko_nimi
        paiva["Päivä"] = viikonpaivat_kaantaja_en_fi[paivaobj.strftime("%A")]
        paiva["Aika"] = pvm.strftime("%d.%m.%Y")
        paiva["Kulutus nettona (kWh)"] += arvot["Kulutus nettona (kWh)"]
        paiva["Tuotanto nettona (kWh)"] += arvot["Tuotanto nettona (kWh)"]
        if paiva["Vuorokauden keskilämpötila"] is None:
            paiva["Vuorokauden keskilämpötila"] = arvot["Vuorokauden keskilämpötila"]
    
    return dict(Yksi_paiva)

def tulosta_kaikki(Yksi_paiva: dict) -> None:
    '''Tulostaa tiedostojen päivät konsoliin. Erottelee viikot viivalla.'''
    edellinen_viikko = None
    Vuosi_W = 7
    Kuukausi_W = 10
    Viikko_W = 10
    Päivämäärä_W = 15
    Päivä_W = 15
    Kulutus_W = 30
    Tuotanto_W = 30
    Lämpötila_W = 33
    viivojen_pituus = Vuosi_W + Kuukausi_W + Viikko_W + Päivämäärä_W + Päivä_W + Kulutus_W + Tuotanto_W + Lämpötila_W


    print(" ")
    print("-"*viivojen_pituus)
    print("sähkönkulutus ja -tuotanto nettona kWh-yksikössä kaikista päivistä:")
    print("-"*viivojen_pituus)
    print(" ")
    print("-"*viivojen_pituus)
    print(
        f"{'Vuosi':<{Vuosi_W}}"+
        f"{'Kuukausi':<{Kuukausi_W}}"+
        f"{'Viikko':<{Viikko_W}}"+
        f"{'Päivämäärä':<{Päivämäärä_W}}"+
        f"{'Päivä':<{Päivä_W}}"+
        f"{'Kulutus nettona (kWh)':>{Kulutus_W}}"+
        f"{'Tuotanto nettona (kWh)':>{Tuotanto_W}}"+
        f"{'Vuorokauden keskilämpötila':>{Lämpötila_W}}"
        )
    print("-"*viivojen_pituus)
    print("-"*viivojen_pituus)

    for paiva in Yksi_paiva.values():
        nykyinen_viikko = paiva["Viikko"]
        if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:
            print("-"*viivojen_pituus)

        print(
            f"{paiva['Vuosi']:<{Vuosi_W}}"+
            f"{paiva['Kuukausi']:<{Kuukausi_W}}"+
            f"{paiva['Viikko'].removeprefix('vko'):<{Viikko_W}}"+
            f"{paiva['Aika']:<{Päivämäärä_W}}"+
            f"{paiva['Päivä']:<{Päivä_W}}"+
            f"{paiva['Kulutus nettona (kWh)']:>{Kulutus_W}.2f}".replace('.', ',')+
            f"{paiva['Tuotanto nettona (kWh)']:>{Tuotanto_W}.2f}".replace('.', ',')+
            f"{paiva['Vuorokauden keskilämpötila']:>{Lämpötila_W}}"
            )
        edellinen_viikko = nykyinen_viikko # Päivitetään edellinen viikko.

def tulosta_vuosi(Yksi_paiva: dict, vuosi: int) -> None:
    '''Tulostaa tiedostojen päivät konsoliin. Erottelee viikot viivalla.'''
    
    #Muodostetaan Filtteri vuodelle.
    paivat_vuodelta = {
        k: v for k, v in Yksi_paiva.items()
        if v["Vuosi"] == vuosi
    }
    if not paivat_vuodelta:
        print(f"Vuodelta {vuosi} ei löydy tietoja.")
        return

    #Määritetään sarakkeiden leveydet ja viivojen pituus
    edellinen_viikko = None
    Vuosi_W = 7
    Kuukausi_W = 10
    Viikko_W = 10
    Päivämäärä_W = 15
    Päivä_W = 15
    Kulutus_W = 30
    Tuotanto_W = 30
    Lämpötila_W = 33
    viivojen_pituus = Vuosi_W + Kuukausi_W + Viikko_W + Päivämäärä_W + Päivä_W + Kulutus_W + Tuotanto_W + Lämpötila_W

    # Tulostetaan otsikot ja muotoilut
    print(" ")
    print("-"*viivojen_pituus)
    print("sähkönkulutus ja -tuotanto nettona kWh-yksikössä kaikista päivistä:")
    print("-"*viivojen_pituus)
    print(" ")
    print("-"*viivojen_pituus)
    print(
        f"{'Vuosi':<{Vuosi_W}}"+
        f"{'Kuukausi':<{Kuukausi_W}}"+
        f"{'Viikko':<{Viikko_W}}"+
        f"{'Päivämäärä':<{Päivämäärä_W}}"+
        f"{'Päivä':<{Päivä_W}}"+
        f"{'Kulutus nettona (kWh)':>{Kulutus_W}}"+
        f"{'Tuotanto nettona (kWh)':>{Tuotanto_W}}"+
        f"{'Vuorokauden keskilämpötila':>{Lämpötila_W}}"
        )
    print("-"*viivojen_pituus)
    print("-"*viivojen_pituus)
    
    # Suodatetaan ja tulostetaan vain halutun vuoden päivät
    # Jotta saadaan viikot eroteltua, tarkistetaan edellinen viikko ja verrataan sitä nykyiseen.

    for paiva in paivat_vuodelta.values():
        nykyinen_viikko = paiva["Viikko"]
        
        if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:
            print("-"*viivojen_pituus)

        print(
            f"{paiva['Vuosi']:<{Vuosi_W}}"+
            f"{paiva['Kuukausi']:<{Kuukausi_W}}"+
            f"{paiva['Viikko'].removeprefix("vko"):<{Viikko_W}}"+
            f"{paiva['Aika']:<{Päivämäärä_W}}"+
            f"{paiva['Päivä']:<{Päivä_W}}"+
            f"{paiva['Kulutus nettona (kWh)']:>{Kulutus_W}.2f}".replace('.', ',')+
            f"{paiva['Tuotanto nettona (kWh)']:>{Tuotanto_W}.2f}".replace('.', ',')+
            f"{paiva['Vuorokauden keskilämpötila']:>{Lämpötila_W}}"
            )
        edellinen_viikko = nykyinen_viikko # Päivitetään edellinen viikko.
    print("-"*viivojen_pituus)

def tulosta_kuukausi(Yksi_paiva: dict, kuukausi: int) -> None:
    '''Tulostaa tiedostojen päivät konsoliin. Erottelee viikot viivalla.'''
    
    #Muodostetaan Filtteri kuukaudelle.
    paivat_kuukaudelta = {
        k: v for k, v in Yksi_paiva.items()
        if v["Kuukausi"] == kuukausi and v["Vuosi"] == datetime.now().year
    }
    if not paivat_kuukaudelta:
        print(f"Kuukaudelta {kuukausi} ei löydy tietoja.")
        return

    #Määritetään sarakkeiden leveydet ja viivojen pituus
    edellinen_viikko = None
    Vuosi_W = 7
    Kuukausi_W = 10
    Viikko_W = 10
    Päivämäärä_W = 15
    Päivä_W = 15
    Kulutus_W = 30
    Tuotanto_W = 30
    Lämpötila_W = 33
    viivojen_pituus = Vuosi_W + Kuukausi_W + Viikko_W + Päivämäärä_W + Päivä_W + Kulutus_W + Tuotanto_W + Lämpötila_W

    # Tulostetaan otsikot ja muotoilut
    print(" ")
    print("-"*viivojen_pituus)
    print("sähkönkulutus ja -tuotanto nettona kWh-yksikössä kaikista päivistä:")
    print("-"*viivojen_pituus)
    print(" ")
    print("-"*viivojen_pituus)
    print(
        f"{'Vuosi':<{Vuosi_W}}"+
        f"{'Kuukausi':<{Kuukausi_W}}"+
        f"{'Viikko':<{Viikko_W}}"+
        f"{'Päivämäärä':<{Päivämäärä_W}}"+
        f"{'Päivä':<{Päivä_W}}"+
        f"{'Kulutus nettona (kWh)':>{Kulutus_W}}"+
        f"{'Tuotanto nettona (kWh)':>{Tuotanto_W}}"+
        f"{'Vuorokauden keskilämpötila':>{Lämpötila_W}}"
        )
    print("-"*viivojen_pituus)
    print("-"*viivojen_pituus)

    # Suodatetaan ja tulostetaan vain halutun kuukauden päivät
    # Jotta saadaan viikot eroteltua, tarkistetaan edellinen viikko ja verrataan sitä nykyiseen.
    for paiva in paivat_kuukaudelta.values():
        nykyinen_viikko = paiva["Viikko"]
        
        if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:
            print("-"*viivojen_pituus)

        print(
            f"{paiva['Vuosi']:<{Vuosi_W}}"+
            f"{paiva['Kuukausi']:<{Kuukausi_W}}"+
            f"{paiva['Viikko'].removeprefix("vko"):<{Viikko_W}}"+
            f"{paiva['Aika']:<{Päivämäärä_W}}"+
            f"{paiva['Päivä']:<{Päivä_W}}"+
            f"{paiva['Kulutus nettona (kWh)']:>{Kulutus_W}.2f}".replace('.', ',')+
            f"{paiva['Tuotanto nettona (kWh)']:>{Tuotanto_W}.2f}".replace('.', ',')+
            f"{paiva['Vuorokauden keskilämpötila']:>{Lämpötila_W}}"
            )
        edellinen_viikko = nykyinen_viikko # Päivitetään edellinen viikko.
    print("-"*viivojen_pituus)

def tulosta_viikko(Yksi_paiva: dict, viikko: int) -> None:
    '''Tulostaa tiedostoista tietyt viikot konsoliin. Erottelee viikot viivalla.'''
    #Muodostetaan Filtteri viikolle.
    paivat_viikolta = {
        k: v for k, v in Yksi_paiva.items()
        if v["Viikko"] == f"vko{viikko}" and v["Vuosi"] == datetime.now().year
    }
    if not paivat_viikolta:
        print(f"Viikolta {viikko} ei löydy tietoja.")
        return
    
    #Määritetään sarakkeiden leveydet ja viivojen pituus
    Vuosi_W = 7
    Kuukausi_W = 10
    Viikko_W = 10
    Päivämäärä_W = 15
    Päivä_W = 15
    Kulutus_W = 30
    Tuotanto_W = 30
    Lämpötila_W = 33
    viivojen_pituus = Vuosi_W + Kuukausi_W + Viikko_W + Päivämäärä_W + Päivä_W + Kulutus_W + Tuotanto_W + Lämpötila_W
    
    # Tulostetaan otsikot ja muotoilut
    print(" ")
    print("-"*viivojen_pituus)
    print("sähkönkulutus ja -tuotanto nettona kWh-yksikössä kaikista päivistä:")
    print("-"*viivojen_pituus)
    print(" ")
    print("-"*viivojen_pituus)
    print(
        f"{'Vuosi':<{Vuosi_W}}"+
        f"{'Kuukausi':<{Kuukausi_W}}"+
        f"{'Viikko':<{Viikko_W}}"+
        f"{'Päivämäärä':<{Päivämäärä_W}}"+
        f"{'Päivä':<{Päivä_W}}"+
        f"{'Kulutus nettona (kWh)':>{Kulutus_W}}"+
        f"{'Tuotanto nettona (kWh)':>{Tuotanto_W}}"+
        f"{'Vuorokauden keskilämpötila':>{Lämpötila_W}}"
        )
    print("-"*viivojen_pituus)
    print("-"*viivojen_pituus)         

    # Suodatetaan ja tulostetaan vain halutun viikon päivät
    for paiva in paivat_viikolta.values():
        print(
            f"{paiva['Vuosi']:<{Vuosi_W}}"+
            f"{paiva['Kuukausi']:<{Kuukausi_W}}"+
            f"{paiva['Viikko'].removeprefix("vko"):<{Viikko_W}}"+
            f"{paiva['Aika']:<{Päivämäärä_W}}"+
            f"{paiva['Päivä']:<{Päivä_W}}"+
            f"{paiva['Kulutus nettona (kWh)']:>{Kulutus_W}.2f}".replace('.', ',')+
            f"{paiva['Tuotanto nettona (kWh)']:>{Tuotanto_W}.2f}".replace('.', ',')+
            f"{paiva['Vuorokauden keskilämpötila']:>{Lämpötila_W}}"
            )
    print("-"*viivojen_pituus)

def tulosta_paiva(tunti_arvot: dict, paiva: date) -> None:
    '''Tulostaa tiedostoista tietyn päivän konsoliin tunneittain.'''
    #Muodostetaan Filtteri päivälle.
    tunnit = {
        aika: arvot
        for aika, arvot in tunti_arvot.items()
        if aika.date() == paiva
    }
    if not tunnit:
        print(f"Päivältä {paiva.strftime('%d.%m.%Y')} ei löydy tietoja.")
        return
    
    #Määritetään sarakkeiden leveydet ja viivojen pituus
    Vuosi_W = 7
    Kuukausi_W = 10
    Viikko_W = 10
    Päivämäärä_W = 15
    Päivä_W = 15
    Klo_W = 6
    Kulutus_W = 30
    Tuotanto_W = 30
    Lämpötila_W = 33
    viivojen_pituus = Vuosi_W + Kuukausi_W + Viikko_W + Päivämäärä_W + Päivä_W + Klo_W + Kulutus_W + Tuotanto_W + Lämpötila_W
    
    # Tulostetaan otsikot ja muotoilut
    print(" ")
    print("-"*viivojen_pituus)
    print("sähkönkulutus ja -tuotanto nettona kWh-yksikössä kaikista päivistä:")
    print("-"*viivojen_pituus)
    print(" ")
    print("-"*viivojen_pituus)
    print(
        f"{'Vuosi':<{Vuosi_W}}"+
        f"{'Kuukausi':<{Kuukausi_W}}"+
        f"{'Viikko':<{Viikko_W}}"+
        f"{'Päivämäärä':<{Päivämäärä_W}}"+
        f"{'Päivä':<{Päivä_W}}"+
        f"{'Klo':<{Klo_W}}"+
        f"{'Kulutus nettona (kWh)':>{Kulutus_W}}"+
        f"{'Tuotanto nettona (kWh)':>{Tuotanto_W}}"+
        f"{'Vuorokauden keskilämpötila':>{Lämpötila_W}}"
        )
    print("-"*viivojen_pituus)
    print("-"*viivojen_pituus)

    # Suodatetaan ja tulostetaan vain halutun päivän tiedot
    for aika in sorted(tunnit.keys()):
        arvot = tunnit[aika]
        print(
            f"{arvot['Vuosi']:<{Vuosi_W}}"+
            f"{arvot['Kuukausi']:<{Kuukausi_W}}"+
            f"{f'{aika.isocalendar().week}':<{Viikko_W}}"+
            f"{aika.strftime('%d.%m.%Y'):<{Päivämäärä_W}}"+
            f"{viikonpaivat_kaantaja_en_fi[aika.strftime('%A')]:<{Päivä_W}}"+
            f"{aika.strftime('%H:%M'):<{Klo_W}}"+ 
            f"{arvot['Kulutus nettona (kWh)']:>{Kulutus_W}.2f}"+
            f"{arvot['Tuotanto nettona (kWh)']:>{Tuotanto_W}.2f}" +
            f"{arvot['Vuorokauden keskilämpötila']:>{Lämpötila_W-3}.1f} °C"
            )
    print("-"*viivojen_pituus)

def rapsan_luonti(paivakohtaiset_tulokset) -> str:
    '''Luo raportin sisällön yhtenä stringinä. Eikö tähän löydy parempaa tapaa?'''

    rapsa = ""
    edellinen_viikko = None

    rapsa += ("-"*210 + "\n")
    rapsa += "Viikkojen sähkönkulutus ja -tuotanto kWh-yksikössä:\n"
    rapsa += ("-"*210 + "\n")
    rapsa += ("-"*210 + "\n")
    rapsa += ("Viikko/Päivä".ljust(17) + "Päivämäärä".ljust(10) + "Kulutus vaihe 1 kWh".rjust(25) + "Kulutus vaihe 2 kWh".rjust(25) + "Kulutus vaihe 3 kWh".rjust(25) + "Tuotanto vaihe 1 kWh".rjust(25) + "Tuotanto vaihe 2 kWh".rjust(25) + "Tuotanto vaihe 3 kWh".rjust(25) + "\n")
    rapsa += ("-"*210 + "\n")

    for paiva in paivakohtaiset_tulokset:
        nykyinen_viikko = paiva["Viikko"]
        if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:
            rapsa += ("-"*210 + "\n")

        rapsa +=    f"{paiva['Viikko'].removeprefix('vko').ljust(5)}" \
                    f"{paiva['Päivä'].ljust(14)}" \
                    f"{paiva['Aika'].strftime('%d.%m.%Y').ljust(10)}" \
                    f"{f'{paiva['Kulutus_vaihe1']:.2f}'.replace(".", ",").rjust(25)}" \
                    f"{f'{paiva['Kulutus_vaihe2']:.2f}'.replace(".", ",").rjust(25)}" \
                    f"{f'{paiva['Kulutus_vaihe3']:.2f}'.replace(".", ",").rjust(25)}" \
                    f"{f'{paiva['Tuotanto_vaihe1']:.2f}'.replace(".", ",").rjust(25)}" \
                    f"{f'{paiva['Tuotanto_vaihe2']:.2f}'.replace(".", ",").rjust(25)}" \
                    f"{f'{paiva['Tuotanto_vaihe3']:.2f}'.replace(".", ",").rjust(25)}\n"
    
        edellinen_viikko = nykyinen_viikko
    rapsa += ("-"*210 + "\n")
    return rapsa

def luo_txt_tiedosto(rapsa) -> None:
    '''Luo raportin tekstitiedostoon Raporttipinkka kansioon.'''
    nyt = datetime.now()
    tiedoston_nimi = f"Raporttipinkka/{nyt.strftime('%H-%d-%m')}_viikkorapsa.txt"

    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        f.write(rapsa)
    print(f"Raportti luotu tiedostoon: {tiedoston_nimi}")

def paavalikko(tunti_arvot: dict, paivadata: dict) -> None | Optional[datetime]:
    '''Valikko käyttäjälle.'''
    input("\n Paina Enter jatkamiseksi...")
    while True:
        print(" ")
        print("=== VALIKKO ===")
        print("Mitä tänän saisi olla? Valitse alla olevista vaihtoehdoista:")
        print("1 - Tulosta kaikki päivät konsoliin")
        print("2 - Tulosta haluamasi vuoden kokonaisuudessaan konsoliin")
        print("3 - Tulosta haluamasi kuluvan vuoden kuukauden yhteenveto konsoliin")
        print("4 - Tulosta haluamasi kuluvan vuoden viikon yhteenveto konsoliin")
        print("5 - Tulosta haluamasi päivän tiedot konsoliin tunneittain, PREMIUM-JÄSENILLE")
        print("6 - Poistu ohjelmasta")
        valinta = input("Valintasi: ").strip().upper()
        if valinta not in ["1", "2", "3", "4", "5", "6"]:
            print("Virheellinen valinta. Yritä uudelleen.")

        if valinta == "1":
            print("Valitsit vaihtoehdon 1: Tulosta kaikki päivät konsoliin")
            print("Haluatko jatkaa? (K/E)")
            jatka = input().strip().upper()
            if jatka == "K":
                print("Haetaan ja tulostetaan kaikki päivät:")
                time.sleep(1)
                tulosta_kaikki(paivadata)
                input("\n Paina Enter jatkamiseksi...")

        if valinta == "2":
            print("Valitsit vaihtoehdon 2: Tulosta haluamasi vuoden kokonaisuudessaan konsoliin")
            print("Haluatko jatkaa? (K/E)")
            jatka = input().strip().upper()
            if jatka == "K":
                vuosi = paavalikko_2_vuosi()
                print("Haetaan ja tulostetaan tiedot vuodelta:", vuosi)
                time.sleep(1)
                tulosta_vuosi(paivadata, vuosi)
                input("\n Paina Enter jatkamiseksi...")
                
        
        if valinta == "3":
            print("Valitsit vaihtoehdon 3: Tulosta haluamasi kuluvan vuoden kuukauden yhteenveto konsoliin")
            print("Haluatko jatkaa? (K/E)")
            jatka = input().strip().upper()
            if jatka == "K":
                kuukausi = paavalikko_3_kuukausi()
                kk_en = datetime(2000, kuukausi, 1).strftime("%B")
                kk_fi = kuukaudet_kaantaja_en_fi[kk_en]
                print("Haetaan ja tulostetaan tiedot kuukaudelta:", kk_fi)
                time.sleep(1)
                tulosta_kuukausi(paivadata, kuukausi)
                input("\n Paina Enter jatkamiseksi...")
        
        if valinta == "4":
            print("Valitsit vaihtoehdon 4: Tulosta haluamasi kuluvan vuoden viikon yhteenveto konsoliin")
            print("Haluatko jatkaa? (K/E)")
            jatka = input().strip().upper()
            if jatka == "K":
                viikko = paavalikko_4_viikko()
                print("Haetaan ja tulostetaan tiedot viikolta:", viikko)
                time.sleep(1)
                tulosta_viikko(paivadata, viikko)
                input("\n Paina Enter jatkamiseksi...")

        if valinta == "5":
            print("Valitsit vaihtoehdon 5: Tulosta haluamasi päivän tiedot konsoliin tunneittain, PREMIUM-JÄSENILLE")
            print("Haluatko jatkaa? (K/E)")
            jatka = input().strip().upper()
            if jatka == "K":
                paiva = paavalikko_5_paiva()
                if paiva is None:
                    # Käyttäjä ei ole premium-jäsen, palataan valikkoon
                    continue
                print("Haetaan ja tulostetaan tiedot päivältä:", paiva.strftime("%d.%m.%Y"))
                time.sleep(1)
                tulosta_paiva(tunti_arvot, paiva)
                input("\n Paina Enter jatkamiseksi...")

        if valinta == "6":
            print("Jaaha, Rahaa ja lämpöä on on niin paljon, että voi jakaa harakoillekkin. Ei siin mittää sit... Palaillaan toiste!")
            print("Ohjelma suljetaan.")
            return

def paavalikko_2_vuosi() -> int:
    '''Päävalikon alivalikko vuoden valintaan.'''
    while True:
    
        vuosi_input = input("Anna haluamasi vuosi muodossa vvvv (esim. 2023): ")
        try:
            vuosi = int(vuosi_input)
            if 2000 <= vuosi <= 2100:
                return vuosi
            else:
                print("Anna Nyt jotain järkevää, jotain tältä vuosisadalta!")
        except ValueError:
            print("Virheellinen syöte. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def paavalikko_3_kuukausi() -> int:
    '''Päävalikon alivalikko kuukauden valintaan.'''
    while True:

        kuukausi_input = input("Anna haluamasi kuukausi muodossa kk (esim. 01): ")
        try:
            vuosi = datetime.now().year
            kuukausi = int(kuukausi_input)
            if 1 <= kuukausi <= 12 and vuosi == datetime.now().year:
                return kuukausi
            else:
                print("Anna Nyt jotain järkevää, jotain kuukauden numero välillä 1-12!")
        except ValueError:
            print("Virheellinen syöte. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def paavalikko_4_viikko() -> int:
    '''Päävalikon alivalikko viikon valintaan.'''
    while True:
        vuosi = datetime.now().year
        viikko_input = input("Anna haluamasi viikkon numero (esim. 1 tai 42): ")
        try:
            vuosi = datetime.now().year
            viikko = int(viikko_input)
            if 1 <= viikko <= 52 and vuosi == datetime.now().year:
                return viikko
            else:
                print("Anna Nyt jotain järkevää, jotain viikon numero välillä 1-52!")
        except ValueError:
            print("Virheellinen syöte. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def paavalikko_5_paiva() -> Optional[date]:
    '''Päävalikon alivalikko päivän valintaan.'''
    premium_jasen = input("Oletko PREMIUM-JÄSEN? (K/E): ").strip().upper()
    if premium_jasen != "K":
        print("Valitettavasti tämä ominaisuus on saatavilla vain PREMIUM-JÄSENILLE.")
        return None
        

    while True:
        paiva_input = input("Anna haluamasi päivä muodossa pp.kk.vvvv (esim. 05.03.2023): ")
        try:
            return datetime.strptime(paiva_input, "%d.%m.%Y").date()
        except ValueError:
            print("Virheellinen päivämäärä. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def Mainos() -> None:
    '''Mainokset pääsi mystisesti tähän ohjelmaan.'''

    premium_mainos = str("PREMIUM-JÄSENYYS: VAIN 9,99 €kk!")
    premium_mainos_raamit = str("#")
    pisin_teksti = str( "No ei hätää, me autamme sinua tässä asiassa! Nyt voit saada selville sähkönkulutuksesi ja -tuotantosi päivä-, viikko-, ja kuukausitasolla helposti ja nopeasti!")
    print(" ")
    print("-"*len(pisin_teksti))
    print("Tervetuloa AurinkoSähköPaneelirapsageneraattori Palveluun!")
    print(" ")
    print("Tulitko hakemaan viikkoraporttia sähkönkulutuksesta ja -tuotannosta? Vai tulitko vertailemaan päivittäistä sähkönkulutusta ja -tuotantoa?")
    print("Etkö tiedä mikä kuluttaa hirveästi sähköä? Puolisosi on taas torkkunut sähköpeiton alla? Lapset pelaa yötämyöhään pleikkarilla?")
    print(pisin_teksti)
    print("Maksamalla premium-jäsenyyden saat vielä tarkemmat raportit ja analyysit sähkönkulutuksestasi ja -tuotannostasi! Nyt voit selvittää mihin sähkö oikein kuluu!")
    print("")
    print('#'*(len(premium_mainos + premium_mainos_raamit*2)+4))
    print('#' + ' '*(len(premium_mainos + premium_mainos_raamit*2)+2) + '#')
    print(f"#  {premium_mainos}  #")
    print("#" + ' '*(len(premium_mainos + premium_mainos_raamit*2)+2) + '#')
    print('#'*(len(premium_mainos + premium_mainos_raamit*2)+4))
    print(" ")
    print("-"*len(pisin_teksti))
    
def main():
    '''Pääohjelma.'''
    Mainos()
    tiedostolista = luetiedostot()
    tunti_arvot = kasittele_Viikkodata(tiedostolista)
    paivakohtaiset_tulokset = paivalaskut(tunti_arvot)
    paavalikko(tunti_arvot, paivakohtaiset_tulokset)
    # tama on valmis  # tulosta_kaikki(paivakohtaiset_tulokset)
    #rapsa = rapsan_luonti(paivakohtaiset_tulokset)
    #kysy_raportti(rapsa)
    
if __name__ == "__main__":
    main()
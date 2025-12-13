# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee csv-tiedostot ja tulostaa näistä raportin tekstitiedostoon, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
import csv
import glob
from typing import List, Dict
from collections import defaultdict

tunti_lista= []
viikonpaivat = []
tiedostot = []
tiedostolista = []
viikko = []
paivaobjekti_lista = []

viikonpaivat_kaantaja_en_fi = {
    "Monday": "Maanantai",
    "Tuesday": "Tiistai",
    "Wednesday": "Keskiviikko",
    "Thursday": "Torstai",
    "Friday": "Perjantai",
    "Saturday": "Lauantai",
    "Sunday": "Sunnuntai"
}

def luetiedostot() -> list:
    '''Hakee kaikki csv-tiedostot annetusta kansiosta.'''
    print(" ")
    print("Luetaan kansiosta viikko*.csv tiedostot.")

    tiedostolista = sorted(glob.glob("viikko*.csv"))
    print("Kansiossa olevat tiedostot:", tiedostolista)
    return tiedostolista
    



def kasittele_Viikkodata(tiedostolista) -> List[Dict]:
    '''Lukee tiedostot ja muodostaa kaikista listan arvoista sanakirjoina.'''

    tunti_lista = []
    for tiedosto in tiedostolista:
        print(f"Käsitellään tiedostoa:{tiedosto}")

        with open(tiedosto, "r", newline="", encoding="utf-8") as f:
            rivit = f.readlines()[1:]  # Ohitetaan otsikkorivi
            for rivi in rivit:

                rivi= rivi.strip().split(";")
                ajankohta_obj = datetime.strptime(rivi[0], "%Y-%m-%dT%H:%M:%S") # Muutetaan aikaleima objektiksi
                vko_nro = f"vko{ajankohta_obj.isocalendar().week}"
                viikonpaiva = ajankohta_obj.strftime("%A")
                #Luodaan sanakirja jokaiselle ajalle, vaiheelle ja muokataan Wh --> kWh.
                tunti_arvot = {
                    "Viikko": vko_nro,
                    "Päivä": viikonpaiva,
                    "Aika": ajankohta_obj,
                    "Kulutus_vaihe1": float(rivi[1]) / 1000, 
                    "Kulutus_vaihe2": float(rivi[2]) / 1000,
                    "Kulutus_vaihe3": float(rivi[3]) / 1000,
                    "Tuotanto_vaihe1": float(rivi[4]) / 1000,
                    "Tuotanto_vaihe2": float(rivi[5]) / 1000,
                    "Tuotanto_vaihe3": float(rivi[6]) / 1000
                }
                tunti_lista.append(tunti_arvot)
    return tunti_lista

def paivalaskut(tunti_lista: List[Dict], tiedostolista: List[str]) -> List[Dict]:
    '''Antaa päiville päivämäärät, tekee viikkolistan ja summaa tuntien arvot päiville.'''

    #Tehdään yhdelle vuorokaudelle snakirja, josta tehdään sitten lista eri päivämäärille.
    Yksi_paiva= defaultdict(lambda: {
        "Viikko": "",
        "Päivä": "",
        "Aika": "",
        "Kulutus_vaihe1": 0.0,
        "Kulutus_vaihe2": 0.0,
        "Kulutus_vaihe3": 0.0,
        "Tuotanto_vaihe1": 0.0,
        "Tuotanto_vaihe2": 0.0,
        "Tuotanto_vaihe3": 0.0
        })
    
    #Käydään tunnit läpi ja tehdään päivämäärä sanakirja, ja lisätään arvot oikeille päiville.
    for tunti in tunti_lista:
      
        pvm = tunti["Aika"].date()
        vko_nimi = f"vko{tunti['Aika'].isocalendar().week}"

        paivaobj = Yksi_paiva[pvm]
        paivaobj["Viikko"] = vko_nimi
        paivaobj["Päivä"] = viikonpaivat_kaantaja_en_fi[tunti["Aika"].strftime("%A")]
        paivaobj["Aika"] = pvm
        paivaobj["Kulutus_vaihe1"] += tunti["Kulutus_vaihe1"]
        paivaobj["Kulutus_vaihe2"] += tunti["Kulutus_vaihe2"]
        paivaobj["Kulutus_vaihe3"] += tunti["Kulutus_vaihe3"]
        paivaobj["Tuotanto_vaihe1"] += tunti["Tuotanto_vaihe1"]
        paivaobj["Tuotanto_vaihe2"] += tunti["Tuotanto_vaihe2"]
        paivaobj["Tuotanto_vaihe3"] += tunti["Tuotanto_vaihe3"]    
    
    return list(Yksi_paiva.values())

def tulosta_viikot(Paivamaara_data) -> None:
    '''Tulostaa viikonpäivien raportin konsoliin. Erottelee viikot viivalla.'''
    edellinen_viikko = None


    print(" ")
    print("-"*210)
    print("Viikkojen sähkönkulutus ja -tuotanto kWh-yksikössä:")
    print("-"*210)
    print(" ")
    print("-"*210)
    print("Viikko/Päivä".ljust(17),"Päivämäärä".ljust(10), "Kulutus vaihe 1 kWh".rjust(25), "Kulutus vaihe 2 kWh".rjust(25), "Kulutus vaihe 3 kWh".rjust(25), "Tuotanto vaihe 1 kWh".rjust(25), "Tuotanto vaihe 2 kWh".rjust(25), "Tuotanto vaihe 3 kWh".rjust(25))
    print("-"*210)
    # Tulostetaan rivit omiin sarakkeisiin.
    print("-"*210)

    #Jotta saadaan viikot eroteltua, tarkistetaan edellinen viikko ja verrataan sitä nykyiseen.
    for paiva in Paivamaara_data:
            nykyinen_viikko = paiva["Viikko"]
            if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:
                print("-"*210)

            print(f"{paiva['Viikko'].ljust(5)}".removeprefix("vko"),
                f"{paiva['Päivä'].ljust(14)}",
                f"{paiva['Aika'].strftime('%d.%m.%Y')}".ljust(10),
                f"{paiva['Kulutus_vaihe1']:.2f}".replace(".", ",").rjust(25),
                f"{paiva['Kulutus_vaihe2']:.2f}".replace(".", ",").rjust(25),
                f"{paiva['Kulutus_vaihe3']:.2f}".replace(".", ",").rjust(25),
                f"{paiva['Tuotanto_vaihe1']:.2f}".replace(".", ",").rjust(25),
                f"{paiva['Tuotanto_vaihe2']:.2f}".replace(".", ",").rjust(25),
                f"{paiva['Tuotanto_vaihe3']:.2f}".replace(".", ",").rjust(25))
            edellinen_viikko = nykyinen_viikko # Päivitetään edellinen viikko.
    print("-"*210)

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


def kysy_raportti(rapsa: str) -> None:
    while True:
        paatos = input("Haluatko luoda raportin tekstitiedostoon? (k/e): ")

        if paatos.lower() in ["k", "kyllä","y","yes"]:
            print("No mää luon...")
            luo_txt_tiedosto(rapsa)
            break # Poistutaan silmukasta tiedoston luonnin jälkeen.
        elif paatos.lower() in ["e", "ei","n","no"]:
            print("No ei sitten.")
            print("Raporttia ei luotu tiedostoon.")
            break # Poistutaan silmukasta ilman tiedoston luontia.
        else:
            print("Virheellinen syöte. Koita ny edes. Ei rapsaa sulle.")
        #Silmukka jatkuu, kunnes saadaan kelvollinen syöte.

def main():
    '''Pääohjelma.'''
    tiedostolista = luetiedostot()
    tunti_lista = kasittele_Viikkodata(tiedostolista)
    paivakohtaiset_tulokset = paivalaskut(tunti_lista, tiedostolista)
    tulosta_viikot(paivakohtaiset_tulokset)
    rapsa = rapsan_luonti(paivakohtaiset_tulokset)
    kysy_raportti(rapsa)
    


    

if __name__ == "__main__":
    main()
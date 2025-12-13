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
        "Aika": None,
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
        paivaobj["Kulutus_vaihe1"] += tunti["Kulutus_vaihe1"]
        paivaobj["Kulutus_vaihe2"] += tunti["Kulutus_vaihe2"]
        paivaobj["Kulutus_vaihe3"] += tunti["Kulutus_vaihe3"]
        paivaobj["Tuotanto_vaihe1"] += tunti["Tuotanto_vaihe1"]
        paivaobj["Tuotanto_vaihe2"] += tunti["Tuotanto_vaihe2"]
        paivaobj["Tuotanto_vaihe3"] += tunti["Tuotanto_vaihe3"]    
    
    return list(Yksi_paiva.values())

def tulosta_viikko42(Paivamaara_data) -> None:
    '''Tulostaa viikonpäivien raportin konsoliin.'''
 

    print(" ")
    print("-"*190)
    print("Viikon 42 sähkönkulutus ja -tuotanto kWh-yksikössä:")
    print("-"*190)
    print(" ")
    print("-"*190)
    print("Päivä".ljust(15),"Päivämäärä".ljust(15), "Kulutus vaihe 1 kWh".rjust(25), "Kulutus vaihe 2 kWh".rjust(25), "Kulutus vaihe 3 kWh".rjust(25), "Tuotanto vaihe 1 kWh".rjust(25), "Tuotanto vaihe 2 kWh".rjust(25), "Tuotanto vaihe 3 kWh".rjust(25))
    print("-"*190)
    # Tulostetaan rivit omiin sarakkeisiin.
    for vp in viikonpaivat:
        print(vp["Päivä"].ljust(15),
              f"{vp["Aika"].strftime("%d.%m.%Y")}".ljust(15),
              f"{vp['Kulutus_vaihe1']:.2f}".replace(".", ",").rjust(25),
              f"{vp['Kulutus_vaihe2']:.2f}".replace(".", ",").rjust(25),
              f"{vp['Kulutus_vaihe3']:.2f}".replace(".", ",").rjust(25),
              f"{vp['Tuotanto_vaihe1']:.2f}".replace(".", ",").rjust(25),
              f"{vp['Tuotanto_vaihe2']:.2f}".replace(".", ",").rjust(25),
              f"{vp['Tuotanto_vaihe3']:.2f}".replace(".", ",").rjust(25))
    print("-"*190)
    
def main():
    '''Pääohjelma.'''
    tiedostolista = luetiedostot()
    tunti_lista = kasittele_Viikkodata(tiedostolista)
    paivakohtaiset_tulokset = paivalaskut(tunti_lista, tiedostolista)
    print(paivakohtaiset_tulokset)
    #viikonpaivat = paivalaskut(tunti_lista)

    #tulosta_viikko42(viikonpaivat)
    

if __name__ == "__main__":
    main()
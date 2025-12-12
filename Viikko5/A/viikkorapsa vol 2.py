# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee tiedoston "viikko42.csv" ja tulostaa näistä raportin KONSOLIIN, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
import csv
from typing import List, Dict
viikkodata = "viikko42.csv"
tunti_lista= []
viikonpaivat = []


def kasittele_Viikkodata(viikkodata: str) -> list:
    '''Lukee tiedoston ja muodostaa listan arvoista sanakirjoina.'''

    viikkodata = "viikko42.csv"
    tunti_lista = []
    with open(viikkodata, "r", newline="", encoding="utf-8") as f:
        rivit = f.readlines()[1:]  # Ohitetaan otsikkorivi
        for rivi in rivit:

            rivi= rivi.strip().split(";")
            ajankohta_obj = datetime.strptime(rivi[0], "%Y-%m-%dT%H:%M:%S") # Muutetaan aikaleima objektiksi

            #Luodaan sanakirja jokaiselle ajalle, vaiheelle ja muokataan Wh --> kWh.
            tunti_arvot = {
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

def paivalaskut(tunti_lista: List[Dict]) -> List[Dict]:
    '''Antaa päiville päivämäärät, tekee viikkolistan ja summaa tuntien arvot päiville.'''

    # Annetaan päivämäärät viikonpäiville, johon verrataan tunteja.
    paivat = {
    "Maanantai" : datetime(2025, 10, 13),
    "Tiistai" : datetime(2025, 10, 14),
    "Keskiviikko" : datetime(2025, 10, 15),
    "Torstai" : datetime(2025, 10, 16),
    "Perjantai" : datetime(2025, 10, 17),
    "Lauantai" : datetime(2025, 10, 18),
    "Sunnuntai" : datetime(2025, 10, 19)
    }
    #Luodaan lista viikonpäiville, johon kerätään summat.
    viikonpaivat = []
    for paivanimi, pvm in paivat.items():
        viikonpaivat.append({
            "Päivä": paivanimi,
            "Aika": pvm,
            "Kulutus_vaihe1": 0.0,
            "Kulutus_vaihe2": 0.0,
            "Kulutus_vaihe3": 0.0,
            "Tuotanto_vaihe1": 0.0,
            "Tuotanto_vaihe2": 0.0,
            "Tuotanto_vaihe3": 0.0
        })
    #Käydään tunnit läpi ja lisätään arvot oikealle päivälle.
    for tunti in tunti_lista:
        for paivaobj in viikonpaivat:
            if tunti["Aika"].date() == paivaobj["Aika"].date():
                paivaobj["Kulutus_vaihe1"] += tunti["Kulutus_vaihe1"]
                paivaobj["Kulutus_vaihe2"] += tunti["Kulutus_vaihe2"]
                paivaobj["Kulutus_vaihe3"] += tunti["Kulutus_vaihe3"]
                paivaobj["Tuotanto_vaihe1"] += tunti["Tuotanto_vaihe1"]
                paivaobj["Tuotanto_vaihe2"] += tunti["Tuotanto_vaihe2"]
                paivaobj["Tuotanto_vaihe3"] += tunti["Tuotanto_vaihe3"]    
    return viikonpaivat

    
def main():

    tunti_lista = kasittele_Viikkodata(viikkodata)
    viikonpaivat = paivalaskut(tunti_lista)

    print("Viikon 42 sähkönkulutus ja -tuotanto kWh-yksikössä:")
    print("-----------------------------------------------------------")
    print(" ")
    
    for vp in viikonpaivat:
        print(vp)

if __name__ == "__main__":
    main()
    
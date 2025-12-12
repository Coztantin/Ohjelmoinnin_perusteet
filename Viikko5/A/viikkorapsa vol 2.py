# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee tiedoston "viikko42.csv" ja tulostaa näistä raportin KONSOLIIN, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
import csv

def kasittele_Viikkodata(viikkodata: str) -> dict:
# Luetaan tiedosto ja käsitellään rivit
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

def paivalaskut():
    


def main():

    data = kasittele_Viikkodata(viikkodata="viikko42.csv")
    for akio in data:
        print(akio)

if __name__ == "__main__":
    main()
    
# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee tiedoston "viikko42.csv" ja tulostaa näistä raportin KONSOLIIN, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
import csv
from py_compile import main

viikkodata = "viikko42.csv"

def kasittele_Viikkodata(viikkodata: str) -> dict:
    # Luetaan tiedosto ja käsitellään rivit
    tunti_lista = []
    with open(viikkodata, "r", newline="", encoding="utf-8") as f:
        rivit = f.readlines()[1:]  # Ohitetaan otsikkorivi
        for rivi in rivit:
            
            tunti= rivi.strip().split(";")
            ajankohta_obj = datetime.strptime(tunti[0], "%Y-%m-%dT%H:%M:%S") # Muutetaan aikaleima objektiksi
            
            tunti_arvot = {
                "Aika": ajankohta_obj,
                "Kulutus_vaihe1": float(tunti[1]),
                "Kulutus_vaihe2": float(tunti[2]),
                "Kulutus_vaihe3": float(tunti[3]),
                "Tuotanto_vaihe1": float(tunti[4]),
                "Tuotanto_vaihe2": float(tunti[5]),
                "Tuotanto_vaihe3": float(tunti[6])
            }
            tunti_lista.append(tunti_arvot)
            
    return tunti_lista



if __name__ == "__main__" :
    tulos = kasittele_Viikkodata(viikkodata)
    print(*tulos[:5], sep="\n")  # Tulostetaan ensimmäiset 5 riviä tarkistukseen

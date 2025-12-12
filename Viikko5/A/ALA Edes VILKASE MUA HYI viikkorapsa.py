# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee tiedoston "viikko42.csv" ja tulostaa näistä raportin KONSOLIIN, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
import csv


viikkodata = "viikko42.csv"
tunti_lista= []
def kasittele_Viikkodata(viikkodata: str) -> dict:
    # Luetaan tiedosto ja käsitellään rivit
    tunti_lista = []
    with open(viikkodata, "r", newline="", encoding="utf-8") as f:
        rivit = f.readlines()[1:]  # Ohitetaan otsikkorivi
        for rivi in rivit:
            
            tunti= rivi.strip().split(";")
            ajankohta_obj = datetime.strptime(tunti[0], "%Y-%m-%dT%H:%M:%S") # Muutetaan aikaleima objektiksi
            
            #Luodaan sanakirja jokaiselle ajalle ja vaiheelle.
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

def paivalaskut(tunti_lista: list) -> dict:
    # Jaetaan luetut tunnit viikonpäivittäin ja palautetaan sanakirjana
    Viikko_lista = {
        "Maanantai": [],
        "Tiistai": [],
        "Keskiviikko": [],
        "Torstai": [],
        "Perjantai": [],
        "Lauantai": [],
        "Sunnuntai": []
    }
    Maanantai_pvm = datetime(2025, 10, 13)
    Tiistai_pvm = datetime(2025, 10, 14)
    Keskiviikko_pvm = datetime(2025, 10, 15)
    Torstai_pvm = datetime(2025, 10, 16)
    Perjantai_pvm = datetime(2025, 10, 17)
    Lauantai_pvm = datetime(2025, 10, 18)
    Sunnuntai_pvm = datetime(2025, 10, 19)

    for tunti in tunti_lista:
        paiva = tunti["Aika"].date()
        if paiva == Maanantai_pvm.date():
            Viikko_lista["Maanantai"].append(tunti)
            #print ("Lisätty Maanantai:", tunti)
        if paiva == Tiistai_pvm.date():
            Viikko_lista["Tiistai"].append(tunti)
            #print ("Lisätty Tiistai:", tunti)
        if paiva == Keskiviikko_pvm.date():
            Viikko_lista["Keskiviikko"].append(tunti)
            #print ("Lisätty Keskiviikko:", tunti)
        if paiva == Torstai_pvm.date():
            Viikko_lista["Torstai"].append(tunti)
            #print ("Lisätty Torstai:", tunti)
        if paiva == Perjantai_pvm.date():
            Viikko_lista["Perjantai"].append(tunti)
            #print ("Lisätty Perjantai:", tunti)
        if paiva == Lauantai_pvm.date():
            Viikko_lista["Lauantai"].append(tunti)
            #print ("Lisätty Lauantai:", tunti)
        if paiva == Sunnuntai_pvm.date():
            Viikko_lista["Sunnuntai"].append(tunti)
            #print ("Lisätty Sunnuntai:", tunti)
    return Viikko_lista

def paivien_summaus(Viikko_lista: dict) -> dict:
    #Lasketaan jokaisen Päivän kulutus ja tuotanto erikseen vaiheittain
    # ja palautetaan sanakirjana):
    paivat =["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    Viikko_lista_summa = {
            
            "Kulutus_vaihe1": 0.0,
            "Kulutus_vaihe2": 0.0,
            "Kulutus_vaihe3": 0.0,
            "Tuotanto_vaihe1": 0.0,
            "Tuotanto_vaihe2": 0.0,
            "Tuotanto_vaihe3": 0.0
        } 
    




if __name__ == "__main__" :
    kasitelty_data = kasittele_Viikkodata(viikkodata)
    viikonpaivat = paivalaskut(kasitelty_data)
    lasketut_paivat = paivien_summaus(viikonpaivat)
    print(lasketut_paivat)
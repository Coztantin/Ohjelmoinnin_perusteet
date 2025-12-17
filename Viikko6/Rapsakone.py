# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee csv-tiedostot ja tulostaa näistä raportin tekstitiedostoon, jossa lasketaan jokaiselle päivälle
    - sähkönkulutuksen nettona kWh-yksikössä
    - sähköntuotannon nettona kWh-yksikössä
    - päivän keskimääräinen lämpötila celsiusasteina
'''
from datetime import timedelta, datetime, date, timezone
import msvcrt
import time
import csv
import glob

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

#Määritetään sarakkeiden leveydet ja viivojen pituus
Raportti_pohjan_muotoilut = {
    "Vuosi_W" : 7,
    "Kuukausi_W" : 10,
    "Viikko_W" : 10,
    "Päivämäärä_W" : 15,
    "Päivä_W" : 15,
    "Klo_W" : 6,
    "Kulutus_W" : 30,
    "Tuotanto_W" : 30,
    "Lämpötila_W" : 33,
}
Raportti_pohjan_muotoilut["viivanpituus"] = sum(Raportti_pohjan_muotoilut.values())
Raportti_pohjan_muotoilut["viivat"] = "-" * Raportti_pohjan_muotoilut["viivanpituus"] # type: ignore



tiedostolista = []
kaikki_tunnit = []
def luetiedostot() -> list:
    '''Hakee kaikki csv-tiedostot annetusta kansiosta.'''
    print(" ")
    print("Luetaan kansiosta *.csv tiedostot.")

    tiedostolista = sorted(glob.glob("*.csv"))
    print("Kansiossa olevat tiedostot:", tiedostolista)
    return tiedostolista

def kasittele_tiedostot(tiedostolista):
    '''Lukee tiedostot ja muodostaa kaikista listan arvoista sanakirjoina. Koska kyseessä on suhteellisen pieni tiedostokoko (alle 500KB), vaikka siihen lisättäisiin viimeinen
    kuukausi dataa, voidaan kaikki tiedot lukea kerralla muistiin. Tekoälyn mukaan, jos tiedostokoko olisi yli 10-50MB TAI yli 100 000 riviä, tulisi harkita eri lähestymistapaa.
    Turha lähtee pilkkomaan.'''
    
    for tiedosto in tiedostolista:
        print(f"Käsitellään tiedostoa:{tiedosto}")

        with open(tiedosto, "r", newline="", encoding="utf-8") as f:
            next(f)  # Ohitetaan otsikkorivi
            for rivi in f:
                rivi = rivi.strip().split(";")
                kaikki_tunnit.append(tieto_muuntaja(rivi))
    return kaikki_tunnit

def tieto_muuntaja(rivi):
    ''' Muuntaa tiedoston rivin oikeaan muotoon, jotta voidaan käyttää niitä laskuissa.'''
    return [
        datetime.fromisoformat(rivi[0]),                    # Aikaleima datetime objektina tekee sisällä v, kk, pp, tt, mm, ss, ms ja aikavyöhykkeen
        float(rivi[1].replace(",", ".")),                   # Sähkönkulutus kWh
        float(rivi[2].replace(",", ".")),                   # Sähköntuotanto kWh
        float(rivi[3].replace(",", "."))                    # Lämpötila Celsius
    ]
    
def Valikko():
    '''Näyttää valikon ja palauttaa käyttäjän valinnan.'''
    
    # Ensimmäinen valikko
    while True:
        print("Tervetuloa Rapsakone-ohjelmaan!\n" 
        
              "-----------------------------------------------------------------------------------\n"
              "Valitse haluamasi toiminto:\n"
              "1 - Päiväkohtainen yhteenveto aikaväliltä\n"
              "2 - Kuukausikohtainen yhteenveto Yhdelle kuukaudelle\n"
              "3 - Vuoden kokonaisyhteenveto\n"
              "0 - Lopeta ohjelma"
              )
        eka_valinta = int(input("Anna valintasi (0-3): "))
        time.sleep(1)
        if eka_valinta not in [0, 1, 2, 3]:
            time.sleep(1)
            print("Jumalauta! Kissa siellä näppiksellä! Ota kissa syliin ja yritä uudestaan.")
            print("")
            continue
        if eka_valinta == 0:
            time.sleep(1)
            print("Jahas... Misklikki taas... ei se mitään.. oon tottunut tähä...Heippulis Hei!")
            print("")
            exit()
        elif eka_valinta == 1:
            time.sleep(1)
            print("")
            print("Valitsit päiväkohtaisen yhteenvedon aikaväliltä.\n"
                  "Tarvitaan alkupäivämäärä ja loppupäivämäärä muodossa pp.kk.vvvv.")
            alkupvm, loppupvm = valikko_aikavali()
            print(f"Valitsit aikavälin {alkupvm} - {loppupvm}. Käsitellään tiedot...")
            # Kutsu funktiota, joka käsittelee päiväkohtaisen yhteenvedon
        elif eka_valinta == 2:
            time.sleep(1)
            print("")
            print("Valitsit kuukausikohtaisen yhteenvedon yhdelle kuukaudelle.\n"
                  "Tarvitaan kuukauden numero väliltä 1-12:")
            kuukausi = valikko_kuukausi()
            print(f"Valitsit kuukauden: {kuukausi}. Käsitellään tiedot...")
            print("")
            # Kutsu funktiota, joka käsittelee kuukausikohtaisen yhteenvedon
        elif eka_valinta == 3:
            time.sleep(1)
            print("")
            print("Valitsit vuoden kokonaisyhteenvedon.\n"
                  "Tarvitaan vuosi muodossa vvvv esim. 2025: ")
            vuosi = valikko_vuosi()            
            print(f"Valitsit vuoden: {vuosi}. Käsitellään tiedot...")
            print("")
                # Kutsu funktiota, joka käsittelee vuoden kokonaisyhteenvedon
        
        else:
            print("-------------------------------------------------------------------")
            continue

# Toinen valikko
        while True:
            time.sleep(1)

            print("-------------------------------------------------------------------------------------\n"
                  "Mitä haluat tehdä seuraavaksi?\n")
            print("1 - Kirjoita raportti tiedostoon\n"
                  "2 - Luo uusi raportti\n"
                  "3 - Lopeta ohjelma"
                 )
            time.sleep(1)
            toka_valinta = int(input("Anna valintasi (0-3): "))
            if toka_valinta not in [0, 1, 2, 3]:
                time.sleep(1)
                print("Jumalauta! Kissa siellä näppiksellä! Ota kissa syliin ja yritä uudestaan.")
                print("")
                continue

            elif toka_valinta == 0:
                time.sleep(1)
                print("Päivän työ on tehty, ohjelma sulkeutuu. Pailaillaan!")
                print("")
                exit()
            elif toka_valinta == 1:
                time.sleep(1)
                print("")
                print("Valitsit Kirjoita raportti tiedostoon.\n"
                      "Aloitetaan raportin kirjoitus...")
                time.sleep(1)

                # Kutsu funktiota, joka kirjoittaa raportin tiedostoon
                print("Raportti kirjoitettu tiedostoon onnistuneesti!\n"
                      " ")    
            elif toka_valinta == 2:
                time.sleep(1)
                print("")
                print("Valitsit uuden raportin.\n"
                      "Palataan valikkoon...")

                return Valikko()
            
            
            elif toka_valinta == 3:
                time.sleep(1)
                print("")
                print("Valitsit lopettaa ohjelman.\n"
                      "Päivän työ on tehty, ohjelma sulkeutuu. Pailaillaan!")
                exit()

            else:
                print("-------------------------------------------------------------------")
            continue

def valikko_vuosi() -> int:
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

def valikko_kuukausi() -> int:
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

def valikko_aikavali() -> tuple[date, date]:
    '''Päävalikon alivalikko aikavälin valintaan.'''
    while True:
        alku_input = input("Anna aikavälin alku päivämäärä muodossa pp.kk.vvvv (esim. 01.01.2023): ")
        loppu_input = input("Anna aikavälin loppu päivämäärä muodossa pp.kk.vvvv (esim. 31.12.2023): ")
        try:
            alku = datetime.strptime(alku_input, "%d.%m.%Y").date()
            loppu = datetime.strptime(loppu_input, "%d.%m.%Y").date()
            if alku <= loppu:
                return (alku, loppu)
            else:
                print("Aikavälin alku ei voi olla myöhemmin kuin loppu. Yritä uudelleen.")
        except ValueError:
            print("Virheellinen päivämäärä. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def raportin_Sisalto() -> str:
    '''Luo raportin sisällön.'''
    
    raportti_sisalto = ""
    raportti_sisalto += "Elama on roskaa"#tähän kohtaan funktio, joka laskee ja lisää raportin sisällön
  
    return raportti_sisalto

def raportin_Pohja() -> str:
    '''Luo raportin pohjan.'''
    #Tätä muokataan jos ehditään lisäämään modulaarisuutta

    raportti_pohja = "Rapsakone Raportti - Yhteenveto\n"                                                                                    #Tätä voisimuokata lisäämällä mitä tulostetaan
    raportti_pohja += f"{Raportti_pohjan_muotoilut['viivat']}\n"
    raportti_pohja += "Tässä raportissa esitetään sähkönkulutuksen, sähköntuotannon ja lämpötilan yhteenveto valitulta ajanjaksolta.\n\n"   #Tätäkin voisi muokata modulaarisuutta
    raportti_pohja += f"{Raportti_pohjan_muotoilut['viivat']}\n"
    raportti_pohja += f"{'Vuosi':<{Raportti_pohjan_muotoilut['Vuosi_W']}} {'Kuukausi':<{Raportti_pohjan_muotoilut['Kuukausi_W']}} {'Viikko':<{Raportti_pohjan_muotoilut['Viikko_W']}} {'Päivämäärä':<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} {'Päivä':<{Raportti_pohjan_muotoilut['Päivä_W']}} {'Klo':<{Raportti_pohjan_muotoilut['Klo_W']}} {'Kulutus (kWh)':>{Raportti_pohjan_muotoilut['Kulutus_W']}} {'Tuotanto (kWh)':>{Raportti_pohjan_muotoilut['Tuotanto_W']}} {'Lämpötila (°C)':>{Raportti_pohjan_muotoilut['Lämpötila_W']}}\n" 
    raportti_pohja += f"{Raportti_pohjan_muotoilut['viivat']}\n"

    # Lisää tähän raportin sisältöä laskettujen tietojen perusteella
    return raportti_pohja

def raportti(raportin_sisalto: str,raportin_pohja: str) -> str:
    '''Luo koko raportin.'''
    raportti = ""
    raportti += raportin_pohja
    raportti += raportin_sisalto

    return raportti

def raportti_tiedostoon(raportti: str):
    '''Kirjoittaa raportin tiedostoon.'''
    with open("Raporttipinkka\\raportti.txt", "w", encoding="utf-8") as f:
        f.write(raportti)


def main():
    '''Pääohjelma. Kysyy Käyttäjältä valikon avulla halutun toiminnon ja suorittaa sen. Tulosten tarkistelu ja tallennus tiedostoon.'''

    tiedostolista =luetiedostot()
    kasittele_tiedostot(tiedostolista)
    Rapsa = raportti(raportin_Sisalto(), raportin_Pohja())
    raportti_tiedostoon(Rapsa)
    print("Raportti on luotu tiedostoon 'Raporttipinkka\\raportti.txt' onnistuneesti.")

    #raportti_tiedostoon(raportti)
    #print("Raportti on luotu tiedostoon 'Raporttipinkka\\raportti.txt' onnistuneesti.")
    #valinta = Valikko()

if __name__ == "__main__":
    main()
# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee csv-tiedostot ja tulostaa näistä raportin tekstitiedostoon, jossa lasketaan jokaiselle päivälle
    - sähkönkulutuksen nettona kWh-yksikössä
    - sähköntuotannon nettona kWh-yksikössä
    - päivän keskimääräinen lämpötila celsiusasteina
'''
from collections import defaultdict
from datetime import timedelta, datetime, date, timezone
import msvcrt
import sys
import time
import csv
import glob

# Määritellään käännökset viikonpäiville ja kuukausille
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
    "Kulutus_W" : 20,
    "Tuotanto_W" : 20,
    "Lämpötila_W" : 23,
    "korjausmäärä" : 8
}
Raportti_pohjan_muotoilut["viivanpituus"] = sum(Raportti_pohjan_muotoilut.values())
Raportti_pohjan_muotoilut["viivat"] = "-" * Raportti_pohjan_muotoilut["viivanpituus"] # type: ignore

# Globaalit muuttujat
tiedostolista = []
kaikki_tunnit = []
def luetiedostot() -> list:
    '''Hakee kaikki csv-tiedostot annetusta kansiosta.'''
    print(" ")
    print("Luetaan kansiosta *.csv tiedostot.")
    lataus_animointi()

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

def aikavali_rapsis(alkupvm: date, loppupvm: date,kaikki_tunnit: list): 
    '''Ottaa annetun aikavälin, hakee tiedot ja tekee niistä tulostettavan tai tallennettavan listan merkkejä.'''
    sisalto = ""
    yhteenveto = ""
    kulutus_summa = 0.0
    tuotanto_summa = 0.0
    lampotila_summa = 0.0
    lampotila_klt = 0.0
    lampotila_lkm = 0
    
    for rivi in kaikki_tunnit:
        if alkupvm <= rivi[0].date() <= loppupvm:
            sisalto +=( 
                f"{rivi[0].year:<{Raportti_pohjan_muotoilut['Vuosi_W']}} " 
                f"{kuukaudet_kaantaja_en_fi[rivi[0].strftime('%B')]:<{Raportti_pohjan_muotoilut['Kuukausi_W']}} "
                f"{rivi[0].isocalendar()[1]:<{Raportti_pohjan_muotoilut['Viikko_W']}} "
                f"{rivi[0].date().strftime('%d.%m.%Y'):<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} "
                f"{viikonpaivat_kaantaja_en_fi[rivi[0].strftime('%A')]:<{Raportti_pohjan_muotoilut['Päivä_W']}} "
                f"{rivi[0].strftime('%H:%M'):<{Raportti_pohjan_muotoilut['Klo_W']}} ")+(
                (f"{rivi[1]:>{Raportti_pohjan_muotoilut['Kulutus_W']}.2f} ").replace(".", ",") +
                (f"{rivi[2]:>{Raportti_pohjan_muotoilut['Tuotanto_W']}.2f} ").replace(".", ",") + 
                (f"{rivi[3]:>{Raportti_pohjan_muotoilut['Lämpötila_W']}.2f}\n").replace(".", ",")
            )
            kulutus_summa += rivi[1]
            tuotanto_summa += rivi[2]
            lampotila_summa += rivi[3]
            lampotila_lkm += 1
            lampotila_klt = lampotila_summa / lampotila_lkm  #Otetaan huomioon myös viimeinen päivä
    yhteenveto += (
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
        f"Valitulta aikaväliltä {alkupvm.strftime('%d.%m.%Y')} - {loppupvm.strftime('%d.%m.%Y')} yhteenveto:\n"
        f"\n")
    yhteenveto += (
        f"Sähkönkulutus yhteensä: {kulutus_summa:.2f} kWh\n".replace(".", ",") +
        f"Sähköntuotanto yhteensä: {tuotanto_summa:.2f} kWh\n".replace(".", ",") +
        f"Keskimääräinen lämpötila: {lampotila_klt:.2f} °C\n".replace(".", ",") +
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
    )
    
    return sisalto, yhteenveto

def kk_rapsis(kuukausi: int, vuosi: int, kaikki_tunnit: list):

    sisalto = ""
    yhteenveto = ""
    kulutus_summa = 0.0
    tuotanto_summa = 0.0
    lampotila_summa = 0.0
    lampotila_klt = 0.0
    lampotila_lkm = 0
    
    for rivi in kaikki_tunnit:
        if rivi[0].year == vuosi and rivi[0].month == kuukausi:
            sisalto +=( 
                f"{rivi[0].year:<{Raportti_pohjan_muotoilut['Vuosi_W']}} " 
                f"{kuukaudet_kaantaja_en_fi[rivi[0].strftime('%B')]:<{Raportti_pohjan_muotoilut['Kuukausi_W']}} "
                f"{rivi[0].isocalendar()[1]:<{Raportti_pohjan_muotoilut['Viikko_W']}} "
                f"{rivi[0].date().strftime('%d.%m.%Y'):<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} "
                f"{viikonpaivat_kaantaja_en_fi[rivi[0].strftime('%A')]:<{Raportti_pohjan_muotoilut['Päivä_W']}} "
                f"{rivi[0].strftime('%H:%M'):<{Raportti_pohjan_muotoilut['Klo_W']}} ")+(
                (f"{rivi[1]:>{Raportti_pohjan_muotoilut['Kulutus_W']}.2f} ").replace(".", ",") +
                (f"{rivi[2]:>{Raportti_pohjan_muotoilut['Tuotanto_W']}.2f} ").replace(".", ",") + 
                (f"{rivi[3]:>{Raportti_pohjan_muotoilut['Lämpötila_W']}.2f}\n").replace(".", ",")
            )
            kulutus_summa += rivi[1]
            tuotanto_summa += rivi[2]
            lampotila_summa += rivi[3]
            lampotila_lkm += 1
            lampotila_klt = lampotila_summa / lampotila_lkm  #Otetaan huomioon myös viimeinen päivä
    yhteenveto += (
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
        f"Kuluvan vuoden ({vuosi}) valitun kuukauden {kuukausi} - {kuukaudet_kaantaja_en_fi[datetime(vuosi, kuukausi, 1).strftime('%B')]} yhteenveto:\n"
        f"\n")
    yhteenveto += (
        f"Sähkönkulutus yhteensä: {kulutus_summa:.2f} kWh\n".replace(".", ",") +
        f"Sähköntuotanto yhteensä: {tuotanto_summa:.2f} kWh\n".replace(".", ",") +
        f"Keskimääräinen lämpötila: {lampotila_klt:.2f} °C\n".replace(".", ",") +
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
    )
    
    return sisalto, yhteenveto

def vuosi_rapsis(vuosi: int, kaikki_tunnit: list):
    sisalto = ""
    yhteenveto = ""
    kulutus_summa = 0.0
    tuotanto_summa = 0.0
    lampotila_summa = 0.0
    lampotila_klt = 0.0
    lampotila_lkm = 0
    
    for rivi in kaikki_tunnit:
        if rivi[0].year == vuosi:
            sisalto +=( 
                f"{rivi[0].year:<{Raportti_pohjan_muotoilut['Vuosi_W']}} " 
                f"{kuukaudet_kaantaja_en_fi[rivi[0].strftime('%B')]:<{Raportti_pohjan_muotoilut['Kuukausi_W']}} "
                f"{rivi[0].isocalendar()[1]:<{Raportti_pohjan_muotoilut['Viikko_W']}} "
                f"{rivi[0].date().strftime('%d.%m.%Y'):<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} "
                f"{viikonpaivat_kaantaja_en_fi[rivi[0].strftime('%A')]:<{Raportti_pohjan_muotoilut['Päivä_W']}} "
                f"{rivi[0].strftime('%H:%M'):<{Raportti_pohjan_muotoilut['Klo_W']}} ")+(
                (f"{rivi[1]:>{Raportti_pohjan_muotoilut['Kulutus_W']}.2f} ").replace(".", ",") +
                (f"{rivi[2]:>{Raportti_pohjan_muotoilut['Tuotanto_W']}.2f} ").replace(".", ",") + 
                (f"{rivi[3]:>{Raportti_pohjan_muotoilut['Lämpötila_W']}.2f}\n").replace(".", ",")
            )
            kulutus_summa += rivi[1]
            tuotanto_summa += rivi[2]
            lampotila_summa += rivi[3]
            lampotila_lkm += 1
            lampotila_klt = lampotila_summa / lampotila_lkm  #Otetaan huomioon myös viimeinen päivä
    yhteenveto += (
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
        f"Valitun vuoden ({vuosi}) yhteenveto:\n"
        f"\n")
    yhteenveto += (
        f"Sähkönkulutus yhteensä: {kulutus_summa:.2f} kWh\n".replace(".", ",") +
        f"Sähköntuotanto yhteensä: {tuotanto_summa:.2f} kWh\n".replace(".", ",") +
        f"Keskimääräinen lämpötila: {lampotila_klt:.2f} °C\n".replace(".", ",") +
        f"{Raportti_pohjan_muotoilut['viivat']}\n"
    )
    
    return sisalto, yhteenveto

def Valikko():
    '''Näyttää valikon ja palauttaa käyttäjän valinnan.'''

    sisalto = None
    yhteenveto = None
    
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
            time.sleep(0.5)
            print("")
            print("Valitsit päiväkohtaisen yhteenvedon aikaväliltä.\n"
                  "Tarvitaan alkupäivämäärä ja loppupäivämäärä muodossa p.k.vvvv.")
            time.sleep(1)
            print(" ")
            alkupvm, loppupvm = valikko_aikavali()
            print(f"Valitsit aikavälin {alkupvm.strftime('%d.%m.%Y')} - {loppupvm.strftime('%d.%m.%Y')}. Käsitellään tiedot...")
            print("")
            lataus_animointi()
            sisalto, yhteenveto = aikavali_rapsis(alkupvm, loppupvm, kaikki_tunnit)
            time.sleep(1)
            print("")
            print("Yhteenveto aikaväliltä:")
            print(yhteenveto)
            print("")
            time.sleep(3)
            print(sisalto)
            print("")
            time.sleep(1)

            # Kutsu funktiota, joka käsittelee päiväkohtaisen yhteenvedon
        elif eka_valinta == 2:
            time.sleep(1)
            print("")
            print("Valitsit kuukausikohtaisen yhteenvedon yhdelle kuukaudelle.\n"
                  "Tarvitaan kuukauden numero väliltä 1-12:")
            kuukausi, vuosi = valikko_kuukausi()
            kk_teksti = kuukaudet_kaantaja_en_fi[datetime(vuosi, kuukausi, 1).strftime('%B')]
            print("")
            print(f"Valitsit kuukauden: {kuukausi}, {kk_teksti}. Käsitellään vuotta {vuosi}. Käsitellään tiedot...")
            print("")
            sisalto, yhteenveto = kk_rapsis(kuukausi, vuosi, kaikki_tunnit)
            time.sleep(1)
            print("")
            print("Yhteenveto aikaväliltä:")
            print(yhteenveto)
            print("")
            print(sisalto)
            print("")
            time.sleep(1)

        elif eka_valinta == 3:
            time.sleep(1)
            print("")
            print("Valitsit vuoden kokonaisyhteenvedon.\n"
                  "Tarvitaan vuosi muodossa vvvv esim. 2025: ")
            vuosi = valikko_vuosi()            
            print(f"Valitsit vuoden: {vuosi}. Käsitellään tiedot...")
            print("")
            sisalto, yhteenveto = vuosi_rapsis(vuosi, kaikki_tunnit)
            time.sleep(1)
            print("")
            print("Yhteenveto vuodelta:")
            print(yhteenveto)
            print("")
            print(sisalto)
            print("")
            time.sleep(1)
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
                print("Päivän työ on tehty, ohjelma sulkeutuu. Pailaillaan!")
                print("")
                exit()

            elif toka_valinta == 1:
                time.sleep(1)
                print("")
                print("Valitsit Kirjoita raportti tiedostoon.\n"
                      "Aloitetaan raportin kirjoitus...")
                time.sleep(1)
                if sisalto == None or yhteenveto == None:
                    print("Ei ole luotu raporttia, palataan valikkoon...")
                    return Valikko()
                
                 # Kutsu funktiota, joka luo raportin sisällön ja pohjan
                Rapsa = raportti(
                    raportin_Sisalto(sisalto), raportin_Pohja(yhteenveto))
                raportti_tiedostoon(Rapsa)

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

def valikko_kuukausi():
    '''Päävalikon alivalikko kuukauden valintaan.'''
    while True:

        kuukausi_input = input("Anna haluamasi kuukausi muodossa kk (esim. 01): ")
        try:
            vuosi = datetime.now().year
            kuukausi = int(kuukausi_input)
            if 1 <= kuukausi <= 12 and vuosi == datetime.now().year:
                return kuukausi, vuosi
            else:
                print("Anna Nyt jotain järkevää, jotain kuukauden numero välillä 1-12!")
        except ValueError:
            print("Virheellinen syöte. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def valikko_aikavali() -> tuple[date, date]:
    '''Päävalikon alivalikko aikavälin valintaan.'''
    while True:
        alku_input = input("Anna aikavälin alku päivämäärä muodossa p.k.vvvv (esim. 1.1.2023): ")
        loppu_input = input("Anna aikavälin loppu päivämäärä muodossa p.k.vvvv (esim. 31.12.2023): ")
        try:
            alku = datetime.strptime(alku_input, "%d.%m.%Y").date()
            loppu = datetime.strptime(loppu_input, "%d.%m.%Y").date()
            if alku <= loppu:
                return (alku, loppu)
            else:
                print("Aikavälin alku ei voi olla myöhemmin kuin loppu. Yritä uudelleen.")
        except ValueError:
            print("Virheellinen päivämäärä. Ota kissa pois näppäimistöltä, siirrä se syliin ja yritä uudelleen.")

def raportin_Sisalto(sisalto) -> str:
    '''Luo raportin sisällön.'''
    
    raportti_sisalto = ""
    raportti_sisalto += sisalto
    return raportti_sisalto

def raportin_Pohja(yhteenveto) -> str:
    '''Luo raportin pohjan.'''
    #Tätä muokataan jos ehditään lisäämään modulaarisuutta
    

    raportti_pohja = "Rapsakone Raportti - Yhteenveto\n"               
    raportti_pohja += f"{Raportti_pohjan_muotoilut['viivat']}\n"
    raportti_pohja += yhteenveto
    raportti_pohja += "\n"
    raportti_pohja += "Alla eritetty vielä päiväkohtaiset tiedot:\n"
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

def lataus_animointi(pituus=30, viive=0.1, teksti="Käsitellään..."):
    '''Näyttää lataus animaation konsolissa.'''
    print(teksti)
    for i in range(pituus+1):
        palkki = "|" + "." * i + " " * (pituus - i) + "|"
        sys.stdout.write("\r" + " " * (pituus + 2))  # tyhjennä rivi
        sys.stdout.write("\r" + palkki)
        sys.stdout.flush()
        time.sleep(viive)
    print("\n")

def Mainos() -> None:
    '''Mainokset pääsi mystisesti tähän ohjelmaan.'''

    premium_mainos = str("PREMIUM-JÄSENYYS: VAIN 9,99 €kk!")
    premium_mainos_raamit = str("#")
    pisin_teksti = str( "No ei hätää, me autamme sinua tässä asiassa! Nyt voit saada selville sähkönkulutuksesi ja -tuotantosi päivä-, viikko-, ja kuukausitasolla helposti ja nopeasti!")
    print(" ")
    print("-"*len(pisin_teksti))
    print("Tervetuloa AurinkoSähköPaneeliRapsaGeneraattori Palveluun!")
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
    '''Pääohjelma. Kysyy Käyttäjältä valikon avulla halutun toiminnon ja suorittaa sen. Tulosten tarkistelu ja tallennus tiedostoon.'''

    tiedostolista =luetiedostot()
    kasittele_tiedostot(tiedostolista)
    Mainos()
    Valikko()
    
    #print(aikavalilta_suodatus(alkupvm, loppupvm, kaikki_tunnit)[1:10],"\n") #Tulostaa esimerkinomaisesti 10 riviä suodatetuista tiedoista
    #Rapsa = raportti(raportin_Sisalto(), raportin_Pohja())
    #raportti_tiedostoon(Rapsa)
    #print("Raportti on luotu tiedostoon 'Raporttipinkka\\raportti.txt' onnistuneesti.")

    #raportti_tiedostoon(raportti)
    #print("Raportti on luotu tiedostoon 'Raporttipinkka\\raportti.txt' onnistuneesti.")
    #valinta = Valikko()

if __name__ == "__main__":
    main()

#TÄMÄ TEKEE TUNTEJA

# def aikavalilta_suodatus(alkupvm: date, loppupvm: date,kaikki_tunnit: list):
#     '''Suodattaa tiedot aikaväliltä.'''
#     edellinen_viikko = None
#     nykyinen_paiva = None
#     suodatetut_tiedot = []
    
#     paiva_kulutus = 0.0
#     paiva_tuotanto = 0.0
#     paiva_lampotila = None


#     for rivi in kaikki_tunnit:
#         pvm = rivi[0].date()
#         if alkupvm <= rivi[0].date() <= loppupvm:
#             nykyinen_viikko = rivi[0].isocalendar()[1] #määrää nykyisen viikon numeron vuodelle
            
#             if nykyinen_paiva is not None and pvm != nykyinen_paiva:

            
#                 if edellinen_viikko is not None and nykyinen_viikko != edellinen_viikko:

#                     print(Raportti_pohjan_muotoilut["viivat"])

        
#                 print(
#                     f"{rivi[0].year:<{Raportti_pohjan_muotoilut['Vuosi_W']}} " +
#                     f"{kuukaudet_kaantaja_en_fi[rivi[0].strftime('%B')]:<{Raportti_pohjan_muotoilut['Kuukausi_W']}} " +
#                     f"{rivi[0].isocalendar()[1]:<{Raportti_pohjan_muotoilut['Viikko_W']}} " +
#                     f"{rivi[0].date().strftime('%d.%m.%Y'):<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} " +
#                     f"{viikonpaivat_kaantaja_en_fi[rivi[0].strftime('%A')]:<{Raportti_pohjan_muotoilut['Päivä_W']}} " +
#                     f"{rivi[0].strftime('%H:%M'):>{Raportti_pohjan_muotoilut['Klo_W']}} " +
#                     (f"{rivi[1]:>{Raportti_pohjan_muotoilut['Kulutus_W']}.2f} ").replace(".", ",") +
#                     (f"{rivi[2]:>{Raportti_pohjan_muotoilut['Tuotanto_W']}.2f} ").replace(".", ",") +
#                     (f"{rivi[3]:>{Raportti_pohjan_muotoilut['Lämpötila_W']}.2f}").replace(".", ",")
#                 )

#                 # Päivän tietojen nollaus
#                 paiva_kulutus = 0.0
#                 paiva_tuotanto = 0.0

#             # Päivän tietojen kerääminen
#             paiva_kulutus += rivi[1]
#             paiva_tuotanto += rivi[2]

#             nykyinen_paiva = pvm #Päivitetään nykyinen päivä
#             edellinen_viikko = nykyinen_viikko #Päivitetään edellinen viikko
        
#         if nykyinen_paiva is not None:
#             print(Raportti_pohjan_muotoilut["viivat"])
#             print(
#                 f"{nykyinen_paiva.year:<{Raportti_pohjan_muotoilut['Vuosi_W']}} " +
#                 f"{kuukaudet_kaantaja_en_fi[nykyinen_paiva.strftime('%B')]:<{Raportti_pohjan_muotoilut['Kuukausi_W']}} " +
#                 f"{edellinen_viikko:<{Raportti_pohjan_muotoilut['Viikko_W']}} " +
#                 f"{nykyinen_paiva.strftime('%d.%m.%Y'):<{Raportti_pohjan_muotoilut['Päivämäärä_W']}} " +
#                 f"{viikonpaivat_kaantaja_en_fi[nykyinen_paiva.strftime('%A')]:<{Raportti_pohjan_muotoilut['Päivä_W']}} " +
#                 f"{'':>{Raportti_pohjan_muotoilut['Klo_W']}} " +
#                 (f"{paiva_kulutus:>{Raportti_pohjan_muotoilut['Kulutus_W']}.2f} ").replace(".", ",") +
#                 (f"{paiva_tuotanto:>{Raportti_pohjan_muotoilut['Tuotanto_W']}.2f} ").replace(".", ",")
#             )
    
#     return suodatetut_tiedot    
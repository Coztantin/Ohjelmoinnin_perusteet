# Copyright (c) 2025 Kosti Korkiakoski
# Licence: MIT

'''
Tehtävänä laatia ohjelma, joka lukee csv-tiedostot ja tulostaa näistä raportin tekstitiedostoon, jossa lasketaan jokaiselle päivälle
    - vaiheittaisen sähkönkulutuksen (1-3 vaihe) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (1-3 vaihe) kWh-yksikössä
'''
from datetime import datetime
from datetime import timezone
import csv
import glob
from typing import List, Dict
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
                    "Vuorokauden keskilämpötila": str(rivi[3]) + " °C"
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

def Mainos(Mainos:str) -> None:
    '''Mainokset pääsi mystisesti tähän ohjelmaan.'''

    premium_mainos = str("PREMIUM-JÄSENYYS: VAIN 9,99 €kk!")
    premium_mainos_raamit = str("#")
    pisin_teksti = str( "No ei hätää, me autamme sinua tässä asiassa! Nyt voit saada selville sähkönkulutuksesi ja -tuotantosi päivä-, viikko-, ja kuukausitasolla helposti ja nopeasti!")
    print(" ")
    print("-"*len(pisin_teksti))
    print("Tervetuloa AurinkoSähköPaneelirapsageneraattori Palveluun!")
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
    #Mainos("Mainos")
    tiedostolista = luetiedostot()
    tunti_arvot = kasittele_Viikkodata(tiedostolista)
    paivakohtaiset_tulokset = paivalaskut(tunti_arvot)
    for i, (k, v) in enumerate(paivakohtaiset_tulokset.items()):
        print(k, v)
        if i == 3:
            break

    
    #tulosta_viikot(paivakohtaiset_tulokset)
    #rapsa = rapsan_luonti(paivakohtaiset_tulokset)
    #kysy_raportti(rapsa)
    
if __name__ == "__main__":
    main()
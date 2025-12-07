"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettu_varaus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettu_varaus.append(int(varaus[0]))
    # Ja tästä jatkuu
    muutettu_varaus.append(str(varaus[1]))
    muutettu_varaus.append(str(varaus[2]))
    muutettu_varaus.append(str(varaus[3]))
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").strftime("%H:%M"))
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(bool(varaus[8].strip().lower() in ["true", "kyllä", "yes", "1"]))
    muutettu_varaus.append(str(varaus[9]))
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")

    #Suoritetaan ensimmäinen vaihe
    print("------------------------------------------------------------------------------------")
    print( "1) Vahvistetut varaukset:")
    print( " ") #tyhjä rivi
    
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print("- " + str(varaus[1]), str(varaus[9]), str(varaus[4]), str(varaus[5]), sep=", ")
    print( " ") #tyhjä rivi

    #Suoritetaan toinen vaihe
    print("2) Pitkät varaukset (≥ 3 tuntia):")
    print( " ") #tyhjä rivi
    for varaus in varaukset[1:]:
        if varaus[6] >= 3:
            print("- " + str(varaus[1]) + ", " + str(varaus[4]) + " klo " + str(varaus[5]) + " kesto " + str(varaus[6]) + " h, " + str(varaus[9]))
    print( " ") #tyhjä rivi

    #Suoritetaan kolmas vaihe
    print("3) Varausten status: onko vahvistettu vai ei?")
    print( " ") #tyhjä rivi
    for varaus in varaukset[1:]:
        status = "Vahvistettu" if varaus[8] == True else "ei Vahvistettu"
        print("- " + str(varaus[1]) + " → " + status)
    print( " ") #tyhjä rivi

    #Suoritetaan neljäs vaihe
    print("4) Yhteenveto vahvistuksista:")
    print( " ") #tyhjä rivi
    vahvistettu_count = 0
    ei_vahvistettu_count = 0
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            vahvistettu_count += 1
        else:
            ei_vahvistettu_count += 1
    print("- Vahvistettuja varauksia: ", vahvistettu_count, " kpl" )
    print("- Ei vahvistettuja varauksia: ", ei_vahvistettu_count, " kpl" )
    print( " ") #tyhjä rivi

    #Suoritetaan viides vaihe
    print("5) Vahvistettujen varausten kokonaistulot:")
    kokonaistulot = 0.0
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            kokonaistulot += varaus[7]
    
    print("Vahvistettujen varausten kokonaistulot: {:.2f} €".format(kokonaistulot).replace('.', ','))
    print( " ") #tyhjä rivi
    
if __name__ == "__main__":
    main()
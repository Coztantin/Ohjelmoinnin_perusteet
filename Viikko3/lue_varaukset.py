"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
def hae_varausnumero(varaus):
    numero = varaus["Varausnumero"]
    print(f"Varausnumero: {numero}")

def hae_varaaja(varaus):
    nimi = varaus["Varaaja"]
    print(f"Varaaja: {nimi}")

def hae_varausaika(varaus):
    paiva = varaus["Päivämäärä"]
    aloitusaika = varaus["Aloitusaika"]
    tuntimaara = varaus["Tuntimäärä"]
    lopetusaika = varaus["Lopetusaika"]

    print(f"Päivämäärä: {paiva}")
    print(f"Aloitusaika: {aloitusaika}")
    print(f"Tuntimäärä: {tuntimaara}")
    print(f"Lopetusaika: {lopetusaika}")

def hae_maskutiedot(varaus):
    tuntihinta = varaus["Tuntihinta"]
    kokonaishinta = varaus["Kokonaishinta"]
    maksettu = varaus["Maksettu"]
    print(f"Tuntihinta: {tuntihinta:.2f} €".replace('.', ','))
    print(f"Kokonaishinta: {kokonaishinta:.2f} €".replace('.', ',') )
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    
def hae_yhteystiedot(varaus):
    kohde = varaus["Kohde"]
    puhelin = varaus["Puhelin"]
    sahkoposti = varaus["Sähköposti"]

    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sahkoposti}")

def main():


    from datetime import datetime
    from datetime import timedelta
    # Maaritellaan tiedoston nimi suoraan koodissa
    varauksetdata = "varaukset.txt"
    varaukset_lista = []

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varauksetdata, "r", encoding="utf-8") as f:
        varaukset = f.readlines()
        # Jaetaan rivit ja jaetaan sisältö listaksi
        for rivi in varaukset:

            osat = rivi.strip().split('|')
            pvm_obj = datetime.strptime(osat[2], "%Y-%m-%d").strftime("%d.%m.%Y") # Muutetaan päivämäärä objektiksi
            aika = datetime.strptime(osat[3], "%H:%M") # Muutetaan aika objektiksi
            lopetusaika = aika  + timedelta(hours=float((osat[4]))) # Lasketaan lopetusaika
            aika_str = aika.strftime("%H.%M")
            lopetusaika_str = lopetusaika.strftime("%H.%M")

            varaus = {
                "Varausnumero": int(osat[0]),
                "Varaaja": str(osat[1]),
                "Päivämäärä": pvm_obj,
                "Aloitusaika": aika_str,
                "Lopetusaika": lopetusaika_str,
                "Tuntimäärä": int(osat[4]),
                "Tuntihinta": float(osat[5]),
                "Kokonaishinta": float(osat[4]) * float(osat[5]),
                "Maksettu": (osat[6].strip().lower() in ["true", "kyllä", "yes", "1"]),
                "Kohde": str(osat[7]),
                "Puhelin": str(osat[8]),
                "Sähköposti": str(osat[9])
            }
            
            varaukset_lista.append(varaus)
    return varaukset_lista

def suorita_ohjelma():
    varaukset = main()
    for varaus in varaukset:
        hae_varausnumero(varaus)
        hae_varaaja(varaus)
        hae_varausaika(varaus)
        hae_maskutiedot(varaus)
        hae_yhteystiedot(varaus)
        print()  # Tyhjä rivi varausten väliin
    

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    #hae_varausnumero(varaus)
    #hae_varaaja(varaus)
    #hae_paiva(varaus)
    #hae_aloitusaika(varaus)
    #hae_tuntimaara(varaus)
    #hae_tuntihinta(varaus)
    #laske_kokonaishinta(varaus)
    #hae_maksettu(varaus)
    #hae_kohde(varaus)
    #hae_puhelin(varaus)
    #hae_sahkoposti(varaus)

if __name__ == "__main__":
    suorita_ohjelma()

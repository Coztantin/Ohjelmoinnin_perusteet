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
from datetime import datetime

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varauksetdata = "varaukset.txt"
    varaukset_lista = []

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varauksetdata, "r", encoding="utf-8") as f:
        varaukset = f.readlines()
        # Jaetaan rivit ja jaetaan sisältö listaksi
        for rivi in varaukset:
            osat = rivi.strip().split('|')

            varaus = {
                "Varausnumero": int(osat[0]),
                "Varaaja": str(osat[1]),
                "Päivämäärä": datetime.strptime(osat[2], "%Y-%m-%d").strftime("%d.%m.%Y"),
                "Aloitusaika": str(osat[3]).replace(":","."),
                "Tuntimäärä": float(osat[4]),
                "Tuntihinta": float(osat[5]),
                "Kokonaishinta": float(osat[4]) * float(osat[5]),
                "Maksettu": (osat[6].strip().lower() in ["true", "kyllä", "yes", "1"]),
                "Kohde": str(osat[7]),
                "Puhelin": str(osat[8]),
                "Sähköposti": str(osat[9].strip())
            }
            varaukset_lista.append(varaus)
    return varaukset_lista
    

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
    varaukset = main()
    
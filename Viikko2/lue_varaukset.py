"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

def main():

    
    # Määritellään tiedoston nimi suoraan koodissa
    varauksetdata = "varaukset.txt"
    varaus_lista = []
    # Avataan tiedosto ja luetaan sisältö
    with open(varauksetdata, "r", encoding="utf-8") as f:
        varaukset = f.readlines()
        for rivi in varaukset:
            osat = rivi.strip().split("|")
            varaus = {
                "Varausnumero": osat[0],
                "Varaaja": osat[1],
                "Päivämäärä": osat[2],
                "Aloitusaika": osat[3],
                "Tuntimäärä": osat[4],
                "Tuntihinta": osat[5],
                #"Kokonaishinta": osat[6],
                "Maksettu": osat[6],
                "Kohde": osat[7],
                "Puhelin": osat[8],
                "Sähköposti": osat[9]
            }
            varaus_lista.append(varaus)
    return varaus_lista
    
    
    

    # Tulostetaan varaus konsoliin
    #print(varaus)

    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))
    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    varaukset = main()
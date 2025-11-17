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
    from datetime import datetime
    from datetime import timedelta
    varauksetdata = "varaukset.txt"
    varaus_lista = []
    # Avataan tiedosto ja luetaan sisältö
    with open(varauksetdata, "r", encoding="utf-8") as f:
        varaukset = f.readlines()
        for rivi in varaukset:

            osat = rivi.strip().split("|")
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
                "Tuntimäärä": float(osat[4]),
                "Tuntihinta": float(osat[5]),
                "Kokonaishinta": float(osat[4]) * float(osat[5]),
                "Maksettu": (osat[6].strip().lower() in ["true", "kyllä", "yes", "1"]),
                "Kohde": str(osat[7]),
                "Puhelin": str(osat[8]),
                "Sähköposti": str(osat[9])
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
    for varaus in varaukset:
       
        print(f"Varausnumero: {varaus['Varausnumero']}")
        print(f"Varaaja: {varaus['Varaaja']}")
        print(f"Päivämäärä: {varaus['Päivämäärä']}") 
        print(f"Aloitusaika: {varaus['Aloitusaika']}")
        print(f"Tuntimäärä: {varaus['Tuntimäärä']}"" h")
        print(f"Lopetusaika: {varaus['Lopetusaika']}")
        print(f"Tuntihinta: {str(varaus['Tuntihinta']).replace('.',',')} €")
        print(f"Kokonaishinta: {str(varaus['Kokonaishinta']).replace('.',',')} €")
        if varaus['Maksettu']:
            print("Maksettu: Kyllä")
        else:
            print("Maksettu: Ei")
        print(f"Kohde: {varaus['Kohde']}")
        print(f"Puhelin: {varaus['Puhelin']}")
        print(f"Sähköposti: {varaus['Sähköposti']}")
        print()  # Tyhjä rivi varausten väliin

    vastaus = input("Haluatko tietää varausten yhteismäärän? Syötä ""Kyllä"" tai ""Ei"": ").strip().lower()
    if vastaus in ["kyllä", "yes", "joo"]:
        kaikkienvaraustensumma = 0
        for varaus in varaukset:
            kaikkienvaraustensumma += float(varaus["Kokonaishinta"])
        print("...") #jätetään vähä väliä    
        print(f"Kaikkien varausten yhteismäärä on: {str(kaikkienvaraustensumma).replace('.',',')} €")
        print("Kiitos ohjelman käytöstä!")
    else:
        print("Kiitos ohjelman käytöstä!")
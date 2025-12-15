# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.
# Copyright (c) 2025 Kosti Korkiakoski
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
# See LICENSE file in the project root for full license information.
#
# I have implemented the changes as per your assingment.
# Changes made:
# - Added docstrings to all functions.
# - changed from list to dict for better readability.
# - Added type hints to function signatures.
# - enhanced printing format for better clarity.

from datetime import datetime
from typing import List,Any
from typing import Dict,Any

def muunna_varaustiedot(varaus: list[str]) -> list[Any]:
    '''
    Docstring for muunna_varaustiedot
    
    :param varaus: Description
    :type varaus: list
    :return: Description
    :rtype: list[Any]
    '''
    muutettu_varaus = []
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(varaus[1])
    muutettu_varaus.append(varaus[2])
    muutettu_varaus.append(varaus[3])
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(varaus[8].lower() == "true")
    muutettu_varaus.append(varaus[9])
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus

def muunna_sanakirjaksi(varaukset: List[List[Any]]) -> Dict[int, Dict[str, Any]]:
    '''Muuttaa varaukset sanakirjaksi'''
    varaus_sanakirja = {}
    for varaus in varaukset[1:]:
        varaus_sanakirja[varaus[0]] = {
            "Nimi": varaus[1],
            "Sähköposti": varaus[2],
            "Puhelin": varaus[3],
            "Varauksen Pvm": varaus[4],
            "Varauksen Klo": varaus[5],
            "Varauksen Kesto": varaus[6],
            "Hinta": varaus[7],
            "Varaus Vahvistettu": varaus[8],
            "Varattu Tila": varaus[9],
            "Varaus Luotu": varaus[10]
        }
    return varaus_sanakirja


def hae_varaukset(varaustiedosto: str) -> list[list[Any]]:
    '''Hakee varaukset tiedostosta ja muuntaa ne listaksi, jossa jokainen varaus on listana. Tämän jälkeen kutsuta'''
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    muunna_sanakirjaksi(varaukset)
    return varaukset

def vahvistetut_varaukset(varaukset: Dict[int, Dict[str, Any]]) -> None:
    '''Käy läpi varaukset ja tulostaa vahvistetut varaukset'''

    print("1) Vahvistetut varaukset:")
    print("-"*30)
    for varaus in varaukset.keys(): #käydään läpi sanakirjan avaimet
        if(varaukset[varaus]["Varaus Vahvistettu"]) == True: #jos varaus on vahvistettu
            print(f"- {varaukset[varaus]['Nimi']}, {varaukset[varaus]['Varattu Tila']}, {varaukset[varaus]['Varauksen Pvm'].strftime('%d.%m.%Y')} klo {varaukset[varaus]['Varauksen Klo'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: Dict[int, Dict[str, Any]]) -> None:
    '''Vilkasee läpi varaukset ja tulostaa pitkät varaukset (yli 3 tuntia)'''
    print("2) Pitkät varaukset (≥ 3 h):")
    print("-"*30)
    for varaus in varaukset.keys():
        if(varaukset[varaus]["Varauksen Kesto"] >= 3):
            print(f"- {varaukset[varaus]['Nimi']}, {varaukset[varaus]['Varauksen Pvm'].strftime('%d.%m.%Y')} klo {varaukset[varaus]['Varauksen Klo'].strftime('%H.%M')}, kesto: {varaukset[varaus]['Varauksen Kesto']} h, {varaukset[varaus]['Varattu Tila']}")

    print()

def varausten_vahvistusstatus(varaukset: Dict[int, Dict[str, Any]]) -> None:
    '''Käy läpi varaukset ja tulostaa jokaisen varauksen vahvistusstatuksen'''
    print("3) Varausten vahvistusstatus:")
    print("-"*30)
    for varaus in varaukset.keys():
        status = "Vahvistettu" if varaukset[varaus]["Varaus Vahvistettu"] else "EI Vahvistettu"
        print(f"- {varaukset[varaus]['Nimi']} → {status}.")
    print()

def varausten_lkm(varaukset: Dict[int, Dict[str, Any]]) -> None:
    '''Laskee varauksien lukumäärän vahvistettuna ja ei vahvistettuna'''
    print("4) Yhteenveto vahvistuksista:")
    print("-"*30)
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset.keys():
        if(varaukset[varaus]["Varaus Vahvistettu"]) == True:
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: Dict[int, Dict[str, Any]]) -> None:
    '''Laskee vahvistettujen varausten kokonaistulot'''
    print("5) Varausten varausten kokonaistulot:")
    print("-"*30)
    varaustenTulot = 0
    for varaus in varaukset.keys():
        if(varaukset[varaus]["Varaus Vahvistettu"]) == True:
            varaustenTulot += varaukset[varaus]["Hinta"]

    print("- Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

def main():
    '''pääohjelma'''
    varaukset = hae_varaukset("varaukset.txt")
    varaukset_sanakirjana = muunna_sanakirjaksi(varaukset)
    print()
    vahvistetut_varaukset(varaukset_sanakirjana)
    pitkat_varaukset(varaukset_sanakirjana)
    varausten_vahvistusstatus(varaukset_sanakirjana)
    varausten_lkm(varaukset_sanakirjana)
    varausten_kokonaistulot(varaukset_sanakirjana)

if __name__ == "__main__":
    main()
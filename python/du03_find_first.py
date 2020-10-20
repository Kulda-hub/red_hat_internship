#!/usr/bin/env python3

# Povolene knihovny: math
# (Poznamka: "povolene" neznamena "nutne"; ukol je mozno snadno vyresit i bez
#  jakychkoli knihoven.)

# IB002 Domaci uloha 3.
#
# Vasi ulohou bude s vyuzitim principu binarniho vyhledavani implementovat
# dve funkce, find_first_occurrence a find_first_greater. V obou pripadech
# musi casova slozitost vaseho algoritmu byt nejhure logaritmicka, tedy byt
# v O(log n). (Pozor, iterovani v poli a slicing a[x:y] ma linearni slozitost.)
# Funkce nesmi modifikovat vstupni pole.


# Ukol 1.
# Implementujte funkci find_first_occurrence, ktera vrati index prvniho
# vyskytu prvku key v serazenem poli numbers. Pokud se prvek v poli
# nevyskytuje, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_occurrence(2, [1, 2, 2, 2, 4]) -->  1
# find_first_occurrence(3, [1, 2, 4, 5])    --> -1

def find_first_occurrence(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu hodnoty 'key' v poli 'numbers',
            -1, pokud se tam tato hodnota nevyskytuje
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """
    low = 0
    high = len(numbers)-1
    if high == -1:
        return -1
    while low <= high:
        mid = (low+high)//2
        mid_value = numbers[mid]
        if mid_value < key:
            low = mid+1
        elif mid_value > key:
            high = mid-1
        elif low != mid:
            high = mid
        else:
            return mid
    return -1
# Ukol 2.
# Implementujte funkci find_first_greater modifikaci predchozi funkce
# find_first_occurrence tak, ze find_first_greater vrati index prvniho prvku
# v poli vetsiho nez key. Neni-li v poli zadny takovy, vrati -1.
#
# Priklady vstupu a vystupu:
# find_first_greater(2, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 4, 5]) -->  2
# find_first_greater(3, [1, 2, 3])    --> -1


def find_first_greater(key, numbers):
    """
    vstup: 'key' hodnota hledaneho cisla, 'numbers' serazene pole cisel
    vystup: index prvniho vyskytu prvku vetsiho nez hodnota 'key',
            -1, pokud tam zadny takovy prvek neni
    casova slozitost: O(log n), kde 'n' je pocet prvku pole 'numbers'
    """

    low = 0
    high = len(numbers)-1
    if high == -1 or numbers[high] <= key:
        return -1
    while low != high:
        mid = (low + high) // 2
        mid_value = numbers[mid]
        if mid_value <= key:
            low = mid + 1
        else:
            high = mid

    return low
"""
Moje_pole =[0,1,1,2,4,5,5]
Moje_pole_extra = [0,4]
print(find_first_occurrence(5,Moje_pole_extra))
print(find_first_greater(1,Moje_pole))
"""

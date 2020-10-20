#!/usr/bin/env python3
import math
# Povolene knihovny: math

# IB002 Domaci uloha 6.
#
# V nasledujicim textu pouzivame pojem "halda" ve vyznamu "binarni halda".
#
# Minimova halda je v kanonickem tvaru, pokud pro kazdy jeji prvek se dvema
# potomky plati, ze jeho levy potomek je mensi nez ten pravy nebo se oba
# rovnaji.
#
# Je v kanonickem tvaru | Neni v kanonickem tvaru
#                       |
#       (1)             |           (1)
#      /   \            |          /   \
#    (2)   (3)          |        (3)   (2)


# Trida representujici minimovou haldu. Pro praci s ni muzete s vyhodou pouzit
# funkce, ktere jste implementovali v zakladnim domacim ukolu.
# V teto implementaci indexujte od 0, tj. koren je na pozici heap.array[0].

class MinHeap:
    __slots__ = ("size", "array")

    def __init__(self):
        self.size = 0
        self.array = []


# Ukol 1.
# Vasim prvnim ukolem je implementovat funkci is_canonical_min_heap(heap),
# ktera overi, zda je zadana halda 'heap' korektni minimovou haldou
# v kanonickem tvaru. Pokud ano, vrati True, v opacnem pripade vrati False.
#
# Prazdna nebo jednoprvkova halda je v kanonickem tvaru implicitne. Mejte na
# pameti, ze halda v kanonickem tvaru musi splnovat take pozadavky kladene na
# minimovou haldu.

def is_canonical_min_heap(heap):
    """
    vstup: 'heap' typu MinHeap
           (je zaruceno, ze heap.size je velikost pole heap.array;
            neni zaruceno, ze prvky heap.array splnuji haldovou podminku
            nebo podminku kanonickeho tvaru)
    vystup: True, pokud je 'heap' minimova halda v kanonickem tvaru
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    if heap.size == 0:
        return True

    if 2 >= heap.size:
        last = math.inf
    else:
        last = heap.array[2]

    if 1 >= heap.size:
        middle = math.inf
    else:
        middle = heap.array[1]

    if not (last >= middle >= heap.array[0]):
        return False

    for i in range(1, heap.size//2):
        if 2 * i + 2 >= heap.size:
            last = math.inf
        else:
            last = heap.array[2 * i + 2]

        if not (last >= heap.array[2 * i + 1] >= heap.array[i]):
            return False
    return True


# Ukol 2.
# Druhym ukolem je implementovat funkci canonise_min_heap(heap), ktera zadanou
# minimovou haldu 'heap' prevede na kanonicky tvar. Funkce bude menit primo
# haldu zadanou v argumentu, proto nebude vracet zadnou navratovou hodnotu.
#
# Napoveda:
# Pro algoritmus s linearni casovou slozitosti je potreba postupovat takto:
# - Rekurzivne resime od korene k listum haldy;
# - pro kazdy uzel haldy:
#   + zkontrolujeme, jestli potomci splnuji vlastnost kanonickeho tvaru;
#     pokud ne:
#     * prohodime hodnoty leveho a praveho potomka;
#     * tim se muze pokazit vlastnost haldy v pravem podstrome, proto
#       probublame problematickou hodnotu z korene praveho podstromu
#       tak hluboko, aby uz neporusovala vlastnost haldy (pri tomto bublani
#       opravujeme pouze vlastnost haldy, kanonicky tvar neresime)
#   + mame tedy korektni minimovou haldu, ktera navic splnuje kanonicky
#     tvar od tohoto uzlu smerem nahoru;
#   + pokracujeme v rekurzi vlevo a vpravo.


def canonise_min_heap(heap):
    """
    vstup: 'heap' korektni minimova halda typu MinHeap
    vystup: funkce nic nevraci, vstupni halda 'heap' je prevedena
            do kanonickeho tvaru (pritom obsahuje stejne prvky jako na zacatku)
    casova slozitost: O(n), kde 'n' je pocet prvku 'heap'
    """
    canonise_min_heap_from_point(heap, 0, len(heap.array))


def canonise_min_heap_from_point(heap, point, size):
    if point * 2 + 2 >= size:
        return

    if heap.array[point * 2 + 2] < heap.array[point * 2 + 1]:
        heap.array[point * 2 + 1], heap.array[point * 2 + 2] = heap.array[point * 2 + 2], heap.array[point * 2 + 1]
        correct_min_heap_from_point(heap, point * 2 + 2, size)

    canonise_min_heap_from_point(heap, point * 2 + 1, size)
    canonise_min_heap_from_point(heap, point * 2 + 2, size)


def correct_min_heap_from_point(heap, point, size):
    minim = heap.array[point]
    if point * 2 + 1 < size:
        if heap.array[point * 2 + 1] < minim:
            minim = heap.array[point * 2 + 1]
        if point * 2 + 2 < size:
            if heap.array[point * 2 + 2] < minim:
                heap.array[point], heap.array[point * 2 + 2] = heap.array[point * 2 + 2], heap.array[point]
                correct_min_heap_from_point(heap, point * 2 + 2, size)
                return
        if heap.array[point] != minim:
            heap.array[point], heap.array[point * 2 + 1] = heap.array[point * 2 + 1], heap.array[point]
            correct_min_heap_from_point(heap, point * 2 + 1, size)
    return


"""ole = []
for i in range(0, 15):
    pole.append(i)
print(pole)
for i in range(1,15,2):
    pole[i], pole[i+1] = pole[i+1], pole[i]
print(pole)
halda = MinHeap()
halda.array = pole
halda.size = len(halda.array)
canonise_min_heap(halda)
print(halda.array)"""

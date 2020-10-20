#!/usr/bin/env python3
import copy
# Povolene knihovny: copy, math
# (Poznamka: "povolene" neznamena "nutne"; ukol je mozno vyresit i bez
#  jakychkoli knihoven.)

# IB002 Domaci uloha 4.
#
# V tomto ukolu uvazujeme pole, ktera obsahuji pouze cisla -1, 0, 1.
# Vasim ukolem bude implementovat funkci trit_sum, ktera pro zadana cisla
# `length` a `total` vrati seznam vsech takovych poli delky `length`, jejichz
# soucet je presne `total`.
#
# Priklady:
# Pro vstup length=2 a total=0 bude vystupem:
#   [[-1, 1], [0, 0], [1, -1]]
# Pro vstup length=4 a total=-3 bude vystupem:
#   [[-1, -1, -1, 0], [-1, -1, 0, -1], [-1, 0, -1, -1], [0, -1, -1, -1]]
#
# Pocty poli pro dane hodnoty `length` a `total` se daji zapsat nasledovne:
#
#                             total
# length|  -5  -4  -3  -2  -1   0   1   2   3   4   5
# ------+----------------------------------------------
#    0  |   0   0   0   0   0   1   0   0   0   0   0
#    1  |   0   0   0   0   1   1   1   0   0   0   0
#    2  |   0   0   0   1   2   3   2   1   0   0   0
#    3  |   0   0   1   3   6   7   6   3   1   0   0
#    4  |   0   1   4  10  16  19  16  10   4   1   0
#   ...
#
# Vsimnete si, ze kazda hodnota v tabulce je souctem tri hodnot: te
# bezprostredne nad ni a dvou sousedicich. (Tomuto se rika trinomialni
# trojuhelnik, viz https://en.wikipedia.org/wiki/Trinomial_triangle.)
#
# Toto pozorovani muzete jednak pouzit pro kontrolu toho, ze vase reseni
# pocita spravne, jednak bude hodnota v tabulce hrat roli v casove slozitosti
# reseni.
#
# Pozadovanou funkci je vhodne resit rekurzivne. Pro dodrzeni spravne casove
# slozitosti je treba si dobre rozmyslet, ve kterych chvilich je vhodne
# rekurzi ukoncit.


def trit_sum(length, total):
    """
    vstup: `length` - nezaporne cele cislo
           `total` - cele cislo
    vystup: seznam vsech poli delky presne `length`,
            jejichz soucet je presne `total`
    casova slozitost: O(T(length, total) * length^2),
        kde T(length, total) je hodnota z tabulky naznacene vyse
    """
    if length == 0 and total != 0:
        return []
    main_array = []
    recursion_training(main_array, [], 0, total, length)
    return main_array


"""def recursion_training_extra(main_array, extra_array, total, length):
    if length == 0:
        main_array.append(extra_array)
        return
    if abs(-total - 1) < length:
        array_plus_one = copy.deepcopy(extra_array)
        array_plus_one.append(1)
        recursion_training_extra(main_array, array_plus_one, total+1, length-1)
    if abs(-total + 1) < length:
        array_minus_one = copy.deepcopy(extra_array)
        array_minus_one.append(-1)
        recursion_training_extra(main_array, array_minus_one, total-1, length-1)
    if abs(-total) < length:
        array_zero = copy.deepcopy(extra_array)
        array_zero.append(0)
        recursion_training_extra(main_array, array_zero, total, length-1)
    return """


def recursion_training(main_array, extra_array, value, total, length):
    if length == 0:
        main_array.append(extra_array)
        return
    if abs(value + 1 - total) < length:
        array_plus_one = extra_array[:]
        array_plus_one.append(1)
        recursion_training(main_array, array_plus_one, value+1, total, length-1)
    if abs(value - 1 - total) < length:
        array_minus_one = extra_array[:]
        array_minus_one.append(-1)
        recursion_training(main_array, array_minus_one, value-1, total, length-1)
    if abs(value - total) < length:
        extra_array.append(0)
        recursion_training(main_array, extra_array, value, total, length-1)
    return



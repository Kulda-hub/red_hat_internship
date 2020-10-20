#!/usr/bin/env python3

# Povolene knihovny: math

# IB002 Domaci uloha 7.
#
# Souctovy strom je binarni strom, kde kazdy uzel ma nasledujici vlastnost:
# Pokud ma uzel alespon jednoho syna, potom je klic uzlu roven souctu klicu
# vsech jeho synu. Listy stromu tedy mohou obsahovat libovolne hodnoty.
# Za souctovy je povazovan i strom, ktery neobsahuje zadne uzly, a strom,
# ktery obsahuje prave jeden uzel.
#
# Muzete si samozrejme pridat vlastni pomocne funkce.
#
# Priklad:
# souctove stromy      nesouctove stromy
#   53       47            53       47
#  /  \        \          /  \     /
# 21  32       47        21  21   46
#             /  \                  \
#            1    46                 1

# Do nasledujicich definic trid nijak nezasahujte.
#
# Trida pro reprezentaci souctoveho stromu.
# root je koren stromu a je typu Node, nebo None, pokud je strom prazdny.
#
# Pro vykreslovani stromu muzete pouzit funkci make_graph z cv07.


class SumTree:
    __slots__ = ("root",)

    def __init__(self):
        self.root = None


# Trida pro reprezentaci uzlu v souctovem strome.
# key je hodnota uzlu, ktera ma byt rovna souctu hodnot vsech synu.

class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self):
        self.key = 0
        self.left = None
        self.right = None


# Ukol 1.
# Vasim prvnim ukolem je napsat funkci, ktera vybuduje uplny souctovy strom ze
# zadaneho pole. Listy stromu budou prave prvky pole v poradi zleva doprava.
# Delka pole bude vzdy mocninou dvojky. Vstupni pole nijak nemodifikujte.
#
# Napriklad:
# Z pole [1,2,3,4] vznikne strom:
#      10
#    /    \
#   3      7
#  / \    / \
# 1   2  3   4

def build_sum_tree(array):
    """
    vstup: pole (Pythonovsky seznam) 'array' cisel delky 'n',
           kde 'n' je nejaka mocnina dvojky
    vystup: korektni strom typu SumTree, ktery ma v listech (v poradi zleva
            doprava) hodnoty ze zadaneho pole 'array'
            strom musi byt uplny, tj. vsechna jeho patra musi byt zcela
            zaplnena
    casova slozitost: O(n)
    extrasekvencni prostorova slozitost: O(log n)
        (Nepocita se prostor vstupniho pole a vybudovaneho vystupniho stromu,
         pocita se zasobnik rekurze.)
    """
    root_node = Node()
    if len(array) == 1:
        root_node.key = array[0]
    else:
        root_node.key = (build_sum_tree_rec(array, 0, len(array) // 2,
                         len(array) // 2, root_node, True) +
                         build_sum_tree_rec(array, len(array) // 2, len(array),
                         len(array) // 2, root_node, False))
    my_sum_tree = SumTree()
    my_sum_tree.root = root_node
    return my_sum_tree


def build_sum_tree_rec(array, array_start, array_end, array_part_length, parent_node, is_left):
    if array_start + 1 == array_end:
        new_node = Node()
        if is_left:
            parent_node.left = new_node
        else:
            parent_node.right = new_node
        new_node.key = array[array_start]
        return new_node.key
    new_node = Node()
    new_node.key = (build_sum_tree_rec(array, array_start, array_end - array_part_length // 2,
                                       array_part_length // 2, new_node, True) +
                    build_sum_tree_rec(array, array_start + array_part_length // 2, array_end,
                                       array_part_length // 2, new_node, False))
    if is_left:
        parent_node.left = new_node
    else:
        parent_node.right = new_node
    return new_node.key


# Ukol 2.
# Vasim druhym ukolem je napsat funkci is_sum_tree, ktera overi, zda je strom
# souctovy. Pokud ano, vraci True, jinak False.
# Vstupni strom nemodifikujte ani v prubehu vypoctu nevytvarejte nove stromy
# nebo uzly.

def is_sum_tree(tree):
    """
    vstup: 'tree' typu SumTree
           (je zaruceno, ze uzly ve strome jsou typu Node;
            neni zaruceno, ze splnuji souctovou podminku)
    vystup: True, pokud je 'tree' korektni SumTree, tj. vsechny jeho uzly
                  splnuji souctovou podminku
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku 'tree'
    """
    if tree.root is None:
        return True
    return is_sum_tree_rec(tree.root)


def is_sum_tree_rec(node):
    if node.left is None and node.right is None:
        return True
    a = 0
    b = 0
    is_sum_of_left = True
    is_sum_of_right = True
    if node.left is not None:
        is_sum_of_left = is_sum_tree_rec(node.left)
        a = node.left.key
    if node.right is not None:
        is_sum_of_right = is_sum_tree_rec(node.right)
        b = node.right.key

    if a + b == node.key and is_sum_of_left and is_sum_of_right:
        return True
    return False


# Ukol 3.
# Vasim tretim ukolem je ze zadaneho souctoveho stromu smazat vsechny listy
# s hodnotou 0. Pokud timto mazanim vzniknou nove listy s hodnotou 0,
# je treba rekurzivne smazat i ty. Modifikujte primo zadany strom, nevytvarejte
# zadne nove stromy ani uzly.

def remove_zero_leaves(tree):
    """
    vstup: 'tree' korektni souctovy strom typu SumTree
    vystup: zadny, ze stromu 'tree' jsou vymazany vsechny listy s hodnotou 0
            (vcetne vsech listu s hodnotou 0, ktere vzniknou timto mazanim)
    casova slozitost: O(n), kde 'n' je pocet prvku puvodniho 'tree'
    """

    if tree.root is None:
        return
    remove_root = remove_zero_leaves_rec(tree.root)
    if remove_root:
        tree.root = None


def remove_zero_leaves_rec(node):
    if node.left is not None and remove_zero_leaves_rec(node.left):
        node.left = None
    if node.right is not None and remove_zero_leaves_rec(node.right):
        node.right = None
    if node.left is None and node.right is None and node.key == 0:
        return True
    return False


"""TESTING
myarray = [1]

sumtree = build_sum_tree(myarray)

print(sumtree.root.key, "\n")
print(sumtree.root.left.key, "   ", sumtree.root.right.key, "\n")
print(sumtree.root.left.left.key, " ", sumtree.root.left.right.key,
        " ", sumtree.root.right.left.key, " ", sumtree.root.right.right.key)
"""

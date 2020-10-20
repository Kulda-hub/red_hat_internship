#!/usr/bin/env python3

# Povolene knihovny: math

# IB002 Domaci uloha 9.
#
# V teto uloze se budeme zabyvat binarnimi vyhledavacimi stromy.
#
# V prvni casti bude Vasi ulohou sestavit skoro uplny binarni vyhledavaci strom
# obsahujici zadane klice. Vstupni pole klicu bude usporadano od nejmensich po
# nejvetsi. Vas algoritmus musi mit LINEARNI casovou slozitost vzhledem k poctu
# zadanych klicu. Tento pozadavek je splnitelny diky usporadanosti pole na
# vstupu.
#
# V druhe casti bude Vasi ulohou zjistit, jestli zadany binarni vyhledavaci
# strom je skoro uplny. Pozadovana casova slozitost je linearni vuci poctu uzlu
# ve strome.
#
# Ve treti casti bude Vasi ulohou zjistit, jestli zadany binarni vyhledavaci
# strom ma vsechny listy ve stejne hloubce. Pozadovana casova slozitost je opet
# linearni vuci poctu uzlu ve strome.
#
# Skoro uplny strom ma zaplnena vsechna patra, jen posledni nemusi byt uplne
# zaplneno (a rovnez nemusi byt doleva zarovnane).
#
# Pro ilustraci, pro vstup (1,2,3,4,5,6,7,8,9,10) je korektnim vystupem
# algoritmu z prvni casti napriklad jeden z nasledujicich stromu:
#
#             ( 5 )                           ( 7 )
#            /     \                         /     \
#          (2)     (8)                  ( 4 )       ( 9 )
#         /  \     /  \                /     \      /   \
#       (1)  (3) (6)  (9)            (2)     (6)  (8)   (10)
#              \   \    \            / \     /
#              (4) (7)  (10)       (1) (3) (5)
#
# Do nasledujicich definic trid nijak nezasahujte.
#
# Pro vykreslovani stromu muzete pouzit funkci make_graph z cv07.


class BSTree:
    """Trida BSTree pro reprezentaci binarniho vyhledavacicho stromu.

    Atributy:
        root   koren stromu typu Node, nebo None, pokud je strom prazdny
    """
    __slots__ = ("root",)

    def __init__(self):
        self.root = None


class Node:
    """Trida Node pro reprezentaci uzlu binarniho vyhledavaciho stromu.

    Atributy:
        key     klic daneho uzlu (zadany pri inicializaci)
        left    odkaz na leveho potomka typu Node, nebo None, pokud neexistuje
        right   odkaz na praveho potomka typu Node, nebo None, pokud neexistuje
    """
    __slots__ = ("left", "right", "key")

    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


# Ukol 1.
# Implementuje funkci build_bst, ktera dostane vzestupne serazeny seznam hodnot
# a vytvori z nich skoro uplny binarni vyhledavaci strom (typu BSTree).
# Zadane pole hodnot nijak nemodifikujte.

def build_bst(array):
    """
    vstup: 'array' vzestupne serazene pole hodnot
    vystup: strom typu BSTree, ktery je skoro uplny (viz vyse) a obsahuje
            hodnoty z pole array
    casova slozitost: O(n), kde 'n' je delka array
    extrasekvencni prostorova slozitost:
         O(log n), nepocitame do ni vstupni pole ani vystupni strom,
         pocitame zasobnik rekurze
    """
    my_tree = BSTree()
    if len(array) == 0:
        return my_tree
    my_tree.root = build_bst_rec(array, 0, len(array) - 1)
    return my_tree  # TODO


def build_bst_rec(array, array_start, array_end):
    if array_start > array_end:
        return None
    middle = (array_start + array_end) // 2
    my_node = Node(array[middle])
    my_node.left = build_bst_rec(array, array_start, middle - 1)
    my_node.right = build_bst_rec(array, middle + 1, array_end)

    return my_node

# Ukol 2.
# Implementujte funkci check_almost_complete, ktera dostane binarni vyhledavaci
# strom a otestujte, zda je skoro uplny.
# Strom nijak nemodifikujte, ani nevytvarejte nove uzly nebo stromy.


def check_almost_complete(tree):
    """
    vstup: 'tree' binarni vyhledavaci strom typu BSTree
    vystup: True, pokud je 'tree' skoro uplny
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet uzlu stromu
    extrasekvencni prostorova slozitost: O(h), kde h je vyska stromu
        (nepocitame vstup, pocitame zasobnik rekurze)
    """
    if tree.root is None:
        return True
    low_level = find_lowest_level(tree.root, 0)
    return check_almost_complete_node(tree.root, low_level, 0)


def check_almost_complete_node(node, low_level, level):
    if node.left is None and node.right is None:
        if level == low_level + 1 or level == low_level:
            return True
        return False
    if node.left is not None and node.right is None:
        if level == low_level:
            return check_almost_complete_node(node.left, low_level, level + 1)
        return False
    if node.left is None and node.right is not None:
        if level == low_level:
            return check_almost_complete_node(node.right, low_level, level + 1)
        return False
    return check_almost_complete_node(node.left, low_level, level + 1) and check_almost_complete_node(node.right,
                                                                                                      low_level,
                                                                                                      level + 1)


def find_lowest_level(node, level):
    if node.left is None and node.right is None:
        return level
    if node.left is not None and node.right is None:
        return level
    if node.left is None and node.right is not None:
        return level
    return min(find_lowest_level(node.left, level + 1), find_lowest_level(node.right, level + 1))
# Ukol 3
# Implementujte funkci check_all_leaves_same_depth, ktera overi, zda jsou
# vsechny listy zadaneho binarniho vyhledavaciho stromu ve stejne hloubce.
# Strom nijak nemodifikujte, ani nevytvarejte nove uzly nebo stromy.


def check_all_leaves_same_depth(tree):
    """
    vstup: 'tree' binarni vyhledavaci strom typu BSTree
    vystup: True, pokud jsou vsechny listy 'tree' ve stejne hloubce
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet uzlu stromu
    extrasekvencni prostorova slozitost: O(h), kde h je vyska stromu
        (nepocitame vstup, pocitame zasobnik rekurze)
    """
    if tree.root is None:
        return True
    my_array = []
    return check_all_leaves_same_depth_rec(tree.root, my_array, 0)


def check_all_leaves_same_depth_rec(node, array_level, level):
    if node.left is None and node.right is None:
        if len(array_level) == 0:
            array_level.append(level)
        if level == array_level[0]:
            return True
        return False
    if node.left is not None and node.right is None:
        return check_all_leaves_same_depth_rec(node.left, array_level, level + 1)
    if node.left is None and node.right is not None:
        return check_all_leaves_same_depth_rec(node.right, array_level, level + 1)
    return check_all_leaves_same_depth_rec(node.left, array_level, level + 1)\
        and check_all_leaves_same_depth_rec(node.right, array_level, level + 1)


"""def inorder(node):
    if not node:
        return
    print(node.key)
    inorder(node.left)

    inorder(node.right)


arr = [1, 2, 3, 4, 5, 6, 7]
my_tree = BSTree()
my_tree = build_bst(arr)
print(check_almost_complete(my_tree))
print(check_all_leaves_same_depth(my_tree))
inorder(my_tree.root)"""

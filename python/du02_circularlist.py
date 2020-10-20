#!/usr/bin/env python3

# IB002 Domaci uloha 2.
#
# Jednosmerne spojovany seznam uz znate - jde o zretezeny seznam uzlu (Node),
# kde kazdy uzel ukazuje na sveho naslednika. V tomto prikladu nemame first
# (ani last), seznam je zadany "prvnim" ze svych uzlu.
# Seznamy v teto uloze nikdy nebudou prazdne, tj. vzdy muzete predpokladat,
# ze na vstupu je objekt typu Node.
#
# Tato uloha pracuje se dvema typy jednosmerne spojovanych seznamu:
# Linearni seznam - kde posledni prvek seznamu ukazuje na None.
# Kruhovy seznam - kde posledni prvek seznamu ukazuje zpet na prvni prvek.
#
# Pro vsechny funkce muzete predpokladat, ze seznam na vstupu je linearni,
# nebo kruhovy, tj. nemusite napriklad osetrovat situaci, kdy naslednikem
# "posledniho" v seznamu je "druhy".
#
# Podobne jako u minule ulohy, smyslem je vyzkouset si praci s odkazy.
# I v teto uloze je tedy zakazano pouzivat seznamy (list), slovniky (dict)
# a mnoziny (set).
# Rovnez nejsou povoleny zadne Pythonovske knihovny.
# (Pokud chcete tyto veci pouzivat pro vlastni testovani, nezapomente je
#  pred odevzdanim vymazat nebo zakomentovat.)
#
# Ve vystupu vyhodnocovaci sluzby znazornujeme jednosmerne spojovane seznamy
# podobne jako u minuleho ukolu:
#
# Toto je linearni seznam o trech prvcich:
# linearni seznam: -> 7 -> 42 -> 17
# Toto je kruhovy seznam o trech prvcich:
# kruhovy seznam: -> 7 -> 42 -> 17 -> zpet na zacatek
#
# Do definice tridy Node nijak nezasahujte.


class Node:
    """Trida Node reprezentujici prvek ve spojovanem seznamu

    Atributy:
        key        klic daneho uzlu (cele cislo)
        next       odkaz na dalsi prvek seznamu
        opposite   odkaz na protejsi prvek seznamu, viz ukol 3.
    """

    __slots__ = ('key', 'next', 'opposite')

    def __init__(self):
        self.key = 0
        self.next = None
        self.opposite = None


# Ukol 1.
# Implementujte funkci is_circular, ktera dostane prvni uzel seznamu
# a otestuje, zda je zadany zretezeny seznam kruhovy.

def is_circular(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: True, pokud je seznam z uzlu 'node' kruhovy
            False, jinak
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    first_node = node
    current_node = node.next
    while current_node != first_node:
        if current_node is None:
            return False
        current_node = current_node.next
    return True


# Ukol 2.
# Implementujte funkci get_length, ktera vrati delku (tj. pocet uzlu)
# linearniho nebo kruhoveho zretezeneho seznamu zacinajiciho v zadanem uzlu.

def get_length(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: pocet prvku v zadanem seznamu
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    first_node = node
    current_node = node.next
    length = 1
    while current_node != first_node and current_node is not None:
        length += 1
        current_node = current_node.next
    return length


# Ukol 3.
# Implementujte funkci calculate_opposites, ktera korektne naplni atributy
# "opposite" v uzlech kruhoveho seznamu sude delky. Tj. pro kruhove seznamy
# delky 2n naplni u kazdeho uzlu atribut opposite uzlem, ktery je o n kroku
# dale (tedy v kruhu je to uzel "naproti").
#
# Napriklad v kruhovem seznamu 1 -> 2 -> 3 -> 4 (-> 1) je opposite
# uzlu 1 uzel 3, uzlu 2 uzel 4, uzlu 3 uzel 1 a uzlu 4 uzel 2.
#
# Pokud vstupni seznam neni kruhovy nebo ma lichou delku, tak funkce
# calculate_opposites seznam neupravuje.
#
# Pozor na casovou a prostorovou slozitost vaseho algoritmu!

def calculate_opposites(node):
    """
    vstup: 'node' prvni uzel seznamu, ktery je linearni, nebo kruhovy
    vystup: nic, kokretne doplni atribut opposite pro kruhovy seznam sude delky
    casova slozitost: O(n), kde 'n' je pocet prvku seznamu
    """
    length = get_length(node)
    if length % 2 == 1 or not is_circular(node):
        return
    first_node = node
    sec_half_node = node
    half_length = length/2
    while length != half_length:
        sec_half_node = sec_half_node.next
        length -= 1
    while length != 0:
        first_node.opposite = sec_half_node
        sec_half_node.opposite = first_node
        first_node = first_node.next
        sec_half_node = sec_half_node.next
        length -= 1


"""
TESTING
node_1 = Node()
node_2 = Node()
node_3 = Node()
node_4 = Node()
node_5 = Node()
node_6 = Node()
node_7 = Node()
node_8 = Node()
node_9 = Node()
node_10 = Node()
node_1.key = 1
node_2.key = 2
node_3.key = 3
node_4.key = 4
node_5.key = 5
node_6.key = 6
node_7.key = 7
node_8.key = 8
node_9.key = 9
node_10.key = 10
node_1.next = node_2
node_2.next = node_3
node_3.next = node_4
node_4.next = node_5
node_5.next = node_6
node_6.next = node_7
node_7.next = node_8
node_8.next = node_9
node_9.next = node_10
node_10.next = node_1

node_extra_1 = Node()
node_extra_2 = Node()
node_extra_1.key = "extra 1"
node_extra_2.key = "extra 2"
node_extra_1.next = node_extra_2
node_extra_2.next = node_extra_1

calculate_opposites(node_extra_1)
print(node_extra_1.opposite.key)
print(node_extra_2.opposite.key)

calculate_opposites(node_8)
print(node_1.opposite.key)
print(node_2.opposite.key)
print(node_3.opposite.key)
print(node_4.opposite.key)
print(node_5.opposite.key)
print(node_6.opposite.key)
print(node_7.opposite.key)
print(node_8.opposite.key)
print(node_9.opposite.key)
print(node_10.opposite.key)
"""

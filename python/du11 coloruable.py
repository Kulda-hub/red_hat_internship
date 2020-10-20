#!/usr/bin/env python3

# Povolene knihovny: math, collections
# Z knihovny collections je povolena pouze datova struktura deque
# reprezentujici frontu. Pro jeji import pouzijte presne nasledujici radek:

from collections import deque

# IB002 Domaci uloha 11.
#
# Tento tyden bude vasim ukolem implementovat dva grafove algoritmy.
# Ukoly jsou zamereny na aplikace pruchodu grafem.
#
# Reprezentace grafu je stejna jako v ukolu cv11, tedy matici sousednosti.
# Matice je indexovana od [0][0], vrcholum odpovidaji cisla 0 .. graph.size-1.
# V matici je na indexu [u][v] hodnota True, pokud graf obsahuje hranu u -> v,
# jinak je tam hodnota False.
#
# Grafy (i neorientovane!) mohou obsahovat smycky (tj. situace, kdy v matici
# na indexu [u][u] je True) a mohou byt i nesouvisle.
#
# Pripomenuti prace s frontou typu deque:
# inicializace fronty: queue = deque() nebo queue = deque([seznam prvku])
# vlozeni prvku do fronty: queue.append(prvek)
# vybrani prvku z fronty: queue.popleft(prvek)
#
# Definici tridy Graph nijak nemodifikujte, ani nepridavejte zadne atributy.
# Zamerne se v teto uloze budete muset obejit bez pomocnych poli ve tride
# Graph; budete muset pouzit lokalni promenne a pripadne parametry v rekurzi.
#
# V teto uloze je zakazano pouzivat datove struktury set (mnoziny) a dict
# (slovniky). Uvedomte si, ze vrcholy grafu jsou vzdy cisla od 0 do size - 1.


class Graph:
    """Trida Graph drzi graf reprezentovany matici sousednosti.
    Atributy:
        size: velikost (pocet vrcholu) grafu
        matrix: matice sousednosti
                [u][v] reprezentuje hranu u -> v
    """
    __slots__ = ("size", "matrix")

    def __init__(self, size):
        self.size = size
        self.matrix = [[False] * size for _ in range(size)]


# Ukol 1.
# Implementujte funkci colourable, ktera zjisti, zda je dany neorientovany graf
# obarvitelny dvema barvami tak, aby kazde dva sousedni vrcholy mely ruznou
# barvu.
#
# Neorientovany graf v nasi reprezentaci znamena, ze
#    graph.matrix[u][v] == graph.matrix[v][u] pro vsechny vrcholy u, v.

def colourable(graph):
    """Zjisti, zda je zadany neorientovany graf obarvitelny dvema barvami.
    Vstup:
        graph - neorientovany graf typu Graph
    Vystup:
        True, pokud je graf obarvitelny dvema barvami
        False, jinak
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(n), kde n je pocet vrcholu grafu
    """
    vertex_array = []
    queue = deque()
    for i in range(graph.size):
        if graph.matrix[i][i]:
            return False
        vertex_array.append(None)

    for i in range(graph.size):
        if vertex_array[i] != None:
            continue
        queue.append(i)

        while queue:
            current = queue.popleft()
            white = False
            black = False
            for j in range(graph.size):
                if graph.matrix[current][j]:
                    if vertex_array[j] == "White":
                        white = True
                        continue
                    if vertex_array[j] == "Black":
                        black = True
                    if vertex_array[j] == None:
                        queue.append(j)
            if black and white:
                return False
            if white:
                vertex_array[current] = "Black"
                continue
            vertex_array[current] = "White"
    return True

my_graph = Graph(4)

my_graph.matrix[0][1] = True
my_graph.matrix[1][0] = True
my_graph.matrix[1][3] = True
my_graph.matrix[2][3] = True
my_graph.matrix[3][1] = True
my_graph.matrix[3][2] = True

print(colourable(my_graph))

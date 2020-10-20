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
        vertex_array[i] = "White"
        queue.append(i)

        while queue:
            current = queue.popleft()
            if vertex_array[current] == "White":
                color = "Black"
            else:
                color = "White"

            for j in range(graph.size):
                if graph.matrix[current][j]:
                    if vertex_array[j] == None:
                        vertex_array[j] = color
                        queue.append(j)
                        continue
                    if vertex_array[j] != color:
                        return False
    return True


# Ukol 2.
# Implementujte funkci compute_dependencies, ktera pro zadany orientovany graf
# spocita topologicke usporadani vrcholu, tj. ocislovani vrcholu takove, ze
# kazda hrana vede z vrcholu s nizsim cislem do vrcholu s vyssim cislem.
#
# Vystupem je pole zadavajici topologicke usporadani (ocislovani vrcholu),
# kde na prvni pozici (tedy s indexem 0) je vrchol nejmensi
# v tomto usporadani, tj. nevede do nej zadna hrana,
# a na posledni pozici vrchol nejvetsi, tj. nevede z nej zadna hrana.
# Pokud topologicke usporadani neexistuje, algoritmus vraci None.
#
# Priklad:
#    mejme graf s vrcholy 0, 1, 2 a hranami 0 -> 1, 2 -> 1, 2 -> 0;
#    vystupem bude pole (Pythonovsky seznam] [2, 0, 1]

def compute_dependencies(graph):
    """Spocita topologicke usporadani vrcholu v grafu.
    Vstup:
        graph - orientovany graf typu Graph
    Vystup:
        pole cisel reprezentujici topologicke usporadani vrcholu
        None, pokud zadne topologicke usporadani neexistuje
    casova slozitost: O(n^2), kde n je pocet vrcholu grafu
    extrasekvencni prostorova slozitost: O(n), kde n je pocet vrcholu grafu
    """

    degree = []
    sorted_array = []
    visited = []
    queue = deque()
    for i in range(graph.size):
        degree.append(0)
        visited.append(False)

    for i in range(graph.size):
        for j in range(graph.size):
            if graph.matrix[i][j]:
                degree[j] += 1

    for i in range(graph.size):
        if degree[i] == 0:
            queue.append(i)
            visited[i] = True

    while queue:
        current = queue.popleft()
        sorted_array.append(current)
        for i in range(graph.size):
            if graph.matrix[current][i] and not visited[i]:
                degree[i] -= 1
                if degree[i] == 0:
                    queue.append(i)
                    visited[i] = True

    for i in range(graph.size):
        if degree[i] != 0:
            return None
    return sorted_array




"""TESTS
my_graph = Graph(4)

my_graph.matrix[0][1] = True
my_graph.matrix[1][0] = True
my_graph.matrix[1][3] = True
my_graph.matrix[2][3] = True
my_graph.matrix[3][1] = True
my_graph.matrix[3][2] = True
print(colourable(my_graph))
print(compute_dependencies(my_graph))
graph_1 = Graph(1)

graph_1.matrix[0][0] = False
print(colourable(graph_1))
print(compute_dependencies(graph_1))

graph_2 = Graph(3)
graph_2.matrix[0][1] = True
graph_2.matrix[0][2] = True
graph_2.matrix[1][0] = True
graph_2.matrix[1][2] = True
graph_2.matrix[2][0] = True
graph_2.matrix[2][1] = True
print(colourable(graph_2))
print(compute_dependencies(graph_2))
"""


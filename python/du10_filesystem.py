#!/usr/bin/env python3

# Povolene knihovny: math

# IB002 Domaci uloha 10.
#
# V tomto ukolu budete pracovat s obecnym korenovym stromem reprezentujicim
# hierarchii unixoveho souboroveho systemu. Uzly tvori adresare reprezentovane
# tridou Directory.
#
# Trida Directory predstavuje jeden adresar stromu a drzi si informaci o svych
# podadresarich pomoci Pythonovskeho slovniku (ten je implementovan jako
# hashovaci tabulka). Slovnik podadresaru nikdy neobsahuje polozky "" (prazdny
# retezec), "." (aktualni adresar), ".." (rodicovsky adresar).
# Vsimnete si, ze adresare si nedrzi sve vlastni nazvy.
#
# Ve vsech nasledujicich funkcich predpokladame, ze pracujeme nad jednou
# adresarovou strukturou.
#
# Dobre rady k pouzivani retezcu a slovniku v Pythonu:
#
# Pro rozdeleni retezce na seznam podretezcu podle znaku '/' pouzijte:
#     retezec.split('/')
#
# Pro zjisteni, zda retezec obsahuje zadany podretezec, pouzijte:
#     podretezec in retezec
#
# Pro zjisteni, zda slovnik obsahuje jako klic zadany retezec pouzijte:
#     retezec in slovnik
#
# Pro pristup k hodnote, ktera odpovida zadanemu klici ve slovniku, pouzijte:
#     slovnik[klic]
#     (pokud klic ve slovniku neni, skonci s chybou)
# nebo
#     slovnik.get(klic)
#     (pokud klic ve slovniku neni, vrati None)
#
# Pro pridani dvojice (klic, hodnota) do slovniku pouzijte:
#     slovnik[klic] = hodnota
#     (pokud klic neexistuje, vytvori se nova polozka slovniku,
#      v opacnem pripade se jen zmeni hodnota prirazena k danemu klici)
#
# Prochazeni vsech polozek (klic, hodnota) ze zadaneho slovniku:
# (nepouzivejte, pokud pouze chcete pristoupit k danemu klici, k tomu jsou
#  operatory a funkce uvedene vyse)
#     for klic, hodnota in slovnik.items(): ...
# pripadne pro prochazeni pouze klicu:
#     for klic in slovnik: ...
#
# Poznamka ohledne slozitosti:
# U vsech slozitostnich pozadavku v tomto ukolu ignorujeme slozitost prace se
# slovnikem a slozitost prace s retezci (ve skutecnosti je napr. porovnani
# retezcu, pocitani hashe retezce nebo hledani podretezce v retezci linearni
# vuci delce retezce).
#
# Dobra rada na zaver: Vhodne rozdeleni na pomocne funkce vam muze vyznamne
# usetrit praci.
#
# Nasledujici definici tridy Directory nemodifikujte.


class Directory:
    """Trida Directory reprezentuje jeden adresar v souborovem systemu.

    Atributy:
        parent: odkaz na nadrazeny adresar
        subdirectories: slovnik, v nemz klici jsou nazvy podadresaru aktualniho
            adresare a hodnotami jsou objekty typu Directory
    """
    __slots__ = ("parent", "subdirectories")

    def __init__(self):
        self.parent = None
        self.subdirectories = {}


# Ukol 1.
# Implementujte funkci cd. Ta bude simulovat prikaz cd slouzici ke zmene
# pracovniho adresare. Pro zjednoduseni budeme vzdy pouzivat jen relativni
# cesty, tj. takove, ktere nezacinaji znakem '/'.
#
# Retezec path popisuje cestu stromem, kde jednotlive klice jsou oddeleny
# znakem "/". Cesta muze obsahovat i polozky "." (aktualni adresar) a ".."
# (rodicovsky adresar(*)). Je zaruceno, ze path neni prazdny retezec, nezacina
# ani nekonci znakem '/' ani neobsahuje dva znaky '/' bezprostredne za sebou.
#
# (*) pritom dodrzujeme bezne uzivanou konvenci, ze pokud adresar nema rodice
# (tj. je korenem adresarove struktury), polozka ".." adresar nemeni
#
# Priklad:
# mejme tento strom adresaru:
#
#                         korenovy adresar
#                       /                  \
#                    "home"               "tmp"
#                      |                /       \
#                    "user"          "aaa"     "bbb"
#                      |               |       /    \
#                 "documents"        "aaa"  "ccc"  "ddd"
#
# Necht root je objekt, ktery odpovida korenovemu adresari. Potom:
# cd(root, ".") by vratilo korenovy adresar (root)
# cd(root, "..") by take vratilo korenovy adresar (viz poznamku vyse)
# cd(root, "home/../tmp") by vratilo podadresar korenoveho adresare s klicem
#     "tmp" (tedy root.subdirectories["tmp"])
# Pokud zadany adresar neexistuje, vracite None.
# Stejne tak vracite None, pokud neexistuje nektery z adresaru po ceste:
# napriklad cd(root, "xyz/..") nebo cd(root, "home/./home/user/documents")

def cd(current, path):
    """Vrati adresar, do nejz se dostaneme z adresare current po pruchodu
       cestou path.

    Vstup:
       current typu Directory -- aktualni adresar
       path -- neprazdny retezec s cestou
               nezacina ani nekonci znakem '/', neobsahuje dve '/' za sebou

    Casova slozitost: linearni vuci delce (poctu segmentu) zadane cesty
        (ale viz poznamku nahore o ignorovani slozitosti nekterych operaci)
    """

    splitted_path = path.split("/")

    for x in splitted_path:
        if x == ".":
            continue
        if x == "..":
            if current.parent is None:
                continue
            current = current.parent
            continue
        new_current = current.subdirectories.get(x)

        if new_current is None:
            return None
        current = new_current
    return current


# Ukol 2.
# Vasi dalsi ulohou bude implementovat funkci mkdirp. Ta bude simulovat prikaz
# mkdir s prepinacem -p. Prikaz mkdir ma za ukol vytvorit zadany adresar.
# Prepinac -p slouzi k tomu, aby v pripade neexistence adresaru v ceste byly
# tyto adresare vytvoreny.
# Pro string path plati totez, co ve funkci cd.
#
# Priklad:
# Necht root je opet objekt reprezentujici korenovy adresar hierarchie, ktera
# je na zacatku prazdna (tj. existuje jen tento adresar).
# Posloupnost prikazu:
# mkdirp(root, "home/user/documents")
# mkdirp(root, "tmp/bbb/../aaa/aaa")  # vytvori i "bbb"
# mkdirp(root, "tmp/bbb/./ccc")
# mkdirp(root, "tmp/bbb/ddd")
# vytvori strom z prvniho prikladu:
#
#                         korenovy adresar
#                       /                  \
#                    "home"               "tmp"
#                      |                /       \
#                    "user"          "aaa"     "bbb"
#                      |               |       /    \
#                 "documents"        "aaa"  "ccc"  "ddd"
#
# Nezapomente, ze je treba vytvorit vsechny adresare po ceste (adresar "bbb"
# vyse vznikl uz pri druhem volani mkdirp).
# V pripade, ze zadany adresar jiz existuje, nic neprovadite.

def mkdirp(current, path):
    """Vytvori vsechny adresare po zadane ceste ze zadaneho aktualniho
       adresare. Existujici adresare nechava v puvodnim stavu.

    Vstup:
       current typu Directory -- aktualni adresar
       path -- neprazdny retezec s cestou
               nezacina ani nekonci znakem '/', neobsahuje dve '/' za sebou

    Casova slozitost: linearni vuci delce (poctu segmentu) zadane cesty
        (ale viz poznamku nahore o ignorovani slozitosti nekterych operaci)
    """
    if current is None:
        current = Directory()
    splitted_path = path.split("/")

    for x in splitted_path:
        if x == ".":
            continue
        if x == "..":
            if current.parent is None:
                continue
            current = current.parent
            continue
        new_current = current.subdirectories.get(x)

        if new_current is None:
            new_directory = Directory()
            new_directory.parent = current
            current.subdirectories[x] = new_directory
            current = new_directory
            continue
        current = new_current


# Ukol 3.
# Naimplementujte funkci find. Ta vrati seznam vsech adresaru v podstrome danem
# aktualnim adresarem, ktere ve svem nazvu obsahuji zadany retezec. (Do toho se
# samozrejme nepocita aktualni adresar, protoze ten sve jmeno nezna.)
#
# Priklad: pro root z ukolu 1 a retezec "me" vrati seznam adresaru (objektu
# typu Directory), ktere odpovidaji polozkam "home" a "documents".
#
# Priklad: pokud bychom jako prvni parametr zadali objekt reprezentujici
# adresar "home" (z ukolu 1) a vyhledavany retezec by byl "o", vrati funkce
# seznam s jednim objektem reprezentujicim adresar "documents".
#
# Poradi adresaru ve vyslednem seznamu neni dulezite.


def find(current, pattern):
    """Najde vsechny adresare v podstrome danem aktualnim adresarem,
       jejichz jmena obsahuji zadany retezec.

    Vstup:
       current typu Directory -- aktualni adresar
       pattern -- vyhledavany podretezec, neobsahuje znak '/', ale muze byt
                  i prazdny (pak zadani splnuji vsechny podadresare ve strome)

    Casova slozitost: linearni vuci velikosti podstromu aktualniho adresare
        (ale viz poznamku nahore o ignorovani slozitosti nekterych operaci)
    """

    my_array = []
    find_rec(current, pattern, my_array)
    return my_array


def find_rec(current, pattern, array):
    """if current.subdirectories == {}:
        return"""
    for key in current.subdirectories:
        if pattern in key:
            array.append(current.subdirectories[key])
        find_rec(current.subdirectories[key], pattern, array)


# Pomocna funkce make_graph vygeneruje .dot soubor s adresarovou strukturou
# s korenem zadanym jako prvni argument funkce.
#
# Na vygenerovany soubor si bud najdete nastroj, nebo pouzijte odkazy:
# http://sandbox.kidstrythisathome.com/erdos/ nebo http://www.webgraphviz.com/
# Staci zkopirovat obsah souboru do formulare webove stranky.

def make_graph(root, filename="fs.dot"):
    with open(filename, "w") as f:
        f.write("digraph FileSystem {\n")
        f.write("node [color=lightblue2, style=filled]\n")
        dot_subdir(root, f)
        f.write("}\n")


def dot_subdir(directory, f, name="/"):
    f.write('"{}" [label="{}"]\n'.format(id(directory), name))

    for subname, subdir in directory.subdirectories.items():
        f.write('"{}" -> "{}"\n'.format(id(directory), id(subdir)))
        dot_subdir(subdir, f, subname)


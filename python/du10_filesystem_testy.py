import du10_filesystem as du


def testy():
    root = du.Directory()
    root.subdirectories["home"] = du.Directory()
    root.subdirectories["home"].parent = root
    root.subdirectories["home"].subdirectories["user"] = du.Directory()
    root.subdirectories["home"].subdirectories["user"].parent = root.subdirectories["home"]
    root.subdirectories["home"].subdirectories["user"].subdirectories["documents"] = du.Directory()
    root.subdirectories["home"].subdirectories["user"].subdirectories["documents"].parent =\
        root.subdirectories["home"].subdirectories["user"]                                                                     
    root.subdirectories["tmp"] = du.Directory()
    root.subdirectories["tmp"].parent = root
    root.subdirectories["tmp"].subdirectories["aaa"] = du.Directory()
    root.subdirectories["tmp"].subdirectories["aaa"].parent = root.subdirectories["tmp"]
    root.subdirectories["tmp"].subdirectories["aaa"].subdirectories["aaa"] = du.Directory()
    root.subdirectories["tmp"].subdirectories["aaa"].subdirectories["aaa"].parent =\
        root.subdirectories["tmp"].subdirectories["aaa"]                                                                       
    root.subdirectories["tmp"].subdirectories["bbb"] = du.Directory()
    root.subdirectories["tmp"].subdirectories["bbb"].parent = root.subdirectories["tmp"]
    root.subdirectories["tmp"].subdirectories["bbb"].subdirectories["ccc"] = du.Directory()
    root.subdirectories["tmp"].subdirectories["bbb"].subdirectories["ccc"].parent =\
        root.subdirectories["tmp"].subdirectories["bbb"]
    root.subdirectories["tmp"].subdirectories["bbb"].subdirectories["ddd"] = du.Directory()
    root.subdirectories["tmp"].subdirectories["bbb"].subdirectories["ddd"].parent =\
        root.subdirectories["tmp"].subdirectories["bbb"]

    du.make_graph(root)
    
    test1(root)
    test2(root)
    test3(root)
    test4(root)
    test5(root)
    test6(root)
    test7()
    test8(root)
    test9(root)
    test10(root)


def test1(root):
    test = du.cd(root, ".")
    vzor = root

    print(("OK" if test == vzor else "ERROR") + " 1")


def test2(root):
    test = du.cd(root, "..")
    vzor = root

    print(("OK" if test == vzor else "ERROR") + " 2")


def test3(root):
    test = du.cd(root, "home/../tmp")
    vzor = root.subdirectories["tmp"]

    print(("OK" if test == vzor else "ERROR") + " 3")


def test4(root):
    test = du.cd(root, "home/../tmp/aaa/aaa")
    vzor = root.subdirectories["tmp"].subdirectories["aaa"].subdirectories["aaa"]

    print(("OK" if test == vzor else "ERROR") + " 4")


def test5(root):
    test = du.cd(root, "home/../tmp/aaa/aaa/aaa")
    vzor = None

    print(("OK" if test == vzor else "ERROR") + " 5")


def test6(root):
    test = du.cd(root, "home/user/documents/../../../tmp/aaa/aaa/../../bbb/ccc/../ddd/../../..")
    vzor = root

    print(("OK" if test == vzor else "ERROR") + " 6")


def test7():
    vzor = du.Directory()
    
    du.mkdirp(vzor, "home/user/documents")
    du.mkdirp(vzor, "tmp/bbb/../aaa/aaa")
    du.mkdirp(vzor, "tmp/bbb/./ccc")
    du.mkdirp(vzor, "tmp/bbb/ddd")
    
    test = du.cd(vzor, "home/user/documents/../../../tmp/aaa/aaa/../../bbb/ccc/../ddd/../../..")

    print(("OK" if test == vzor else "ERROR") + " 7")


def test8(root):
    test = du.find(root, "me")
    vzor = [root.subdirectories["home"], root.subdirectories["home"].subdirectories["user"].\
            subdirectories["documents"]]

    print(("OK" if test == vzor else "ERROR") + " 8")


def test9(root):
    test = du.find(root, "")
    vzor = [root.subdirectories["home"], root.subdirectories["home"].subdirectories["user"].\
            subdirectories["documents"]]

    print(("OK" if test == vzor else "ERROR") + " 9")


def test10(root):
    test = du.find(root, "dfthvtrfdhctrhctrh")
    vzor = []

    print(("OK" if test == vzor else "ERROR") + " 10")

testy()

def exemple1():
    import subprocess as sp
    
    if __name__ != "__main__":
        print("loading subprocess", end=" ... ")
    
    res = sp.run(["dir", "/b"], capture_output=True, shell=True, text=True, encoding="UTF-8")
    if res.returncode:
        print(f"Erreur de commande :\n({res.returncode}) {res.stderr}")
    else:
        print(res.stdout)


def make2Darray(x, y):
    return [([0] * x)[:] for i in range(y)]


def makeNDarray(*args, **kvargs):
    
    res = kvargs.get("init", 0)
    for dimension in args:
        if not type(res) == list:
            res = [res for i in range(dimension)]
        else:
            res = [res.copy() for i in range(dimension)]
    return res


def exemple2():
    t = make2Darray(5, 3)
    print(t)
    t[1][1] += 2
    print(t)


def exemple3():
    n = makeNDarray(5, 3, 2)
    n[1][1][1] += 2
    print(n)

from xml.dom.minidom import Element
def exemple4():
  for a in dir(Element):
    if not callable(getattr(Element, a)) and not a.startswith("__"):
      print(f"{a}")

  for a in dir(Element):
    if callable(getattr(Element, a)) and not a.startswith("__"):
      print(f"{a}()")


exemple4()

if __name__ != "__main__":
    print("ok")

input("")
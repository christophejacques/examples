def test(valeur):
    match valeur.split(":"):
        case ["1", *reste]:
            print("<1", reste)

        case ["2"]:
            print(">2")

        case ["3", reste]:
            print("3, Reste:", reste)

        case [code, reste]:
            print("code:", code, reste)

        case valeur if valeur[0][0] == "5":
            print("=>", valeur)

        case autre:
            print(autre)


def main1():
    test("1:Un:One")
    test("2")
    test("3:dfxsdf")
    test("4:dfxsdf")
    test("5Cinq")
    test("6Six")


class Define:

    def __init__(self, fonction):
        print("fonction:", fonction)
        Define.fonction = fonction

    def __call__(self, *args):
        print("call")
        return Define.fonction(*args)

    def ajouter(self):
        print("Define:")

        def params(*args, **kwargs):
            print("Define params:", args)
            return Define.fonction(*args)

        return params

  

def define(fonction):
    print("*fonction*:", fonction.__name__)
    def parametres(*args, **kwargs):
        print("*params*:", *args, **kwargs)
        return fonction(*args, **kwargs)
    return parametres



@define
def sub(a, b):
    print("*define*")
    return a-b

@Define
def add(a, b):
    print("originale")
    return a+b

@Define.ajouter
def aj(a: int, b: int) -> int:
    print("copie 1")
    return a+b

@Define.ajouter
def aj(a: str, b: str) -> str:
    print("copie 2")
    return a+"+"+b

# print(add(1, 2))
print(aj(3, 4))
print(aj("3", "4"))

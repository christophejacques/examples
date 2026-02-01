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
            print("if =>", valeur)

        case autre:
            print("default:", autre)


def main1():
    test("1:Un:One")
    test("2")
    test("3:dfxsdf")
    test("4:dfxsdf")
    test("5Cinq")
    test("6Six")

main1()

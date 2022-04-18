from winreg import QueryValueEx, OpenKeyEx, ConnectRegistry, HKEY_LOCAL_MACHINE
from winreg import EnumKey, EnumValue

une_cle = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WDDiscovery"
# une_cle = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# une_cle = r"SOFTWARE\Microsoft\Windows\CurrentVersion"


def title(titre):
    print(titre.title())
    print("-" * len(titre))


def liste_registry(fonction, cle):
    title(f"get {fonction.__name__} :")

    try:
        i = 0
        while True:
            print("", i, fonction(cle, i))
            i += 1
    except OSError:
        if i > 0: 
            print()
        return True
    except Exception as e:
        print(e)
        return False


def get_key(registre, cle):
    title(f"get Query {registre}\\{cle} :")
    try:
        root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKeyEx(root, registre)
        res = QueryValueEx(key, cle)[0]
        print(res)

    except OSError:
        return True
    except Exception as e:
        print("error:", e)


with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as HK:
    # print(une_cle)
    *registre, cle = une_cle.split("\\")
    try:
        key = OpenKeyEx(HK, une_cle)
        if liste_registry(EnumKey, key) and liste_registry(EnumValue, key):
            pass
    except Exception:
        pass

    registre_parent = "\\".join(registre)
    if get_key(registre_parent, cle):
        pass


if __name__ == "__main__":
    pass

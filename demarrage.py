#! /usr/bin/env python3

from winreg import ConnectRegistry
from winreg import HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, OpenKeyEx, OpenKey, EnumValue, EnumKey, HKEY_USERS
# from winreg import QueryValueEx,
from os import scandir, environ
import platform


def get_keys(proot, pkey_string):
    results = []
    try:
        root = ConnectRegistry(None, proot)
        policy_key = OpenKey(root, pkey_string)
        
        i = 0
        while True:
            try:
                cle = EnumKey(policy_key, i)
                results.append(cle)
                i += 1
            except OSError:
                break

    except OSError as ose2:
        print("OSError2:", ose2)
        pass
    except Exception as e:
        print("Error:", e)

    return results


def root_string(root):
    return {
        HKEY_LOCAL_MACHINE: "HKLM\\",
        HKEY_CURRENT_USER: "HKCU\\",
        HKEY_USERS: "HKU\\",
    }[root]


def print_souligne(sigle, texte):
    print(texte)
    print(sigle * len(texte))


def print_all_registry_keys(root_key, key_string):
    try:
        root = ConnectRegistry(None, root_key)
        policy_key = OpenKeyEx(root, key_string)
        print_souligne("-", root_string(root_key) + key_string)
        i = 0
        while True:
            try:
                cle, valeur, *args = EnumValue(policy_key, i)
                print("  -", cle, ":", valeur)
                i += 1
            except OSError:
                break

    except OSError:
        pass
    except Exception as e:
        print("Error:", e)
    else:
        print()


def print_all_directory_files(repertoire):
    print_souligne("-", repertoire)
    try:
        with scandir(repertoire) as liste_fichiers:
            for f in liste_fichiers:
                if f.name != "desktop.ini":
                    print("  -", f.name)
    except Exception as e:
        print("Error:", e)
    print()


def liste_users():
    for cle in get_keys(HKEY_USERS, ""):
        print_all_registry_keys(HKEY_USERS, cle + r"\SOFTWARE\Microsoft\Windows\CurrentVersion\Run")

    print()


def main():
    titre = f"Applications démarrées pour : {environ['USERNAME']}"
    print_souligne("=", titre)

    print_all_registry_keys(HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")

    print_all_registry_keys(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")

    print_all_directory_files(
        "{}\\{}".format(environ.get("ProgramData", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"))
    print_all_directory_files(
        "{}\\{}".format(environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"))

    titre = "Applications démarrées pour différents utilisateurs"
    print_souligne("=", titre)
    liste_users()


if __name__ == "__main__":
    if platform.system() == "Windows":
        main()
    else:
        print("Ne fonctionne que sur une platefome Windows")

# input()

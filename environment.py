import sys
import os


def getdirs(repertoire):
    dirs = []
    files = []
    try:
        for fichier in os.scandir(repertoire):
            if fichier.is_dir():
                if os.path.exists(os.path.join(repertoire, fichier.name, "__init__.py")):
                    dirs.append(fichier.name)

            elif fichier.name.endswith(".py"):
                files.append(fichier.name)

        print("-", repertoire, "(", len(dirs) + len(files), ")")
        for rep in sorted(dirs):
            print(f"    /{rep}")
        for file in sorted(files):
            print(f"    > {file}")
        print()

    except NotADirectoryError:
        pass


if True:
    print("Liste des modules :")
    for module in sorted(sys.modules):
        if module[0] != "_":
            print("-", f"{module:20} :", sys.modules[module])

if sys.version_info[:2] < (3, 10):
    print("Veuillez vérifier que vous utilisez la version 3.10 de python")
    exit(1)

print("Current diretory:", os.getcwd())
print("Version de Python:", sys.version)

print("\nRecherche des modules :")
for chemin in filter(lambda x: not x.endswith(".zip"), sys.path):
    getdirs(chemin)

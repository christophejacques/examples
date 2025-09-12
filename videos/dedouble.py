# ! c:\bat\python.bat -3.10
import os
import math

mesure: list = ["o", "Ko", "Mo", "Go", "To", "Po", "??"]


def human_readable_size(x, nombre_decimales: int = 2) -> str:
    puissance: int = int(math.log(x, 1024)) if x > 0 else 0
    # valeur: float = round(x/(1024**puissance)*10**nombre_decimales)/10**nombre_decimales
    valeur: float = x/(1024**puissance)
    return f"{valeur:.2f} {mesure[puissance]}"


movie: tuple = ("mpg", "avi", "mp4", "mkv", "wmv")
picture: tuple = ("jpg", "jpeg", "png", "gif", "bmp", "")

repertoires: list = [
    r"F:\Videos\Japan",
    r"D:\Mes Documents\dwhelper", 
    r"D:\Mes Documents\dwhelperold", 
]
files: dict = {}


def scandir(repertoire) -> None:
    
    with os.scandir(repertoire) as contenu:
        for f in contenu:
            if f.is_dir():
                scandir(f.path)

            elif not f.is_file():
                continue

            *lst_nom, extension = f.name.lower().split(".")
            nom: str = " ".join(lst_nom)
            if extension not in movie:  # + picture:
                continue

            identifiant, *_ = nom.replace("_", " ").split()
            if "-" not in identifiant:
                continue

            code, numero, *_ = identifiant.strip("[]").split("-")
            if not numero.isnumeric():
                continue

            cle: str = f"{code.upper()}-{numero}"
            if not files.get(cle):
                files[cle] = []
            files[cle].append((f.stat().st_size, f.path))


error: bool = False
for repertoire in repertoires:
    if not os.path.isdir(repertoire):
        error = True
        print(f"Repertoire inexistant: {repertoire}")

if error:
    exit()

for repertoire in repertoires:
    scandir(repertoire)


nb_doublons: int = 0
for cle in sorted(files):
    if len(files[cle]) <= 1:
        continue
    nb_doublons += 1
    print(cle)
    for size, file in sorted(files[cle], key=lambda x: x[1]):
        try:
            print(f"  {human_readable_size(size):>10} -", file[:130])
        except UnicodeEncodeError:
            print(file[:file.rindex("\\")], "..")
            # print("UnicodeEncodeError")
        except Exception as error:
            print(error)

print(f"\n{nb_doublons} doublons trouves.")

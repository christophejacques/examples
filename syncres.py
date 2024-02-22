import os
import sys
import datetime
import ctypes
import time


def eprint(*args):
    print(*args, end="")


def convertir_time(file_time):
    """
    Convertit l'attribut st_atime d'un fichier en date et heure.

    Args:
        file_time: float representant la datetime d'un fichier.

    Returns:
        Un tuple contenant la date et l'heure sous forme de (année, mois, jour, heure, minute, seconde).
    """

    # Convertir le timestamp en secondes depuis l'époque Unix en datetime
    dt = datetime.datetime.fromtimestamp(file_time)

    # Extraire les différents champs de la date et de l'heure
    annee = dt.year
    mois = dt.month
    jour = dt.day
    heure = dt.hour
    minute = dt.minute
    seconde = dt.second

    return annee, mois, jour, heure, minute, seconde


def get_newest_file(directory):
    """
    Recupere le fichier le plus recent d'un repertoire.

    Args:
        repertoire contenant des fichiers a rechercher

    Returns:
        fichier le plus recent : DirEntry
    """
    print("Scanning", directory)

    last_file: os.DirEntry 
    last_time: float = 0.0

    files = os.scandir(directory)
    for file in files:
        if not file.is_file():
            continue

        file_time = file.stat().st_mtime
        # print(file.name, file_time)
        if file_time < last_time:
            continue

        last_time = file_time
        last_file = file

    return last_file


def aide():
    print("Le seul parametre autorisé est : --report")


def main():
    if len(os.sys.argv) == 2 and os.sys.argv[1].lower() != "--report":
        aide()
        return

    time.sleep(2)
    directory = os.environ["APPDATA"] + r"\FreeFileSync\Logs"
    file = get_newest_file(directory)

    if len(os.sys.argv) == 1:
        print("{:04}-{:02}-{:02} {:02}:{:02}:{:02} -".format(*convertir_time(file.stat().st_mtime)), file.name)
        
    elif os.sys.argv[1].lower() == "--report":
        # Définir la fonction ShellExecute
        ShellExecute = ctypes.windll.shell32.ShellExecuteW

        # Ouvrir le fichier HTML dans Firefox
        ShellExecute(0, "open", f"{directory}\\{file.name}", None, None, 0)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        aide()
    else:
        main()

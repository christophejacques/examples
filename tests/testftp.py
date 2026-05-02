import os
from VARIABLES_ENV import Coffre
from myftp import MyFTP


# Informations de connexion à votre serveur FTP
hostname = "test.rebex.net"
username = "demo"
password = Coffre.get_password(hostname, username)


def download():
    nb_files: int = 0
    copied_files: int = 0
    directory = ftp.pwd()

    if ftp.debug:
        print(directory, flush=True)

    for fichier in ftp.fichiers:
        if os.path.exists(f"./ftp/{fichier}"):
            # le fichier existe deja donc on ne le re-telecharge pas
            continue

        copied_files += 1

        if ftp.debug:
            print("Downloading:", f"{directory}/{fichier}", flush=True, end=" ... ")

        if ftp.getfile(directory, f"{fichier}", f"./ftp/{fichier}", show=False):
            if ftp.debug:
                print("Done")

    nb_files = len(ftp.fichiers)
    if nb_files == 0:
        print("- Aucun fichier trouvé.")
    elif copied_files < 2:
        print(f"- {copied_files} fichier copié sur {nb_files}.")
    else:
        print(f"- {copied_files} fichiers copiés sur {nb_files}.")


if __name__ == "__main__":
    with MyFTP(hostname, username, password, welcome=False, debug=False) as ftp:
        ftp.scan("/", callback=download)

import os
# from VARIABLES_ENV import password
from myftp import MyFTP


# Informations de connexion à votre serveur FTP
hostname = "test.rebex.net"
username = "demo"
password = "password"

remote_path = "/"  # Chemin du dossier de destination sur le serveur


def download():
    directory = ftp.pwd()
    print(directory)
    for fichier in ftp.fichiers:
        if os.path.exists(f"./ftp/{fichier}"):
            # le fichier existe deja donc on ne le re-telecharge pas
            continue

        print("Downloading:", f"{directory}/{fichier}", flush=True, end=" ... ")
        if ftp.getfile(directory, f"{fichier}", f"./ftp/{fichier}", show=False):
            print("Done")


with MyFTP(hostname, username, password) as ftp:
    ftp.scan("/", callback=download, show=False)

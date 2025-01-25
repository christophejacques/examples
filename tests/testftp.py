import os
from ftplib import FTP

# Informations de connexion à votre serveur FTP
hostname = "perso.numericable.com"
username = "cjacques"
password = "pleinne1"
remote_path = "/"  # Chemin du dossier de destination sur le serveur
local_file = "mon_fichier.txt"


def fprint(*args):
    print(*args, flush=True)

def sendfile(hostname, remote_path, local_file, username, password):
    # Connexion au serveur FTP
    with FTP(hostname) as ftp:
        fprint("login", username)
        ftp.login(username, password)

        fprint(f"ftp.cwd({remote_path})")
        # Changement de répertoire sur le serveur (si nécessaire)
        ftp.cwd(remote_path)

        # Envoi du fichier
        fprint(f"ftp.storbinary({'STOR ' + local_file})")
        with open(local_file, 'rb') as f:
            ftp.storbinary('STOR ' + local_file, f)

        fprint("Fichier envoyé avec succès !")


def getfile(hostname, remote_path, remote_file, local_file, username, password):

    if os.path.exists(local_file):
        os.remove(local_file)

    fichier_recupere: bool = False
    # Connexion au serveur FTP
    with FTP(hostname) as ftp:
        fprint("login", username)
        ftp.login(username, password)

        fprint(f"ftp.cwd({remote_path})")
        # Changement de répertoire sur le serveur (si nécessaire)
        ftp.cwd(remote_path)

        # Envoi du fichier
        fprint(f"ftp.retrbinary({'RETR ' + local_file})")
        with open(local_file, 'wb') as f:
            try:
                ftp.retrbinary('RETR ' + remote_file, f.write)
                fichier_recupere = True
            except Exception as erreur:
                fprint(erreur)
        
        if fichier_recupere:
            fprint("Fichier téléchargé avec succès !")
        else:
            os.remove(local_file)


# sendfile(hostname, remote_path, local_file, username, password)
getfile(hostname, remote_path, local_file, local_file, username, password)

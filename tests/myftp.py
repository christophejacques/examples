import os
import math
from ftplib import FTP
from VARIABLES_ENV import password


multi: list[str] = ["o ", "Ko", "Mo", "Go", "To", "Po", "??"]

# Informations de connexion à votre serveur FTP
hostname = "perso.numericable.com"
username = "cjacques"

local_file = "mon_fichier.txt"


def fprint(*args, **kwargs):
    print(*args, flush=True, **kwargs)

def int2human(size_str: str) -> str:
    size: int = int(size_str)
    logarithme: int = int(math.log2(size) // 10)
    return f"{size / 1024 ** logarithme:,.2f} {multi[logarithme]}"

def readable_date(date_param: str) -> str:
    return (date_param[:4] + "-" + date_param[4:6] + "-" + date_param[6:8] + " " + 
        date_param[8:10] + ":" + date_param[10:12] + ":" + date_param[12:])

class MyFTP:

    def __init__(self, hostname, username, password):
        fprint("Connecting to:", hostname, end=" ... ")
        self.ftp = FTP(hostname)
        self.ftp.login(username, password)
        fprint("Done.")

        welcome = self.ftp.getwelcome()
        if welcome:
            fprint(welcome)

        self.dirs: list = list()
        self.files: list = list()
        self.sizes: list = list()
        self.datem: list = list()

    def __enter__(self, *args):
        # fprint("enter:", args)
        return self

    def __exit__(self, param1, param2, traceback):
        if param1:
            fprint("exit:", param2)
        self.close()

    def scan(self, chemin: str, level: int=0) -> None:
        rep: str

        self.cd(chemin)
        self.getliste()

        liste_dirs: list = self.dirs.copy()
        while liste_dirs:
            rep = liste_dirs.pop(0)
            level += 1
            self.scan(f"{chemin}/{rep}", level)
            level -= 1

        if level == 0:
            self.cd(chemin)

    def getliste(self):
        self.dirs.clear()
        self.files.clear()
        self.sizes.clear()
        self.datem.clear()

        fprint("List content:")
        max_filename_size: int = 0
        for fichier in self.ftp.mlsd(facts=["type"]):
            file_name, file_type = fichier

            match file_type.get("type", None):
                case "dir":
                    self.dirs.append(file_name)
                case "file":
                    if len(file_name) > max_filename_size:
                        max_filename_size = len(file_name)
                    self.files.append(file_name)
                    self.sizes.append(f"{int2human(file_type.get("size", 0)):>12}")
                    self.datem.append(file_type.get("modify", ""))

        fprint("Dirs:", self.dirs)
        fprint("Files:")
        for index, file_name in enumerate(self.files):
            print(f"- {readable_date(self.datem[index])}  {file_name:{max_filename_size}} {self.sizes[index]}")

    def close(self):
        if self.ftp:
            self.ftp.close()
            fprint("Connection closed.")

    def dir(self, remote_path):
        current_path = self.pwd()
        self.cd(remote_path)
        fprint("dir")
        self.ftp.dir(fprint)
        self.cd(current_path, show=False)

    def md(self, remote_path):
        fprint("md", remote_path, end=" ... ")
        self.ftp.mkd(remote_path)
        fprint("done.")

    def cd(self, remote_path, show: bool=True):
        if show:
            fprint("cd", remote_path)
        self.ftp.cwd(remote_path)

    def rd(self, remote_path):
        fprint("rd", remote_path, end=" ... ")
        self.ftp.rmd(remote_path)
        fprint("done.")

    def pwd(self):
        return self.ftp.pwd()

    def ren(self, from_name, to_name):
        self.ftp.rename(from_name, to_name)

    def sendfile(self, remote_path, local_file):
        # Changement de répertoire sur le serveur (si nécessaire)
        self.cd(remote_path)

        # Envoi du fichier
        fprint(f"ftp.storbinary({'STOR ' + local_file})")
        with open(local_file, 'rb') as file:
            self.ftp.storbinary('STOR ' + local_file, file)

        fprint("Fichier envoyé avec succès !")

    def getfile(self, remote_path, remote_file, local_file):
        if os.path.exists(local_file):
            os.remove(local_file)

        fichier_recupere: bool = False

        # Changement de répertoire sur le serveur (si nécessaire)
        self.cd(remote_path)

        # Envoi du fichier
        fprint(f"ftp.retrbinary({'RETR ' + local_file})")
        with open(local_file, 'wb') as file:
            try:
                self.ftp.retrbinary('RETR ' + remote_file, file.write)
                fichier_recupere = True
            except Exception as erreur:
                fprint(erreur)
        
        if fichier_recupere:
            fprint("Fichier téléchargé avec succès !")
        else:
            os.remove(local_file)


if __name__ != "__main__":
    exit()
    
with MyFTP(hostname, username, password) as my_ftp:
    # my_ftp.getliste()
    my_ftp.scan("/ASP")

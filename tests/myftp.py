import os
import math
from ftplib import FTP
from VARIABLES_ENV import Coffre
from typing import Optional


multi: list[str] = ["o ", "Ko", "Mo", "Go", "To", "Po", "??"]


def fprint(*args, **kwargs):
    print(*args, flush=True, **kwargs)


def eprint(*args, **kwargs):
    print(*args, end="", **kwargs)


def int2human(size_str: str) -> str:
    size: int = int(size_str)
    logarithme: int = int(math.log2(size) // 10)
    return f"{size / 1024 ** logarithme:,.2f} {multi[logarithme]}"


def readable_date(date_param: str) -> str:
    return (date_param[:4] + "-" + date_param[4:6] + "-" + date_param[6:8] + " " + 
        date_param[8:10] + ":" + date_param[10:12] + ":" + date_param[12:])


class MyFTP:
    OPTIONS: list[str] = ["welcome", "debug"]

    def __init__(self, hostname, username, password, **options):

        for option in options:
            if option not in MyFTP.OPTIONS:
                raise Exception(f"Option {option!r} inconnue.")

        self.debug: bool = options.get("debug", True)

        if self.debug:
            fprint("Initialising FTP", end=" ... ")
        self.ftp = FTP(timeout=5)

        if self.debug:
            eprint("connecting to:", hostname, " ... ", flush=True)
        self.ftp.connect(hostname)

        if self.debug:
            eprint(f"login with {username!r} ... ", flush=True)
        self.ftp.login(username, password)

        if self.debug:
            fprint("Done.")

        if self.debug:
            reponse = self.ftp.sendcmd("SYST")
            if reponse:
                fprint(f"Serveur : {reponse}")
        
        if options.get("welcome", True):
            welcome_message = self.ftp.getwelcome()
            if welcome_message:
                fprint(welcome_message)

        self.dirs: list = list()
        self.fichiers: dict = dict()
        self.nb_dirs: int = 0
        self.nb_files: int = 0
        self.size_files: int = 0

    def __enter__(self, *args):
        return self

    def __exit__(self, param1, param2, traceback):
        if param1:
            fprint("exit:", param2)
        self.close()

    def scan(self, chemin: str = "", level: int = 0, callback=None, 
      show: Optional[bool] = None) -> None:
        rep: str

        if show is None:
            show = self.debug

        if level == 0:
            self.nb_dirs = 0
            self.nb_files = 0
            self.size_files = 0

        self.getliste(chemin, show=show)

        liste_dirs: list = self.dirs.copy()
        self.nb_dirs += len(liste_dirs)
        self.nb_files += len(self.fichiers)

        for nom, attr in self.fichiers.items():
            self.size_files += int(attr.get("size", 0))

        if callback:
            callback()

        while liste_dirs:
            rep = liste_dirs.pop(0)
            level += 1
            self.scan(f"{chemin}/{rep}", level, callback=callback, show=show)
            level -= 1

        if level == 0:
            self.cd(chemin, show)
            if show:
                fprint(f"{self.nb_dirs} répertoire(s) et {self.nb_files} fichier(s) pour :", 
                    int2human(str(self.size_files)))

    def getliste(self, remote_path: str = "/", show: Optional[bool] = None):
        self.dirs.clear()
        self.fichiers.clear()

        if show is None:
            show = self.debug

        self.cd(remote_path, show)

        if False:
            lignes: list = list()
            self.ftp.dir(lignes.append)
            for ligne in lignes:
                fprint("*", ligne)

        if show:
            fprint("List content:")
        max_filename_size: int = 0
        # for fichier in self.ftp.mlsd(facts=["type", "size", "perm", "modify"]):
        for fichier in self.ftp.mlsd():
            file_name, file_type = fichier
            # fprint("->", fichier)

            match file_type.get("type", None):
                case "dir":
                    self.dirs.append(file_name)

                case "file":
                    if len(file_name) > max_filename_size:
                        max_filename_size = len(file_name)

                    self.fichiers[file_name] = {}
                    self.fichiers[file_name]["size"] = file_type.get("size", 0)

                    # recuperation de la date de modification
                    # sinon la date de creation
                    date_modif = file_type.get("modify", 
                        file_type.get("create", 
                        self.ftp.voidcmd(f"MDTM {file_name}")[4:].strip()))

                    self.fichiers[file_name]["date"] = date_modif

        if not show:
            return

        fprint("Dirs:", self.dirs)
        fprint("Files:")
        for fichier in sorted(self.fichiers):
            fprint(f"- {readable_date(self.fichiers[fichier]["date"])}", end=" ")
            fprint(f"{int2human(self.fichiers[fichier]["size"]):>10} {fichier}")

    def close(self):
        if self.ftp:
            self.ftp.close()

            if self.debug:
                fprint("Connection closed.")

    def dir(self, remote_path):
        current_path = self.pwd()
        self.cd(remote_path)
        fprint("dir")
        self.ftp.dir(fprint)
        self.cd(current_path, show=False)

    def md(self, remote_path) -> str:
        if self.debug:
            fprint("md", remote_path, end=" ... ")
        path = self.ftp.mkd(remote_path)
        if self.debug:
            fprint("done.")
        return path

    def cd(self, remote_path, show: bool = True):
        if show:
            fprint("cd", remote_path)
        self.ftp.cwd(remote_path)

    def rd(self, remote_path):
        if self.debug:
            fprint("rd", remote_path, end=" ... ")
        self.ftp.rmd(remote_path)
        if self.debug:
            fprint("done.")

    def pwd(self):
        return self.ftp.pwd()

    def ren(self, from_name, to_name):
        self.ftp.rename(from_name, to_name)

    def delete(self, file_name):
        self.ftp.delete(file_name)

    def sendfile(self, remote_path, local_file):
        # Changement de répertoire sur le serveur (si nécessaire)
        self.cd(remote_path)

        # Envoi du fichier
        if self.debug:
            fprint(f"ftp.storbinary({'STOR ' + local_file})")
        with open(local_file, 'rb') as file:
            self.ftp.storbinary('STOR ' + local_file, file)

        if self.debug:
            fprint("Fichier envoyé avec succès !")

    def getfile(self, remote_path, remote_file, local_file=None, show: bool = True) -> bool:
        if local_file is None:
            local_file = remote_file

        if os.path.exists(local_file):
            os.remove(local_file)

        fichier_recupere: bool = False

        # Changement de répertoire sur le serveur (si nécessaire)
        if self.pwd != remote_path:
            self.cd(remote_path, show=show)

        # Recuperation du fichier
        if show:
            fprint(f"ftp.retrbinary({'RETR ' + remote_file})")

        with open(local_file, 'wb') as file:
            try:
                self.ftp.retrbinary('RETR ' + remote_file, file.write)
                fichier_recupere = True
            except Exception as erreur:
                fprint(erreur)
        
        if fichier_recupere:
            if show:
                fprint("Fichier téléchargé avec succès !")
            return True

        else:
            os.remove(local_file)
            return False


def main():
    # Informations de connexion à votre serveur FTP
    hostname = "test.rebex.net"
    username = "demo"
    password = Coffre.get_password(hostname, username)

    with MyFTP(hostname, username, password, welcome=False, debug=True) as my_ftp:
        my_ftp.scan("/pub")
        # my_ftp.getliste()
        # my_ftp.getliste("/pub/example")
        # my_ftp.getfile("/", "readme.txt", "./ftp/readme.txt")


if __name__ == "__main__":
    main()

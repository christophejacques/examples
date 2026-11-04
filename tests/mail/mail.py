import email
import imaplib
import re
import json
import binascii

from email.header import decode_header
from email.utils import parsedate_to_datetime
from typing import Optional, Dict, List, Generator

from general import Unique


class MailConfig(Unique):

    configs: List[Dict]

    IMAP_SERVER: str = ""
    USERNAME: str = ""
    PASSWORD: str = ""

    selected: int = 0

    def read_config_json(self) -> None:
        # Get Configuration JSon File
        with open("ENVIRONNEMENT") as env:
            configs = json.load(env)
            self.configs = sorted(configs, key=lambda cfg: cfg["USERNAME"])

    def set_config(self, ident: int = 0) -> None:
        self.selected = ident
        config = self.configs[ident]
        self.IMAP_SERVER = config.get("IMAP_SERVER", "")
        self.USERNAME = config.get("USERNAME", "")
        self.PASSWORD = config.get("PASSWORD", "")

    def get_ident(self) -> int:
        return self.selected

    def get_config_ident(self, username: str) -> int:
        for index, config in enumerate(self.configs):
            if config.get("USERNAME", "") == username:
                return index

        raise Exception(f"Username {username} introuvable.")

    def get_usernames(self) -> List[str]:
        liste: List[str] = list()
        for config in self.configs:
            liste.append(config.get("USERNAME", ""))

        return liste


class Mail:

    mail: imaplib.IMAP4_SSL

    configs: List[Dict]

    IMAP_SERVER: str = ""
    USERNAME: str = ""
    PASSWORD: str = ""

    def __init__(self):
        self.set_config()

    def set_config(self, ident: int = 0) -> None:
        config = MailConfig()
        self.IMAP_SERVER = config.IMAP_SERVER
        self.USERNAME = config.USERNAME
        self.PASSWORD = config.PASSWORD

    def connect(self) -> None:
        try:
            # 1. Connexion sécurisée au serveur IMAP (port 993)
            self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            self.connected = True
            # print(f"connected to {self.IMAP_SERVER}.")

        except Exception as e:
            self.connected = False
            self.logged = False
            print(f"Connection error : {e}")
            return

        try:
            # 2. Authentification
            self.mail.login(self.USERNAME, self.PASSWORD)
            self.logged = True
            # print(f"Utilisateur {self.USERNAME} authentifié.")

        except Exception as e:
            self.logged = False
            print(f"Authentication error : {e}")
            return

    def select(self, directory: str) -> None:
        if not self.logged:
            return

        if len(directory) > 0 and directory[0] != '"':
            directory = f'"{directory}"'
        self.directory = directory

        # 2. Sélection de la boîte de réception ("INBOX")
        self.mail.select(self.directory)

        return
    
        status, response = self.mail.status(self.directory, "(MESSAGES UNSEEN)")
        if status == "OK":
            # response contient une liste avec un seul élément en bytes
            data = response[0].decode("utf-8").strip("()")
            dossier, _, messages, _, unseen = data.split()
            print(dossier, " :")
            print("  Message : ", messages)
            print("  Non lu  : ", unseen)
            print()

    @staticmethod
    def decoder_texte(header_val) -> str:
        """Décode les entêtes du mail si nécessaire."""
        if header_val is None:
            return "None"

        val, encoding = decode_header(header_val)[0]
        try:
            if isinstance(val, bytes):
                return val.decode(encoding or "utf-8", errors="ignore")
            return val

        except Exception:
            return "/!\\ " + val.decode("utf-8", errors="ignore")

    @staticmethod
    def decoder_date(date_val) -> str:
        if date_val is None or date_val == "None":
            return ""

        try:
            # Décodage en objet datetime conscient du fuseau horaire (timezone-aware)
            while date_val and (
                    date_val[0].lower() not in "azertyuiopmlkjhgfdsqwxcvbn0123456789"):
                date_val = date_val[1:]

            parsed_date = parsedate_to_datetime(date_val)
            date = parsed_date.strftime("%Y-%m-%d %H:%M:%S %z")

        except Exception as erreur:
            print("mail.decoder_date()", date_val, erreur)
            date = date_val

        return date

    @staticmethod
    def decode_imap_utf7(chaine) -> str:
        # print(f"decode: *{chaine}*")
        res: List = []
        decode: List = []
        for caractere in chaine:
            if caractere == '&' and not decode:
                # Début d'une séquence encodée
                decode.append('&')

            elif caractere == '-' and decode:
                # Fin d'une séquence encodée
                if len(decode) == 1:
                    res.append('&')  # C'était un '&' littéral (&-)
                else:
                    # Restauration du base64 standard et décodage UTF-16BE
                    b64_str = ''.join(decode[1:]).replace(',', '/') + '==='
                    b = binascii.a2b_base64(b64_str)
                    res.append(b.decode('utf-16be'))
                decode = []

            elif decode:
                decode.append(caractere)

            else:
                res.append(caractere)
                
        if decode:
            b64_str = ''.join(decode[1:]).replace(',', '/') + '==='
            b = binascii.a2b_base64(b64_str)
            res.append(b.decode('utf-16be'))
            
        return ''.join(res)

    @staticmethod
    def print_body(body: str) -> None:
        maxi: int = 5
        taille: int = 100
        total: int = len(body)
        indice: int = 0
        indice_body: int = 0
        while indice < maxi:
            debut = indice_body * taille
            indice_body += 1
            premiere = True
            for ligne_n in body[debut:debut+taille].split("\n"):
                for ligne_r in ligne_n.split("\r"):
                    if ligne_r.strip() != "":
                        premiere = True
                        indice += 1
                        # print(indice, ligne_r)
                        print(" |", ligne_r)

                    elif premiere:
                        premiere = False
                        print(" |")

                    if indice >= maxi:
                        break

                if indice >= maxi:
                    break

            if (indice_body+1) * taille > total:
                indice = maxi

        print("---")

    def extract_payload(self, indice, message) -> None:

        all_content = message.get("Content-Type")
        content_disposition = str(message.get("Content-Disposition"))
        # content_encoding = message.get("Content-Transfer-Encoding")

        if all_content:
            content_type, charset = [tab.strip() 
                for tab in all_content.split(";")]
            *debut, encoding = charset.split("=")

        else:
            content_type = ""
            encoding = "?"

        if debut and debut[0].lower() == "charset":
            encoding = encoding.replace("\"", "")
            
        # print(f"#-{indice}>", content_type, content_disposition, content_encoding, debut, encoding)

        if (content_type not in ["text/plain", "-text/html"] or 
                "attachment" in content_disposition):
            return

        payload = message.get_payload(decode=True)
        if type(payload) is bytes:
            body = payload.decode(encoding, errors="ignore")
        else:
            print("payload type:", type(payload))
            body = str(payload)

        print("Corps :")
        self.print_body(body)

    def get_dirs(self, directory: Optional[str] = None) -> Generator:
        if not self.logged:
            return

        association: Dict = {
            "inbox": (1, "Courrier"),
            "outbox": (2, "A envoyer"),
            "junk": (4, "Indésirables"),
            "draft": (6, "Brouillon"),
            "drafts": (7, "Brouillons"),
            "sent": (9, "Envoyés"),
            "sent items": (10, "Éléments envoyés"),
            "trash": (14, "Corbeille"),
            "deleted items": (15, "Éléments supprimés")
        }

        # 2. Récupération de la liste des répertoires
        # parametres :  directory='INBOX', pattern='%'
        if directory is None:
            status, folder_list = self.mail.list(pattern='%')
        else:
            if directory[0] != '"':
                directory = f'"{directory}"'
            status, folder_list = self.mail.list(directory=directory)

        if status == "OK":
            for folder in folder_list:
                if folder is None or isinstance(folder, tuple):
                    continue

                # Décodage de la réponse brute (bytes -> str)
                folder_str = folder.decode("utf-8")

                # Extraction du nom du dossier via une expression régulière
                # La réponse a la forme : '(\\HasNoChildren) "/" "INBOX"'
                match = re.search(r'\(.*?\) "[^"]*?" "?([^"]*)"?$', folder_str)
                if match:
                    folder_str = match.group(1)
                    true_name = folder_str

                    if "&" in folder_str:
                        folder_str = self.decode_imap_utf7(folder_str)

                    folder_assoc = association.get(folder_str.lower())
                    if folder_assoc is None:
                        yield (False, 0, true_name, folder_str, true_name)

                    else:
                        yield (True, folder_assoc[0], folder_str, folder_assoc[1], true_name)

                else:
                    print(f"get_dirs(), Erreur: {folder_str}")

    @staticmethod
    def flags_list_to_code(flags_list: List) -> str:
        flags: str = ""
        for flag in flags_list:
            if flag == "\\Seen": 
                flags += "V"
            elif flag == "NEWSLETTER": 
                flags += "L"
            elif flag == "Junk": 
                flags += "J"
            elif flag == "$HasAttachment": 
                flags += "F"
            elif flag == "\\Answered": 
                flags += "R"
            elif flag == "\\Recent": 
                flags += "N"

        return flags

    def get_mails(self, mail_type: str) -> Generator:
        if not self.logged:
            return

        status, messages = self.mail.search(None, mail_type)
        email_ids: List = messages[0].split()
        for mail_id in email_ids[:]:
            status, msg_data = self.mail.fetch(mail_id, "(BODY.PEEK[HEADER] FLAGS)")
            if status != "OK":
                print(f"Erreur {mail_id=}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    imap_response_header = response_part[0].decode('utf-8')
                    msg = email.message_from_bytes(response_part[1])
                    id_mail = mail_id.decode()
                    expediteur = " ".join(self.decoder_texte(msg.get("From")).split())
                    sujet = self.decoder_texte(msg.get("Subject")).replace("\n", "").replace("\r", "")
                    sujet = sujet.replace("\xa0", "")
                    response_date = self.decoder_texte(msg.get("Date"))

                    flags: str = ""
                    if "FLAGS" in imap_response_header:
                        flags_part = imap_response_header.split("FLAGS (")[1].split(")")[0]
                        flags_list = flags_part.split()
                        flags = self.flags_list_to_code(flags_list)
                    
                    date = self.decoder_date(response_date)

                    datas: dict = {
                        "ATT": f"{flags}",
                        "NUM": f"{id_mail}",
                        "EXP": f"{expediteur}",
                        "OBJ": f"{sujet}",
                        "DAT": f"{date}"
                    }
                    yield datas

    def read_dirs(self, directory=None) -> None:
        liste_repertoires = list(self.get_dirs(directory))
        print("Nomre de répertoires trouvés :", len(liste_repertoires))
        for dir in liste_repertoires:
            print("-", dir)
        print()

    def read(self, mail_type: str) -> None:
        # 3. Recherche des e-mails (ici, récupération des e-mails non lus : "UNSEEN")
        # Pour tous les e-mails, utilisez "ALL"
        # status, messages = self.mail.search(None, mail_type)

        # Récupération de la liste des identifiants d'e-mails
        mails: List = list(self.get_mails(mail_type))
        print(f"Nombre d'e-mails trouvés : {len(mails)}")

        for mail in mails:
            print(f'{mail["NUM"]:3}', end=" ")
            print(f'{mail["ATT"]:3}', end=" ")
            print(mail["DAT"], end=" ")
            print(mail["OBJ"])
            pass

        # Récupération des données brutes du message
        # Recommandé :
        # ------------
        # BODY.PEEK[]       Récupère l'intégralité du message (entêtes + corps) sans marquer l'e-mail comme lu.
        # 
        # Autres options :
        # ----------------
        # RFC822            Récupère également l'intégralité du message, mais marque automatiquement le message comme lu (\Seen) sur le serveur.
        # BODY.PEEK[HEADER] Récupère uniquement les entêtes du mail (Sujet, Expéditeur, Date, etc.) sans marquer comme lu.
        # BODY.PEEK[TEXT]   Récupère uniquement le corps du message (sans les entêtes) sans marquer comme lu.
        # FLAGS             Récupère les drapeaux du message (\Seen pour lu, \Answered pour répondu, \Flagged pour important, \Deleted, etc.).
        # INTERNALDATE      Récupère la date et l'heure de réception du message sur le serveur IMAP.
        # RFC822.SIZE       Récupère la taille du message en octets.
        # UID               Récupère l'identifiant unique (UID) du message.
        # status, msg_data = self.mail.fetch(mail_id, "BODY.PEEK[]")

        # --- MARQUER COMME NON LU ---
        # if mail_type == "UNSEEN":
        #    Remet le fanion (flag) '\Seen' à zéro
        #    self.mail.store(mail_id, "-FLAGS", "\\Seen")

        # --- SUPPRIMER UN MAIL ---
        # Étape 1 : Marquer le mail avec le fanion '\Deleted'
        # mail.store(mail_id, "+FLAGS", "\\Deleted")
        # print(f"-> Mail {mail_id.decode()} marqué pour SUPPRESSION.")

    def disconnect(self) -> None:
        if self.connected and self.mail.state == "SELECTED":
            self.connected = False
            try:
                self.mail.close()
                # print(f"Utilisateur {self.USERNAME} déconnecté.")
            except Exception as e:
                print("close error:", e)

        if self.logged and self.mail.state == "AUTH":
            self.logged = False
            try:
                self.mail.logout()
                # print(f"serveur {self.IMAP_SERVER} déconnecté.")
            except Exception as e:
                print("logout error:", e)

    def run(self) -> None:

        self.connect()

        directory = "INBOX"
        # directory = '"El&AOk-ments envoy&AOk-s"'
        if True:
            self.read_dirs()
        else:
            self.read_dirs(directory)

        self.select(directory)  
        self.read("ALL")  # ALL, UNSEEN
        self.disconnect()


def main() -> None:
    config: MailConfig
    ident: int

    config = MailConfig()
    config.read_config_json()
    ident = config.get_config_ident("jacquesc@noos.fr")
    config.set_config(ident)  # ident

    mail = Mail()
    mail.run()


if __name__ == '__main__':
    main()

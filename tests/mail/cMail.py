import email
import imaplib

from email.header import decode_header
from datetime import datetime


class Mail:

    mail: imaplib.IMAP4_SSL

    IMAP_SERVER: str = ""
    USERNAME: str = ""
    PASSWORD: str = ""

    def __init__(self):
        # Get Configuration 
        res: str = "?"

        with open("ENVIRONNEMENT") as env:
            while res != "":
                res = env.readline().strip()
                if not res:
                    continue

                key, value = res.split("=")
                valeur = value.strip("\"")
                match key.upper():
                    case "IMAP_SERVER":
                        self.IMAP_SERVER = valeur
                    case "USERNAME":
                        self.USERNAME = valeur
                    case "PASSWORD":
                        self.PASSWORD = valeur

    def connect(self):
        try:
            # 1. Connexion sécurisée au serveur IMAP (port 993)
            self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            self.connected = True
            print(f"connected to {self.IMAP_SERVER}.")

        except Exception as e:
            self.connected = False
            self.logged = False
            print(f"Connection error : {e}")
            return

        try:
            # 2. Authentification
            self.mail.login(self.USERNAME, self.PASSWORD)
            self.logged = True
            print(f"Utilisateur {self.USERNAME} authentifié.")

        except Exception as e:
            self.logged = False
            print(f"Authentication error : {e}")
            return

    def select(self, directory: str):
        if not self.logged:
            return

        self.directory = directory

        # 2. Sélection de la boîte de réception ("INBOX")
        self.mail.select(self.directory)

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
    def decoder_texte(header_val):
        """Décode les entêtes du mail si nécessaire."""
        val, encoding = decode_header(header_val)[0]
        if isinstance(val, bytes):
            return val.decode(encoding or "utf-8", errors="ignore")
        return val

    @staticmethod
    def print_body(body: str):
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

    def extract_payload(self, indice, message):

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

    def read(self, mail_type: str):
        # 3. Recherche des e-mails (ici, récupération des e-mails non lus : "UNSEEN")
        # Pour tous les e-mails, utilisez "ALL"
        status, messages = self.mail.search(None, mail_type)

        # Récupération de la liste des identifiants d'e-mails
        email_ids = messages[0].split()

        print(f"Nombre d'e-mails trouvés : {len(email_ids)}")

        # 4. Parcourir les derniers e-mails (ici le plus récents)
        for mail_id in email_ids[:]:
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
            status, msg_data = self.mail.fetch(mail_id, "BODY.PEEK[]")
            if status != "OK":
                print(f"Erreur {mail_id=}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Conversion des données brutes en objet email
                    msg = email.message_from_bytes(response_part[1])

                    expediteur = " ".join(self.decoder_texte(msg.get("From")).split())
                    sujet = self.decoder_texte(msg.get("Subject"))
                    date_reception = self.decoder_texte(msg.get("Date"))

                    print(f"\n--- E-mail ID: {mail_id.decode()} ---")
                    try:
                        date = datetime.strptime(date_reception, "%a, %d %b %Y %H:%M:%S %z")
                        print(f"Date2 : {date.isoformat()} ", end="")
                        # .strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        print(f"Date1 : {date_reception[:32]:34} ", end="")

                    # decodage : "%a, %d %b %Y %H:%M:%S %z"
                    print(f"De : {expediteur}")
                    print(f"Sujet : {sujet}")

                    # Extraction du corps de l'e-mail
                    if msg.is_multipart():
                        for indice, part in enumerate(msg.walk()):
                            # Récupère le texte brut s'il ne s'agit pas d'une pièce jointe
                            self.extract_payload(indice, part)

                    else:
                        self.extract_payload(0, msg)

            # --- MARQUER COMME NON LU ---
            if mail_type == "UNSEEN":
                # Remet le fanion (flag) '\Seen' à zéro
                # self.mail.store(mail_id, "-FLAGS", "\\Seen")
                pass

            # --- SUPPRIMER UN MAIL ---
            # Étape 1 : Marquer le mail avec le fanion '\Deleted'
            # mail.store(mail_id, "+FLAGS", "\\Deleted")
            # print(f"-> Mail {mail_id.decode()} marqué pour SUPPRESSION.")

    def disconnect(self):
        if self.connected and self.mail.state == "SELECTED":
            self.connected = False
            try:
                self.mail.close()
                print(f"Utilisateur {self.USERNAME} déconnecté.")
            except Exception as e:
                print("close error:", e)

        if self.logged and self.mail.state == "AUTH":
            self.logged = False
            try:
                self.mail.logout()
                print(f"serveur {self.IMAP_SERVER} déconnecté.")
            except Exception as e:
                print("logout error:", e)

    def run(self):
        self.connect()
        self.select("INBOX")
        self.read("UNSEEN")  # ALL
        self.disconnect()


def main():
    mail = Mail()
    mail.run()


if __name__ == '__main__':
    main()

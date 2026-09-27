import imaplib
import re

from typing import Optional, Tuple, Dict


# Init Configuration 
IMAP_SERVER: str = ""
USERNAME: str = ""
PASSWORD: str = ""

# Get Configuration 
res: str = "debut"

with open("ENVIRONNEMENT") as env:
    while res != "":
        res = env.readline().strip()
        if not res:
            continue

        key, value = res.split("=")
        valeur = value.strip("\"")
        match key.upper():
            case "IMAP_SERVER":
                IMAP_SERVER = valeur
            case "USERNAME":
                USERNAME = valeur
            case "PASSWORD":
                PASSWORD = valeur


# 1. Connexion au serveur IMAP (en SSL)
imap_server = IMAP_SERVER
email_user = USERNAME
email_pass = PASSWORD

association: Dict = {
    "inbox": "Courrier",
    "outbox": "A envoyer",
    "junk": "Indésirables",
    "draft": "Brouillon",
    "drafts": "Brouillons",
    "sent": "Envoyés",
    "trash": "Corbeille"
}

try:
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)

    # 2. Récupération de la liste des répertoires
    # parametres :  directory='INBOX', pattern='%'
    status, folder_list = mail.list(pattern='%')  

    if status == "OK":
        print("Répertoires trouvés :")
        for folder in folder_list:
            if folder is None or isinstance(folder, tuple):
                continue

            # Décodage de la réponse brute (bytes -> str)
            folder_str = folder.decode("utf-8")

            # Extraction du nom du dossier via une expression régulière
            # La réponse a la forme : '(\\HasNoChildren) "/" "INBOX"'
            match = re.search(r'\(.*?\) ".*?" "?(.*)"?', folder_str)
            if match:
                folder_str = match.group(1)
                folder_name = affectation.get(folder_str.lower(), folder_str)
                print(f'("{folder_str}", "{folder_name}")')
            else:
                print(f"Erreur de décodage: {folder_str}")

    # 3. Fermeture de la connexion
    mail.logout()

except Exception as e:
    print(f"Erreur : {e}")

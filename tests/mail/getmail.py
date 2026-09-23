import email
from email.header import decode_header
import imaplib


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


def print_body(body: str):
    maxi: int = 20
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


def extract_payload(indice, message):

    all_content = message.get("Content-Type")
    content_disposition = str(message.get("Content-Disposition"))
    content_encoding = message.get("Content-Transfer-Encoding")

    if all_content:
        content_type, charset = [tab.strip() 
            for tab in all_content.split(";")]
        *debut, encoding = charset.split("=")

    else:
        content_type = ""
        encoding = "?"

    if debut and debut[0].lower() == "charset":
        encoding = encoding.replace("\"", "")
        
    print(f"#-{indice}>", content_type, content_disposition, content_encoding, debut, encoding)

    if content_type != "text/plain" or "attachment" in content_disposition:
        return

    payload = message.get_payload(decode=True)
    if type(payload) is bytes:
        body = payload.decode(encoding, errors="ignore")
    else:
        body = str(payload)

    print("Corps :")
    print_body(body)


def decoder_texte(header_val):
    """Décode les entêtes du mail si nécessaire."""
    val, encoding = decode_header(header_val)[0]
    if isinstance(val, bytes):
        return val.decode(encoding or "utf-8", errors="ignore")
    return val


try:
    # 1. Connexion sécurisée au serveur IMAP (port 993)
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(USERNAME, PASSWORD)

    # 2. Sélection de la boîte de réception ("INBOX")
    mail.select("INBOX")

    # 3. Recherche des e-mails (ici, récupération des e-mails non lus : "UNSEEN")
    # Pour tous les e-mails, utilisez "ALL"
    status, messages = mail.search(None, "UNSEEN")
    # status, messages = mail.search(None, "ALL")

    # Récupération de la liste des identifiants d'e-mails
    email_ids = messages[0].split()

    print(f"Nombre d'e-mails trouvés : {len(email_ids)}")

    # 4. Parcourir les derniers e-mails (ici les 5 plus récents)
    for mail_id in email_ids[-10:]:
        # Récupération des données brutes du message
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        if status != "OK":
            print(f"Erreur {mail_id=}")
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Conversion des données brutes en objet email
                msg = email.message_from_bytes(response_part[1])

                expediteur = " ".join(decoder_texte(msg.get("From")).split())
                sujet = decoder_texte(msg.get("Subject"))
                date_reception = decoder_texte(msg.get("Date"))
                content_type = decoder_texte(msg.get("Content-Type"))

                print(f"\n--- E-mail ID: {mail_id.decode()} ---")
                print(f"Date : {date_reception[:32]:34} ", end="")
                print(f"De : {expediteur}")
                print(f"Sujet : {sujet}")

                # Extraction du corps de l'e-mail
                if msg.is_multipart():
                    for indice, part in enumerate(msg.walk()):
                        # Récupère le texte brut s'il ne s'agit pas d'une pièce jointe
                        extract_payload(indice, part)

                else:
                    extract_payload(0, msg)

        # --- MARQUER COMME NON LU ---
        # Remet le fanion (flag) '\Seen' à zéro
        mail.store(mail_id, "-FLAGS", "\\Seen")
        # print(f"-> Mail {mail_id.decode()} marqué comme NON LU.")

        # --- SUPPRIMER UN MAIL ---
        # Étape 1 : Marquer le mail avec le fanion '\Deleted'
        # mail.store(mail_id, "+FLAGS", "\\Deleted")
        # print(f"-> Mail {mail_id.decode()} marqué pour SUPPRESSION.")

    # Étape 2 : Appliquer définitivement la suppression des mails marqués '\Deleted'
    # mail.expunge()
    
    # 5. Déconnexion
    mail.close()
    mail.logout()

except Exception as e:
    print(f"Erreur : {e}")

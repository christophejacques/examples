import imaplib

# Définition des informations de connexion
imap_host = "imap.gmail.com"
imap_port = 993
username = "christophe.michael.jacques@gmail.com"
password = "password"

# Connexion au serveur IMAP
with imaplib.IMAP4_SSL(imap_host, imap_port) as imap:
    imap.login(username, password)

    # Sélection de la boîte de réception
    imap.select("INBOX")

    # Récupération des identifiants des emails
    status, email_ids = imap.search(None, "ALL")

    # Itération sur les emails
    for email_id in email_ids[0].split():
        # Récupération du contenu de l'email
        status, email_data = imap.fetch(email_id, "(RFC822)")

        # Décodage du message
        message = email_data[0][1].decode("utf-8")

        # Traitement du message
        print(message)

    # Déconnexion du serveur IMAP
    imap.logout()

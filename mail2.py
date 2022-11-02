import imaplib
import email
import traceback 
import base64
import quopri
import html
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "christophe.michael.jacques" + ORG_EMAIL 
<<<<<<< HEAD
FROM_PWD = "xxxxxxxx" 
=======
FROM_PWD = "password" 
>>>>>>> 154bc9e3f82f2a3a57b5fa36d70b209759ec8141
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993


def aucun_codage(*args):
    return ""


def unquote_printable(charset="UTF-8"):
    def encodage(s):
        return quopri.decodestring(s).decode(charset)
    return encodage


def unquote_base64(charset="UTF-8"):
    def encodage(s):
        return quopri.decodestring(base64.b64decode(s)).replace(b"\xca", b"?").replace(b"\xab", b"?").decode(charset)
    return encodage


def unescape_html(charset="UTF-8"):
    def encodage(s):
        return html.unescape(html_to_text(s))  # .decode(charset)
    return encodage
    # fonction = lambda x: html.unescape(html_to_text(ssfonction(x)))


def get_coding_method(contents_types):
    fonction = aucun_codage
    charset = ""

    if not (isinstance(contents_types[0], tuple) or isinstance(contents_types[0], list)):
        if len(contents_types) != 2:
            return charset, fonction   
        contents_types = [contents_types.copy()]

    for cle, content in contents_types:
        content = content.strip()
        if cle.lower() == "content-type":
            print("content-type:", end="")
            for type_content in content.split(";"):
                type_content = type_content.strip()
                if "charset" == type_content.lower().strip()[:7]:
                    _, charset = type_content.split("=")
                    if charset:
                        charset = charset.strip('"')
                        print(f' charset:"{charset}"', end=";")

                elif "name" == type_content.lower().strip()[:4]:
                    _, *tnom = type_content.split("=")
                    nom = "=".join(tnom)
                    if nom.startswith('"') and nom.endswith('"'): 
                        dnom = nom[1:-1]
                        print(f' name:"{decode_string(dnom)}"', end=";")
                    else:
                        print(f' name:"{decode_string(nom)}', end=";")
                elif "/" in type_content:
                    print(f" {type_content}", end=";")
            print()

        elif cle.lower() == "content-transfer-encoding":
            print("content-transfer-encoding:", content)
            if content == "quoted-printable":
                fonction = unquote_printable(charset)

            elif content == "base64":
                # fonction = lambda x: quopri.decodestring(base64.b64decode(x)).decode(charset)
                # fonction = lambda x: quopri.decodestring(base64.b64decode(x))
                fonction = unquote_base64(charset)

            else:
                print(f"content-transfer-encoding: '{content}' non implémenté.")

        elif cle.lower() == "content-disposition":
            # Content-Disposition: attachment; filename="AMN_20220212144751.PDFAMN.pdf"
            # print("content-disposition:", content)
            for type_content in content.split(";"):
                type_content = type_content.strip()
                if "filename" == type_content.lower()[:8]:
                    _, *tnom = type_content.split("=")
                    nom = "=".join(tnom)
                    if nom.startswith('"') and nom.endswith('"'): 
                        dnom = nom[1:-1]
                        print(f'filename:"{decode_string(dnom)}"')
                    else:
                        print(f'filename:"{decode_string(nom)}')

        elif cle.lower() == "x-attachment-id":
            # X-Attachment-Id: 17eee314970fff2d2221
            pass
            
        elif cle.lower() == "content-id":
            # Content-ID: <f_l2k5a0be0>
            pass
            
        elif cle.lower() == "content-description":
            # Content-Description: image001.gif
            pass

        elif cle.lower() == "mime-version":
            # MIME-Version: 1.0
            pass

        elif cle.lower() == "delivered-to":
            # Delivered-To [ christophe.michael.jacques@gmail.com ]
            print("Delivered-To:", content)

        elif cle.lower() == "received":
            # Received [ by 2002:a05:6102:504a:0:0:0:0 with SMTP id by10csp7953029vsb;
            print("Received:", content.split("\n"))

        elif cle.lower() == "x-google-smtp-source":
            # X-Google-Smtp-Source [ ABdhPJyycnL0aEdwVkqej01RnCO2hqRZEiulbVs7ketE2aFi46ezXbGl28LIUANl+pAtb+Eg9qXZ ]
            print(f"{cle}:", content)

        elif cle.lower() == "x-received":
            # X-Received [ by 2002:adf:fd0b:0:b0:20a:ea57:6dab with SMTP id e11-20020adffd0b000000b0020aea576dabmr9684462wrr.175.1651505169834;
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "arc-seal":
            # X-Received [ i=1; a=rsa-sha256; t=1651505169; cv=none; d=google.com; s=arc-20160816;
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "arc-message-signature":
            # X-Received [ i=1; a=rsa-sha256; t=1651505169; cv=none; d=google.com; s=arc-20160816;
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "arc-authentication-results":
            # X-Received [ i=1; a=rsa-sha256; t=1651505169; cv=none; d=google.com; s=arc-20160816;
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "return-path":
            # Return-Path [ <tele_loisirs@ml.tv-news.fr> ]
            print(f"{cle}:", content)

        elif cle.lower() == "received":
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "received-spf":
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "authentication-results":
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "dkim-signature":
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content.split("\n"))

        elif cle.lower() == "x-abuse-reports-to":
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "X-CSA-complaints".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "X-Mailer".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "Message-ID".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "X-Auto-Response-Suppress".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "X-CampaignID".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "List-Unsubscribe".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "List-Unsubscribe-Post".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "List-ID".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "Feedback-ID".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "X-SignalSpam-CID".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "From".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            if '"' in content:
                debut, a_decoder, *tfin = content.split('"')
                fin = '"'.join(tfin)
                print(f"{cle}:", f'{debut}"{decode_string(a_decoder)}"{fin}')
            else:
                print(f"{cle}:", content)

        elif cle.lower() == "To".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "Subject".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", decode_string(content))

        elif cle.lower() == "Precedence".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        elif cle.lower() == "Date".lower():
            # Received [ from poc-geo4.splio.com (poc-geo4.splio.com. [91.190.171.74])
            print(f"{cle}:", content)

        else:
            print("cle non implémentée:", cle, "[", content, "]")

    return charset, fonction   


def html_to_text(texte_html):
    pos1 = pos2 = 0
    res = ""
    try:
        while texte_html:
            pos1 = texte_html.index("<")
            pos2 = texte_html.index(">", pos1)
            balise = texte_html[1+pos1:pos2].split()[0]
            # print("balise:", balise)
            if pos1 > 0:
                res += texte_html[:pos1].strip()
            if balise.strip("/").lower() in ("br", "p"):
                res += "\n"
            texte_html = texte_html[pos2+1:].strip()

    except ValueError:
        # traceback.print_exc()
        res += texte_html

    return res


def read_message(m):
    fonction = aucun_codage
    charset = ""
    if m.get_payload():
        if m.is_multipart():
            if isinstance(m.get_payload()[0], email.message.Message):
                
                if m.get("Date"):
                    print("Date :", m.get("Date", "?"))
                if m.get("From"):
                    print('From :', m.get("From", "?"))
                if m.get('subject'):
                    print('Subject :', decode_string(m.get('subject', "?")))
                # print(dir(m))
                # for k, v in m.__dict__.items():
                #     print("#", k, v)

                for payload in m.get_payload():
                    read_message(payload)
                return

        elif "text/plain" == m.get_content_type():
            print("-=" * 40)
            charset, fonction = get_coding_method(m.items())

        elif "text/html" == m.get_content_type():
            print("-=" * 40)
            charset, ssfonction = get_coding_method(m.items())
            fonction = lambda x: html.unescape(html_to_text(ssfonction(x)))

        elif "image/" == m.get_content_type()[:6]:
            print("IMG:", m.get_content_type())

        elif "application/pdf" == m.get_content_type():
            print("PDF:", m.get_content_type())

        else:
            print("unknown content_type:", m.get_content_type())

        texte = ""
        debut = False
        for ligne in m.as_string().split("\n"):
            if debut:
                texte += ligne + "\n"
            else:
                # print("#", ligne)
                if ligne[:7].lower() != "content":
                    debut = True
                if not ligne.strip(): 
                    continue
                get_coding_method(ligne.split(":"))

        print(fonction(texte))

    else:
        print("No payload !")


def decode_string(chaine):
    res = ""
    for ligne in chaine.split("\n"):
        ligne = ligne.strip()
        if ligne.startswith("=") and ligne.endswith("="): 
            ligne = ligne[1:-1]
            sep = ligne[0]
            _, charset, methode_codage, detail, *_ = ligne.split(sep)
            if methode_codage == "Q":
                ligne = quopri.decodestring(detail).decode(charset)
            elif methode_codage == "B":
                ligne = base64.b64decode(detail).decode(charset)
            else:
                print(f"unknow codage method: *{methode_codage}*")
            res += ligne

        else:
            res += ligne
    return res


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        # print("email id:", first_email_id, latest_email_id)
        print("Nombre de messages:", latest_email_id - first_email_id)

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    try:
                        msg = email.message_from_string(str(arr[1], 'UTF-8'))
                        print("o=" * 45)
                        # print(msg)
                        # print("o=" * 45)
                        read_message(msg)
                        # return
                        continue

                    except UnicodeDecodeError as u:
                        print("UnicodeDecodeError", u)

                    except Exception as e:
                        print("Error", e)
                        traceback.print_exc()

                    # return

    except Exception as e:
        traceback.print_exc() 
        print(str(e))


if __name__ == "__main__":
    read_email_from_gmail()

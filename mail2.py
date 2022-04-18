import imaplib
import email
import traceback 
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "christophe.michael.jacques" + ORG_EMAIL 
FROM_PWD = "password" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993


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
        print("email id:", first_email_id, latest_email_id)

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    try:
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        email_subject = msg['subject'].replace("\n", "")
                        email_from = msg['from']
                        # print("dir:", msg)
                        print("Date :", msg["Date"])
                        print('From : ' + email_from)
                        print('Subject : ' + email_subject + '\n')
                    except UnicodeDecodeError:
                        pass
                    except Exception as e:
                        print("Error", e)

    except Exception as e:
        traceback.print_exc() 
        print(str(e))


read_email_from_gmail()

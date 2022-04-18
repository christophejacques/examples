#!/usr/bin/env python3
import urllib.request
from html import unescape


email = 'christophe.michael.jacques@gmail.com'
password = 'pleinne2'
max_messages = 4


def install_mail_opener():
    # Set up authentication for gmail
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='mail.google.com',
                              uri='https://mail.google.com/',
                              user=email,
                              passwd=password)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)


def get_content(texte, balise, start=0, count=1):
    lcount = 0
    while lcount < count:
        lcount += 1
        ifrom = texte.index(f'<{balise}>', start) + len(balise) + 2
        ito   = texte.index(f'</{balise}>', start + len(balise) )
        start = ito + len(balise)

    return ifrom, ito, texte[ifrom:ito]


def get_contents(texte, balise, maxcount=999999):
    liste = []
    index = 0
    fin = 0
    error = False
    while not error and index < maxcount:
        try:
            debut, fin, contenu = get_content(texte, balise, fin)
            liste.append(contenu)

        except ValueError:
            error = True
        except Exception as e:
            error = True
            print("Error", e)

    return liste


def main():
    install_mail_opener()

    gmailurl = 'https://mail.google.com/gmail/feed/atom'
    with urllib.request.urlopen(gmailurl) as page:
        contents = unescape(page.read().decode('utf-8'))

    contenus = get_contents(contents, "title")
    if contenus:
        print(contenus[0])
        print(f"{len(contenus)-1} nouveau(x) message(s) :")
        for title in contenus[1:1+max_messages]:
            print("-", title)
        if len(contenus) > max_messages+1: 
            print("...")
    else:
        print("Aucun nouveau message")


if __name__ == "__main__":
    main()

# input()

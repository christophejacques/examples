import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib.parse import urlparse, unquote
import json
import ssl
import socket


def print_dico(title, dico):
    print(title, ":")
    for champ in dico:
        print("-", champ, ":", dico[champ])


def check_code(code):
    if code in (requests.codes["OK"], requests.codes["okay"]):
        print("Connexion OK")
    else:
        print("code:", code, end=", ")
        if code == requests.codes["unauthorized"]:
            print("Autorisation requise !")
        elif code == requests.codes["forbidden"]:
            print("Acces interdit !")
        elif code == requests.codes["not_allowed"]:
            print("Acces non autorise !")
        elif code == requests.codes["proxy_authentication"]:
            print("Erreur d'autentification au Proxy !")

    return code


def reponse_get(r, *args, **kwargs):
    print("URL =", r.url)
    check_code(r.status_code)


def parse_json(key, value, curent_level, massage):
    t = type(value)
    if t == str:
        try:
            tmp = json.loads(value)
            for k in tmp:
                parse_json(k, tmp[k], curent_level + 1, massage)
        except Exception:
            print("  " * curent_level + str(key), ":", value)
            return
    else:
        if t == list:
            print("  " * curent_level + str(key), "[")
            for li in value:
                parse_json(key, li, curent_level + 1, massage)
            print("  " * curent_level + "]")
            return
        if t == dict:
            print("  " * curent_level + str(key), "{")
            for k in value:
                parse_json(k, value[k], curent_level + 1, massage)
            print("  " * curent_level + "}")
            return
        if t == set:
            print("  " * curent_level + str(key), "(")
            for li in value:
                parse_json(key, li, curent_level + 1, massage)
            print("  " * curent_level + ")")
            return

        print("  " * curent_level + str(key), ":", value)


# 'https://httpbin.org/ip'
# URL = "https://portail.cykleo.fr/pu/stations/availability?organization_id=5"
URL = "https://portail.cykleo.fr/TAO_velos/carte_stations"

hostname = 'portail.cykleo.fr'
port = 443
resource = '/'

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
sock = socket.create_connection((hostname, port))
ssock = context.wrap_socket(sock, server_hostname=hostname)


with requests.Session() as s:

    # Tentative d'autentification
    auth = HTTPBasicAuth('utilisateur', 'password')
    s.auth = auth

    # Ajout d'une fonction callback sur Session
    s.hooks['response'].append(reponse_get)
    s.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"

    p = s.get(URL, timeout=(4, 10))
    if False:
        print_dico("Session", s.headers)
        print()
        print_dico("Request", p.headers)
        print()

    # .netrc might have more auth for us on our new host.
    # new_auth = requests.utils.get_netrc_auth(URL)
    # prepared_request = p.copy()
    # if new_auth is not None:
    #     prepared_request.prepare_auth(new_auth)

    if "json" in p.headers["Content-Type"].lower():
        print(p.json())
    elif False:
        charset = "ANSI"
        # print("Content-Type:", p.headers["Content-Type"])
        for ligne in p.iter_lines():
            if "<meta " in ligne.decode():
                if "charset=" in ligne.decode():
                    charset = ligne.decode().split()[1].split("=")[1].split("\"")[1]

                to_check = False
                for param in ligne.decode(charset).split():
                    if "name=" in param and "config/environment" in param:
                        print(param)
                        to_check = True
                    if to_check and "content=" in param:
                        config = json.loads(unquote(param.split("=")[1])[1:-1])
                        parse_json("root", config, 0, {})
                if not to_check:
                    print(ligne.decode(charset))
            else:
                print(ligne.decode(charset))

    # if check_code(p.status_code) != requests.codes["OK"]:
    if p.status_code != requests.codes["OK"]:
        exit(0)

    if False:
        if s.cookies.items():
            print("Session.Cookies:", s.cookies.items())
        if p.cookies.items():
            print("Get cookies:", p.cookies.items())
        print()
        print_dico("Session", s.headers)
        print()
        print_dico("Request", p.headers)

    s.auth = HTTPDigestAuth('utilisateur', 'password0')

    jar = requests.cookies.RequestsCookieJar()
    if True:
        jar.set('acceptAnalyticCookies', 'true', domain=urlparse(URL).netloc, path="/")
        jar.set('_ga', 'GA1.2.2031518071.1634980626', domain=urlparse(URL).netloc, path="/")
    s.cookies = jar
    s.headers['Referer'] = 'https://portail.cykleo.fr/TAO_velos/carte_stations'

    URL = "https://portail.cykleo.fr/pu/stations/availability"
    URL += "?organization_id=5"
    print()

    p1 = s.get(URL, timeout=(4, 10), cookies=jar)
    if False:
        if s.cookies.items():
            print("Session.Cookies:", s.cookies.items())
        if p1.cookies.items():
            print("Get cookies:", p1.cookies.items())

    if "json" in p1.headers['Content-Type'].lower():
        print("\napplication/json:")
        parse_json("root", p1.json(), 0, {})
        # print_dico("application/json", p1.json())
    else:
        print(p1.text)

exit(0)

# HTTP Basic authentication for website
auth = HTTPBasicAuth('user1', 'password0')
s.auth = auth
print(2, s.get('https://httpbin.org/basic-auth/user1/password0').text)

# HTTP Digest authentication for website
auth = HTTPDigestAuth('user1', 'password0')
s.auth = auth
print(3, s.get('https://httpbin.org/digest-auth/auth/user1/password0').text)

import urllib.parse
import urllib.request as ur
from urllib.parse import urlencode
import ssl, socket, os

DEBUG = False
ignore_certificats = False
print("debut")

# url = ur.urljoin("Http://perso.numericable.com", "cjacques/ASP/Actualisation_Financeurs.txt")
# 
url = ur.urljoin("Https://echange.asp-public.fr", "FdCR/4.00/Patchs/N0010.txt")


def getFile(url):

    if ur.getproxies():
        print("Paramétrage du proxy")
        proxy_protocols = {}
        if ur.getproxies().get("http"):
            proxy_protocols["http"] = ur.getproxies().get("http")
        if ur.getproxies().get("http"):
            proxy_protocols["https"] = ur.getproxies().get("https")
        proxy = ur.ProxyHandler(proxy_protocols)
        
        password_mgr = ur.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "christophe.jacques1", "password")

        auth = ur.HTTPBasicAuthHandler(password_mgr)
        if DEBUG:
            print("http auth-header:", )
            for a in auth.passwd.passwd[None]:
                print(" -", a, "=>", auth.passwd.passwd[None][a])
        bopener = ur.build_opener(proxy, auth, ur.HTTPHandler)
        ur.install_opener(bopener)
    else:
        print("Pas de proxy")
        
    if ur.urlparse(url).scheme == "https":
        print("Connexion sécurisée")
        # Server address
        serverHost = ur.urlparse(url).netloc
        serverPort = "443"
        serverAddress = (serverHost, serverPort)
        try:
            # Retrieve the server certificate in PEM format
            cert = ssl.get_server_certificate(serverAddress)
        except ssl.SSLCertVerificationError:
            print("Erreur de certification")
        except Exception as e:
            print("Erreur:", e)
        else:
            print("Certification : OK")

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handler = ur.HTTPSHandler(context=ctx)
        
        with socket.create_connection(serverAddress) as sock:
            with ctx.wrap_socket(sock, server_hostname=serverHost) as ssock:
                print("Sock version:", ssock.version())

    else:
        print("Pas de connexion sécurisée")
        handler = ur.HTTPHandler

    bopener = ur.build_opener(handler)
    ur.install_opener(bopener)

    response = ur.urlopen(url, timeout=5)
    # response = bopener.open(url)
    return response


def print_screen(page):
    for _ in range(5):
        ligne = page.readline()[:-1].decode('ansi').strip()
        if ligne:
            print(ligne)


def direct():
    print(url)
    print("Direct access :")
    try:
        page = ur.urlopen(url, timeout=5)
        print_screen(page)
    except Exception as e:
        print("Error:", e)


def main():
    print()
    print("Proxy + certificats :")
    page = getFile(url)
    print_screen(page)


try:
    direct()
    main()

except Exception as e:
    print(e)
    # import traceback
    # traceback.print_exc()
print("Fin")
input()
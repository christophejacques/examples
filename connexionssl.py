import urllib.request as ur
import urllib.parse as up
import ssl
import hashlib
import socket

url = "https://echange.asp-public.fr/osiris_lfi/Actualisation_Financeurs.txt"
# url = "http://perso.numericable.com/cjacques/ASP/Actualisation_Financeurs.txt"


def exemple1():
    controle = "SSL"
    handler = ur.BaseHandler()

    if controle == "IGNORE_SSL":
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handler = ur.HTTPSHandler(context=ctx)

    elif controle == "SSL":
        # Active le controle de certificat SSL
        handler = ur.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLS))

    opener = ur.build_opener(handler)
    # opener = ur.build_opener()
    print("openurl =", url)
    try:
        # f = ur.urlopen(url, timeout=2)
        f = opener.open(url, timeout=10)
    except Exception as e:
        print("Error:", e)
        if hasattr(e, "code"):
            print("code:", e.code)
        print("args:", e.args)
        if e.args:
            print("args:", e.args[0])
        if hasattr(e, "reason"):
            print("reason:", e.reason)
        exit(1)

    opener.close()

    financeurs = {}
    for ligne in f: 
        code, *libs = ligne[:-1].decode().split("|")
        if code.isnumeric():
            financeurs[code] = libs
        else:
            financeurs["00000"] = libs[0].strip(), libs[1].strip()
    f.close()

    for fin in sorted(financeurs)[:5]:
        print(fin, ": {1:20s} , {0}".format(*financeurs[fin]))


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def exemple2():
    fprint(url)
    urlp = up.urlparse(url)

    scheme = urlp.scheme
    host = urlp.hostname
    port = urlp.port or 443

    serveur = (host, port)
    fprint(serveur)
    print("scheme:", scheme)
    fprint("Récupération du certificat", end=" ")
    certificat = ssl.get_server_certificate(serveur)
    fprint(" Ok")
    fprint("Validation du certificat", end=" : ")

    try:
        print()
        trusted_cert = ssl.PEM_cert_to_DER_cert(certificat)

        conn = socket.create_connection((host, port))
        sock = ssl.wrap_socket(conn)
        current_cert = sock.getpeercert(True)

        pem_cert = ssl.DER_cert_to_PEM_cert(current_cert)       
        if certificat == pem_cert:
            print("- certificat == PEM cert")
        else:
            print("- certificat != PEM cert")

    except Exception:
        fprint("- Certificat invalide !")
        import traceback
        traceback.print_exc()
    else:
        if hashlib.sha1(trusted_cert).digest() == hashlib.sha1(current_cert).digest():
            fprint("- digest : Certificat validé")
        else:
            fprint("- digest : Certificat non valide !")


# exemple1()
exemple2()

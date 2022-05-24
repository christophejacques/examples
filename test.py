import requests
import ssl
import certifi
import urllib
from pprint import pprint


host = "expired.badssl.com"
url = f'https://{host}/'

url = 'https://echange.asp-public.fr/osiris_lfi/Actualisation_Financeurs.txt'
# url = 'https://self-signed.pythontest.net/'

urlp = urllib.parse.urlparse(url)
scheme = urlp.scheme
host = urlp.netloc
path = urlp.path

url = f"{scheme}://{host}{path}"
print(url)

# context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Making a get request
# response = requests.get(url, verify=False)
response = urllib.request.urlopen(url, timeout=5)

if hasattr(response, "status_code") and response.status_code != 200:
    print("Statut:", response.status_code)
if hasattr(response, "status") and response.status != 200:
    print("Statut:", response.status)
financeurs = {}

# print("headers:", response.headers)
print("Content-Type:", response.headers.get("Content-Type"))
print()
if "text/" in response.headers.get("Content-Type"):
    # for i, ligne in enumerate(response.iter_lines()):
    for i, ligne_encodee in enumerate(response.readlines()):
        try:
            ident, libelle, code = ligne_encodee.decode().strip("\n").split("|")
            if ident.isnumeric():
                financeurs[ident] = (code, libelle)
        except Exception:
            print(ligne_encodee.decode().strip("\n"))
        if i > 6: 
            break

elif "json" in response.headers.get("Content-Type"):
    print(response.json)

pprint(financeurs)
exit()

print()
address = host, 443
with open(certifi.where()) as f:
    try:
        cert = ssl.get_server_certificate(address, ca_certs=f.name)
    except ssl.SSLCertVerificationError:
        print("> ssl.SSLCertVerificationError")
    except Exception:
        from traceback import print_exc
        print_exc()
    else:
        print("Certificat certifié")

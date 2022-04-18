import os
import requests
import ssl
import certifi
import urllib

url = 'https://expired.badssl.com/'
url = 'https://echange.asp-public.fr/'
# url = 'https://self-signed.pythontest.net/'
host = urllib.parse.urlparse(url).netloc

# Making a get request
response = requests.get(url, verify=False)
 
print(response.status_code)
print(response.connection)
print(dir(response.connection))
print(response.connection.poolmanager)
print(dir(response.connection.poolmanager))
print(response.connection.poolmanager)
print(response.connection.max_retries)

print(response.url)
print(response.encoding)
print(response.cookies)
print(response.headers)
print("Content-Type:", response.headers.get("Content-Type"))
if "text/html" in response.headers.get("Content-Type"):
    print(response.text)
elif "json" in response.headers.get("Content-Type"):
    print(response.json)

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

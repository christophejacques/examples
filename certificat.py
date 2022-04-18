import certifi
import requests


def load():
    print("certificats location:", certifi.where())
    try:
        print('Contrôle de la connection à Github...')
        # test = requests.get('https://api.github.com')
        test = requests.get('https://echange.asp-public.fr')
        print('Connection à Github OK.')

    except requests.exceptions.SSLError:
        print('SSL Error. Ajout des certificats custom au magasin Certifi...')
        cafile = certifi.where()

        exit()
        # supprimer le exit() afin d'importer le nouveau certificat

        with open('certicate.pem', 'rb') as infile:
            customca = infile.read()
        with open(cafile, 'ab') as outfile:
            outfile.write(customca)

        print('Le certificat a été installé')
        print('Vous pouvez relancer le script')


def save(crtPath):
    import win32crypt
    # Flag variables
    CERT_STORE_PROV_SYSTEM = 0x0000000A
    CERT_STORE_OPEN_EXISTING_FLAG = 0x00004000
    CRYPT_STRING_BASE64HEADER = 0x00000000
    CERT_SYSTEM_STORE_CURRENT_USER_ACCOUNT = 1 << 16
    X509_ASN_ENCODING = 0x00000001
    CERT_STORE_ADD_REPLACE_EXISTING = 3
    CERT_CLOSE_STORE_FORCE_FLAG = 0x00000001

    # replace with your certificate file path
    # crtPath = "D:\\certificates\\cert_file.crt"

    with open(crtPath, 'r') as f:
        cert_str = f.read()

    cert_byte = win32crypt.CryptStringToBinary(cert_str, CRYPT_STRING_BASE64HEADER)[0]
    store = win32crypt.CertOpenStore(CERT_STORE_PROV_SYSTEM, 0, None, CERT_SYSTEM_STORE_CURRENT_USER_ACCOUNT|CERT_STORE_OPEN_EXISTING_FLAG, "ROOT")
        
    try:
        store.CertAddEncodedCertificateToStore(X509_ASN_ENCODING, cert_byte, CERT_STORE_ADD_REPLACE_EXISTING)
    finally:
        store.CertCloseStore(CERT_CLOSE_STORE_FORCE_FLAG)


if __name__ == "__main__":
    load()

import requests
from os import environ
from pprint import pprint


authentication: dict = {}


def decode_header(response):
    for header in response.headers:
        print("-", f"{header:30.30}", ":", end=" ")

        if ";" in response.headers[header]:
            print()
            for cookie in response.headers[header].split(";"):
                print("    -", cookie.strip())
        else:
            print(response.headers[header])

    print(response.content.decode("ansi"))
    print(response.url)


def check_environnement():
    vars_env: dict = {
        "client_id": "API_SIRET_CLIENT_ID",
        "client_secret": "API_SIRET_CLIENT_SECRET"
    }
    for variable in vars_env:
        authentication[variable] = environ.get(vars_env[variable])

    if all(authentication.values()):
        print("Environnement charge")

    else:
        print("Erreur de configuration, Variable(s) d'environnement non valide :")
        for variable in vars_env:
            if not authentication[variable]:
                print("-", vars_env[variable])
        print()
        exit()


# Declaration/Initialisation des variables
siret_insee: str = "33447335200816"

# URL de l'API
url_token: str = "https://api.insee.fr/token"
url_siret: str = f"http://api.insee.fr/entreprises/sirene/V3/siret/{siret_insee}"


def get_token():
    # Paramètres de la requête
    data: dict = {
        "grant_type": "client_credentials",
    }
    data.update(authentication)

    print("Recuperation du token pour l'API")
    # Effectuez la requête
    response = requests.post(url_token, data=data)

    # Vérifiez le code de réponse
    if response.status_code == 200:
        # Le token est dans le corps de la réponse
        token = response.json().get("access_token", "")
        print("token:", token)
    else:
        # Une erreur s'est produite
        print(response.status_code)
        print(response.text)
        exit()

    return token


def get_siret():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {get_token()}",
    }

    print("\nRecherche des infos pour le SIRET:", siret_insee)
    response = requests.get(url_siret, headers=headers)

    if response.status_code == 200:
        # les informations sont dans le JSon
        response = response.json().get("etablissement", {}).get("uniteLegale")

    else:
        # Une erreur s'est produite
        print("status:", response.status_code)
        print("Reponse:", response.content)
        exit()

    return response


check_environnement()
pprint(get_siret())

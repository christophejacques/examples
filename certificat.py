import certifi
import requests

import pip_system_certs.wrapt_requests  # Force l'intégration
import ssl
import socket


def get_certificate_pem(hostname, port=443):
    # Création d'un contexte SSL par défaut
    context = ssl.create_default_context()
    
    # Établissement de la connexion socket
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # Récupération du certificat au format binaire (DER)
            cert_der = ssock.getpeercert(binary_form=True)
            
            # Conversion du format binaire vers le format PEM
            cert_pem = ssl.DER_cert_to_PEM_cert(cert_der)
            return cert_pem


if __name__ == "__main__":
    # Exemple d'utilisation
    # host = "google.com"
    host = "www.maif.fr"
    try:
        pem_data = get_certificate_pem(host)
        print(f"Certificat pour {host} :\n")
        print(pem_data)
        
    except Exception as e:
        print(f"Erreur : {e}")
        raise

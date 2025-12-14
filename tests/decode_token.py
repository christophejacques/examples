import json
import base64


def decode_jwt_unsafe(bearer_auth_header):
    """
    Décode un JWT sans vérifier sa signature ni son expiration.
    Méthode NON SÉCURISÉE, uniquement pour l'inspection des données.
    """

    # 1. Extraction du jeton (Token)
    if not bearer_auth_header.startswith("Bearer "):
        raise ValueError("L'en-tête n'est pas au format Bearer.")
        
    token = bearer_auth_header.split(" ")[1]
    
    # 2. Séparation des trois parties
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
    except ValueError:
        raise ValueError("Le Jeton (Token) n'est pas au format JWT (Header.Payload.Signature).")

    # 3. Fonction d'aide pour le décodage Base64 URL Safe
    # Le Base64 utilisé dans les JWT est "URL safe" et peut nécessiter un padding.
    def decode_base64_url_safe(data):
        # Ajoute le padding manquant (si nécessaire)
        padding = '=' * (4 - (len(data) % 4))
        # Décode en Base64 URL Safe, puis en bytes, puis en chaîne JSON
        decoded_bytes = base64.urlsafe_b64decode(data + padding)
        return decoded_bytes.decode('utf-8')

    # 4. Décoder l'En-tête (Header) et le Contenu (Payload)
    header_json_str = decode_base64_url_safe(header_b64)
    payload_json_str = decode_base64_url_safe(payload_b64)
    
    # 5. Conversion des chaînes JSON en dictionnaires Python
    header = json.loads(header_json_str)
    payload = json.loads(payload_json_str)
    
    return header, payload, signature_b64


def decode_baerer_auth(auth_header: str):

    try:
        header_data, payload_data, signature = decode_jwt_unsafe(auth_header)
                
        print("\n## Contenu (Payload) :")
        print(json.dumps(payload_data, indent=2))
        
        print(f"\n## Signature (NON VÉRIFIÉE)")
        print(signature)
        
    except ValueError as e:
        print(f"❌ Erreur lors du décodage : {e}")
    except Exception as e:
        print(f"❌ Une erreur inattendue s'est produite : {e}")


def decode_basic_auth(token: str):
    try:            
        # On prend la partie après "Basic " (soit l'index 1 après le split)
        encoded_credentials = token.split(" ")[1]
        
        # 2.2. Décoder la chaîne Base64 (elle est encodée en bytes)
        # L'argument `altchars=None` est la valeur par défaut
        decoded_bytes = base64.b64decode(encoded_credentials)
        
        # 2.3. Convertir les bytes décodés en une chaîne de caractères (string)
        # Généralement, l'encodage est UTF-8 ou Latin-1
        decoded_string = decoded_bytes.decode('utf-8')
        
        # 2.4. Séparer l'utilisateur et le mot de passe
        # La chaîne décodée est toujours au format "utilisateur:mot_de_passe"
        username, password = decoded_string.split(":", 1)
        
        # --- 3. Affichage des résultats ---
        print(f"En-tête reçu : {token}")
        print("-" * 30)
        print(f"Identifiants Base64 : {encoded_credentials}")
        print(f"Chaîne décodée : {decoded_string}")
        print(f"Utilisateur : **{username}**")
        print(f"Mot de passe : **{password}**")

    except ValueError as e:
        print(f"Erreur de format : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite lors du décodage : {e}")    


decode_functions: dict = {
    "basic": decode_basic_auth,
    "bearer" : decode_baerer_auth
}


def main():
    tokens: list = list()

    # tokens.append("Basic bW9udXRpbGlzYXRldXI6bW9ubW90ZGVwYXNzZQ==")
    tokens.append("Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJGOS0yZ2NwNTBqSWZna2NCZ2w1NEJHemdfdkFGZXlEVm1xbFItSDlObHJNIn0.eyJleHAiOjE3NjQ4NTMzOTIsImlhdCI6MTc2NDg1MzA5MiwiYXV0aF90aW1lIjoxNzY0ODUzMDkxLCJqdGkiOiI4NmU2NjRmNy0xZWI2LTQ3M2UtYTE2ZS04NDI0ODNmNjc1NDMiLCJpc3MiOiJodHRwczovL2F1dGhrZXlkZXYuYXNwLXB1YmxpYy5mci9pYW0vcmVhbG1zL3JjaXBhYy1pIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjVmMTkwODM3LTIxNjgtNGVkZC05OTZlLTI2Y2RmOGIyNDkyYiIsInR5cCI6IkJlYXJlciIsImF6cCI6IjE5OTk2NmU2MGY5NGE4NzkyNmY4MDdhZTMzMDhkZDBhIiwibm9uY2UiOiJkOWFkYzMwYi04NmI5LTQ3YTItYmJiMC1mNDllMDVjODI2ZGMiLCJzaWQiOiI1ZTRiNzljMS03NWUxLTQyMjctYWE3MC1hNzI1ZTk3MmFkYjYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vcmNpcGFjLWludC5hc3AtcHVibGljLmZyIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJyZHI0LXJjaXBhYy11c2VyIiwicmRyNC1yY2lwYWMtYWRtaW4iLCJkZWZhdWx0LXJvbGVzLXJjaXBhYy1pIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJjb2RlUGFydGVuYWlyZSI6IlBBQyIsImRhdGUtZGVybmllcmUtY29ubmV4aW9uIjoiMjAyNS0xMi0wMlQxMDoxNjo0Ny4wMDArMDE6MDAiLCJuYW1lIjoiQ2hyaXN0b3BoZSBKQUNRVUVTIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiY2hyaXN0b3BoZS5qYWNxdWVzMSIsInNlc3Npb25fc3RhdGUiOiI1ZTRiNzljMS03NWUxLTQyMjctYWE3MC1hNzI1ZTk3MmFkYjYiLCJnaXZlbl9uYW1lIjoiQ2hyaXN0b3BoZSIsImZhbWlseV9uYW1lIjoiSkFDUVVFUyIsImVtYWlsIjoiY2hyaXN0b3BoZS5qYWNxdWVzMUBhc3AtcHVibGljLmZyIn0.QdYnfGAMLnyXV0D8jRUvG0_5ksUpTVuuDwyjx8Nmgw3YnL9ODYbmGubNU-3cqcYuHp1kWwK7gdgHP4wlRXb_ZskSRZIPV7NvfQ6sd7yQkQQleBWE2MUDp7lrH2dAIK36df7ElY1a4F4VJ17UjoMfHzJxsLnXSnNA6grS3zSjJGKLdGXPURkdzLpp-WFn17fnIzjcEpSwsuX6UmdMqPNF9vgTCtCfznl-0bBCrXul2MYPaZmRhoqlGhReAZhctHq2oAMg4P_NBbIDw-pFJ_FExfUzQRgN1GLVF6Bhn19Cjf8l-I9CVGx3uDAaxfF6it9adhTvS-_LLVCQojZZDuFhPw")
    for token in tokens:
        decode_functions.get(
            token.split()[0].lower(), 
            lambda x: x)(token)


main()

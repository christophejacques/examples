from typing import Protocol, List, runtime_checkable


@runtime_checkable
class Volant(Protocol):
    def voler(self) -> str: ...

class Avion:
    def voler(self) -> str:
        return "L'avion décolle avec ses réacteurs."

class Autruche:
    def courir(self) -> str:
        return "L'autruche court très vite."

# --- Vérification au moment de l'exécution ---
objets = [Avion(), Autruche()]

for obj in objets:
    # isinstance() n'est utilisable que si le decorateur
    # @runtime_checkable est applique a la classe Protocol (Volant)
    if isinstance(obj, Volant):
        print(f"Compatible : {obj.voler()}")
    else:
        print(f"Incompatible : {type(obj).__name__} ne sait pas voler.")



# 1. Définition du Protocole
class MoyenPaiement(Protocol):
    def payer(self, montant: float) -> bool: ... 

# 2. Classes concrètes (pas besoin d'hériter de MoyenPaiement !)
class CarteBancaire:
    def payer(self, montant: float) -> bool:
        print(f"Paiement de {montant}€ par Carte Bancaire:", end="")
        return False

class PayPal:
    def payer(self, montant: float) -> bool:
        print(f"Paiement de {montant}€ via PayPal:", end="")
        return False

class CartePass:
    def payer(self, montant: float) -> bool:
        print(f"Paiement de {montant}€ via carte PASS:", end="")
        return True

# Cette classe est invalide car elle n'a pas la méthode 'payer'
class Especes:
    def donner_billet(self):
        print("Billet donné.")

# 3. Utilisation avec le typage
def encaisser_panier(elements: List[MoyenPaiement], total: float) -> bool:
    for moyen in elements:
        if moyen.payer(total):
            return True
        else:
            print("ECHEC")
    return False

# Test
mes_paiements: List[MoyenPaiement] = [PayPal(), CarteBancaire(), CartePass()]
if encaisser_panier(mes_paiements, 42.50):
    # paiement bien encaisse
    print("OK")
else:
    print("Le paiement n'a pu être encaissé")

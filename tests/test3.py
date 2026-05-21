def printf(*args):
    msg: str = ""
    for arg in args:
        msg += f"{arg} "
    return f"{msg.strip()}"


def siErreur(*switch_erreur):
    def conteneur(fonction):
        def wrapper(*args, **kwargs):
            try:
                resultat = fonction(*args, **kwargs)
                return resultat

            except Exception as erreur:
                if isinstance(erreur, switch_erreur[0]):
                    if callable(switch_erreur[1]):
                        return switch_erreur[1](erreur)
                    else:
                        return switch_erreur[1]

                raise erreur

        return wrapper
    return conteneur


# @siErreur(ZeroDivisionError, "Infinity")
@siErreur(ZeroDivisionError, printf)
# @siErreur(IndexError, "Infinity")
def division(a, b) -> float:
    return a / b


print("=>", division(5, 2))
print("=>", division(5, 0))


class Entier:
    def __init__(self, valeur):
        self.valeur = valeur

    def __truediv__(self, other) -> tuple[int, int]:
        if other == 0:
            return 0, self.valeur

        resultat: int = self.valeur // other
        reste = self.valeur - resultat * other
        return resultat, reste


t = Entier(13)
print(t / 0)
print(t / 2)

import re


def extension(chaine: str) -> str:
    return chaine.rpartition(".")[-1]


def filename(chaine: str) -> str:
    return chaine.rpartition(".")[0]


def string_format(chaine: str, **kwargs) -> str:
    expressions = re.findall('({[^}]*})', chaine)
    for expression in expressions:
        nom_variable, *fonctions = expression.strip("{}").split(":")
        valeur: str = kwargs.get(nom_variable, "")
        for fonction in fonctions:
            if hasattr(valeur, fonction):
                valeur = getattr(valeur, fonction)()
            else:
                valeur = eval(f"{fonction}('''{valeur}''')")

        chaine = chaine.replace(expression, valeur, 1)

    return chaine


print(string_format("0 https://javgg.net/jav/", img_name="AzErTy.jpg"))
print(string_format("1 https://javgg.net/jav/{img_name:lower:filename}/", img_name="AzErTy.jpg"))
print(string_format("2 https://javgg.net/jav/{img_name:lower:filename}/" + 
    "{img_name:extension:upper}/", img_name="AzErTy.jpg"))
print(string_format("3 {scheme:lower}://{uri}/{img_name:capitalize}", 
    scheme="https",
    uri="www.google.fr",
    img_name="AzErTy.jpg"))


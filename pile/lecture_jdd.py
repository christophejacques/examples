#!/usr/bin/env python3
# Type de données :
# -----------------
# databases: dict[int, dict] {
#   wait: dict[str, list] {
#     nom_database: list[tuple] [
#       (index: int, contenu: str), (...), ...] 
#   }
# }

def lecture_jdd(nom_fichier: str) -> dict[int, dict[str, list]]:
    databases: dict[int, dict[str, list]] = dict()

    with open(nom_fichier, encoding="utf-8") as jdd:
        database: str = ""
        wait: str = ""
        iwait: int = 0
        data: str = "\n"
        ligne: str = ""

        while len(data) > 0:
            data = jdd.readline()
            if len(data) <= 1:
                continue

            ligne = data.strip()
            if ligne == "":
                continue

            match ligne:
                case _ if ligne.startswith("#"):
                    # commentaire
                    continue

                case section if ligne.startswith("["):
                    # Nouvelle section (temps d'attente, type database)
                    wait, database = section.strip("[]").split(",")

                    iwait = int(wait)
                    if databases.get(iwait) is None:
                        databases[iwait] = dict()

                    database = database.strip().upper()
                    if databases[iwait].get(database) is None:
                        databases[iwait][database] = list()

                case _:
                    # Donnees
                    index, content, *statut = ligne.split(",")
                    databases[iwait][database].append(
                        (int(index), content.strip(), " ".join(statut).strip()))

    return databases


if __name__ == "__main__":
    databases = lecture_jdd("jeu_donnees2.conf")
    for iwait in databases:
        print(f"{iwait}s:")
        for database in databases[iwait]:
            print(" ", database, "=", databases[iwait][database])

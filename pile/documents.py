import datetime as dt
from typing import Optional, Dict


class Document:
    # Classe de Base pour définir les documents

    TZ: dt.timezone

    ident: int
    header: Dict
    payload: Dict

    def __str__(self) -> str:
        statut = self.header.get('statut', None)
        statut = "" if statut is None else f"{statut:7} - "

        contenu = f"{self.payload.get('content', '')}"

        maintenant = dt.datetime.now(Document.TZ)
        temps_traitement = (maintenant - self.header.get("date_creation", maintenant)).total_seconds()
        if temps_traitement == 0:
            temps_traitement = ""
        else:
            temps_traitement = f" - (Temps: {temps_traitement:.2f}s)"

        return f"{statut}Doc {self.ident}: {contenu}{temps_traitement}"

    @classmethod
    def init(cls):
        # Calcul de la timezone a ne faire qu'une seule fois
        heure_utc = dt.datetime.now(dt.UTC).hour
        heure_locale = dt.datetime.now().hour
        delta_hour = heure_locale - heure_utc

        cls.TZ = dt.timezone(dt.timedelta(hours=delta_hour))
        # print(f"Initialisation de la timezone: +{delta_hour}h00")


Document.init()


class DocumentAMQ(Document):

    def __init__(self, ident: int, content: str):
        self.ident = ident

        # creation du header du document
        self.header = dict()

        # Ajout de la date de creation du document
        maintenant = dt.datetime.now(Document.TZ)
        self.header.update({"date_creation": maintenant})

        # Mise a jour du contenu du payload
        self.payload = {"content": content}


class DocumentElastic(Document):

    def __init__(self, ident: int, content: str, header: Optional[Dict] = None):
        self.ident = ident

        # creation du header du document
        if header is None:
            self.header = dict()
        else:
            self.header = header

        # Mise a jour du contenu du payload
        self.payload = {"content": content}


if __name__ == "__main__":
    print(f"{Document.TZ=}")
    print(f"{DocumentAMQ.TZ=}")
    print(f"{DocumentElastic.TZ=}")

    print("AMQ", DocumentAMQ(1, "Premier doc"))
    print("ELAS", DocumentElastic(1, "Premier doc"))
    print("ELAS", DocumentElastic(2, "Doc integre"))
    print("ELAS", DocumentElastic(2, "Doc rejete", header={"statut": "REJETE"}))

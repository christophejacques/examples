import datetime as dt
from typing import List, Dict, Optional
from time import sleep, perf_counter
from threading import Thread


def fprint(*args, showTime: bool = True, **kwargs):
    if showTime:
        # affichage de l'heure en premier avant le reste
        maintenant = dt.datetime.now(Document.TZ).isoformat()
        print(f"{maintenant} -", *args, **kwargs, flush=True)
    else:
        print(*args, **kwargs, flush=True)


class Document:
    TZ: dt.timezone

    ident: int
    header: Dict
    payload: Dict

    def __init__(self, ident: int, content, statut: Optional[Dict] = None):
        self.ident = ident

        # creation du header du document
        self.header = dict()

        # Ajout de la date de creation du document
        maintenant = dt.datetime.now(Document.TZ)
        self.header.update({"date_creation": maintenant})

        # Mise a jour du contenu du payload
        self.payload = {"content": content}

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
        date_utc = dt.datetime.now(dt.UTC)
        heure_utc = date_utc.hour

        heure_locale = dt.datetime.now().hour
        delta_hour = heure_locale - heure_utc

        tz = dt.timezone(dt.timedelta(hours=delta_hour))
        cls.TZ = tz

        # fprint(f"Initialisation de la timezone: +{delta_hour}h00")


class ActiveMQ:
    __content: List[Document]

    def __init__(self, name: str):
        self.__content = list()
        self.name = name

    def add(self, document: Document, retry_min: int = 0, retry_sec: int = 0) -> None:
        if document.header.get("release") is None and retry_min+retry_sec > 0:
            # calcul de la datetime de liberation s'il y a un retry_sec ou retry_min
            release_time = dt.timedelta(minutes=retry_min, seconds=retry_sec) + \
                dt.datetime.now(Document.TZ)

            document.header.update({"release": release_time})

        # ajout du document dans la liste (file)
        self.__content.append(document)

    def isEmpty(self) -> bool:
        return len(self.__content) <= 0

    def pop(self) -> Optional[Document]:
        if self.isEmpty():
            return None

        doc = self.__content.pop(0)
        return doc

    def view(self) -> Optional[Document]:
        if self.isEmpty():
            return None

        doc = self.__content[0]
        return doc

    def has_document(self, ident: int) -> bool:
        for document in self.__content:
            if ident == document.ident:
                return True

        return False

    def __len__(self) -> int:
        return len(self.__content)

    def __str__(self) -> str:
        contenu = [doc.ident for doc in self.__content]
        return f"{self.name} " + str(contenu)


class sigmaGestionListener:

    # Temps de retention d'un document dans la file de retry avant liberation
    RETRY_SEC_PERC33: int = 10

    # Nombre de retry maximal 
    RETRY_NBR_PERC33: int = 2
    DEBUG: bool = False

    def __init__(self):

        Document.init()

        self.amq_perf3 = ActiveMQ("PERF3")
        self.amq_perc33 = ActiveMQ("PERC33")
        self.amq_perc33_retry = ActiveMQ("RETRY")

        # Jeu de données

        #  Flux PERF3
        fprint("Ajout des documents PERF3 du jeu de donnees: 1, 3, 5, 6 et 8")
        for index, nombre in [(1, "Un"), (3, "Trois"), (5, "Cinq"), (6, "Six"), (8, "Huit")]:
            self.amq_perf3.add(Document(index, nombre))

        # Flux PERC33
        fprint("Ajout des documents PERC33 du jeu de donnees: 1 à 5")
        for index, nombre in [(1, "Un"), (2, "Deux"), (3, "Trois"), (4, "Quatre"), (5, "Cinq")]:
            document = Document(index, nombre)
            self.amq_perc33.add(document)
            fprint(f" +  Document ajouté: {document}")

        # ajout du 2eme jeu de donnees dans un tache
        # devant s'executer dans 7s
        Thread(target=self.add_decale).start()

    def add_decale(self):
        sleep(7)
        document = Document(2, "Deux")
        self.amq_perf3.add(document)
        fprint(f" +  Document PERF3 ajouté: {document}")

        fprint("Ajout des documents du jeu de donnees: 6, 7 et 8")
        for index, nombre in [(6, "Six"), (7, "Sept"), (8, "Huit")]:
            document = Document(index, nombre)
            self.amq_perc33.add(document)
            fprint(f" +  Document ajouté: {document}")

    def print(self, **kwargs):
        # personnalisation de l'affichage des deplacement des documents
        if kwargs.get("ajout"):
            aj_sup = "(+)" 
        elif kwargs.get("suppr"):
            aj_sup = "(-)" 
        else:
            aj_sup = "   " 

        if kwargs.get("to_retry"):
            deplace = "->>" 
        elif kwargs.get("to_perc"):
            deplace = "<<-" 
        else:
            deplace = "   " 

        chaine = f"{self.amq_perc33}"
        message = f"{aj_sup} {chaine:20}{deplace} "
        message += f"{self.amq_perc33_retry}"
        fprint(message)

    def check_perf3(self, document: Document) -> None:
        # regarde si le document existe dans la file PERF3
        if self.amq_perf3.has_document(document.ident):
            # le document est trouve => on l'INTEGRE
            document.header.update({"statut": "INTEGRE"})
        else:
            # le document n'est pas trouve => on le REJETE
            document.header.update({"statut": "REJETE"})

    def check_perc33(self) -> None:
        doc = self.amq_perc33.pop()
        if doc is None:
            fprint("    /!\\ PERC34 Queue is empty")
            return

        # code permettant de mettre à jour l'état INTEGRE/REJETE du flux
        self.check_perf3(doc)

        if doc.header.get("statut", "?") == "REJETE":
            # mise en place des retry que sur les flux REJETE
            retry_sec: int = sigmaGestionListener.RETRY_SEC_PERC33

            # calcul du nombre de retry à faire
            # initialisé à RETRY_NBR_PERC33 si variable absente
            # sinon decrementation de 1
            nb_retries = doc.header.get("retry", sigmaGestionListener.RETRY_NBR_PERC33)
            if nb_retries > 0:
                nb_retries -= 1
                doc.header.update({"retry": nb_retries})

                if self.DEBUG:
                    fprint(f"    >> GoTo RETRY ({1+nb_retries} fois), Doc {doc.ident}, {doc.payload}")

                # envoi sur la file des retry
                self.amq_perc33_retry.add(doc, retry_sec=retry_sec)
                return

        # si on arrive ici, cela signifi que l'on a dépiller le document
        # et qu'il n'a pas été envoyé vers la file de retry
        # donc l'affichage indique uniquement sont contenu
        fprint(f"{doc}")

    def check_retry(self) -> None:
        # on regarde le document suivant sans le supprimer
        doc = self.amq_perc33_retry.view()
        if doc is None:
            fprint("    /!\\ Retry Queue is empty")
            return

        # on regarde s'il reste du temps avant la liberation du document
        maintenant = dt.datetime.now(Document.TZ)
        if maintenant < doc.header.get("release", maintenant):
            # le temps de renvoyer le document vers la file initiale
            # n'est pas encore arrive

            # on calcul le temps restant à attendre
            duree = (doc.header.get("release") - maintenant).total_seconds()
            if self.DEBUG:
                fprint("        * wait Doc", doc.ident, doc.payload, "for", duree, "seconds ...")

            # on attend donc uniquement le temps restant
            sleep(duree)
            if self.DEBUG:
                fprint("    << Back to PERC33, Doc", doc.ident, doc.payload)

        # si on arrive ici, cela signifie
        # qu'il faut renvoyer immediatement le document vers la file initiale
        doc = self.amq_perc33_retry.pop()

        # suppression de la datetime de liberation du document 
        # de la file des retry
        doc.header.pop("release", 0)

        # envoi du document sur la file initiale
        self.amq_perc33.add(doc)


class Main:

    def __init__(self):
        self.perc33 = None
        self.retry = None
        self.prev_nb_perc33: int = 0
        self.prev_nb_retry: int = 0
        self.nb_perc33: int = 0
        self.nb_retry: int = 0

        # initialisation du service
        self.sg = sigmaGestionListener()

    def print_piles(self):
        # affiche le contenu des piles si on est pas en mode DEBUG
        if sigmaGestionListener.DEBUG:
            pass
            return 

        self.nb_perc33 = len(self.sg.amq_perc33)
        self.nb_retry = len(self.sg.amq_perc33_retry)

        if self.prev_nb_perc33 != self.nb_perc33 or self.prev_nb_retry != self.nb_retry:
            # n'affiche les pile que si l'une d'elle a changee

            # calcul des variables permettant de personnaliser l'affichage
            ajout = (self.prev_nb_perc33 < self.nb_perc33 and self.prev_nb_retry == self.nb_retry)
            suppression = (self.prev_nb_perc33 > self.nb_perc33 and self.prev_nb_retry == self.nb_retry)
            to_retry = (self.prev_nb_perc33 > self.nb_perc33 and self.prev_nb_retry < self.nb_retry)
            to_perc = (self.prev_nb_perc33 < self.nb_perc33 and self.prev_nb_retry > self.nb_retry)

            self.sg.print(ajout=ajout, suppr=suppression, to_retry=to_retry, to_perc=to_perc)

        self.prev_nb_perc33 = self.nb_perc33
        self.prev_nb_retry = self.nb_retry

    def run(self):
        debut = perf_counter()

        # boucle tant que 
        #     l'une des 2 files n'est pas vide
        #     ou que le traitement des retry n'est pas fini
        while (not self.sg.amq_perc33.isEmpty() or 
          not self.sg.amq_perc33_retry.isEmpty() or 
          self.retry is not None and self.retry.is_alive()):

            self.print_piles()
            # controle des documents de la file principale
            if not self.sg.amq_perc33.isEmpty():
                if self.perc33 is None or not self.perc33.is_alive():
                    # lancement du traitement en tache de fond
                    self.perc33 = Thread(target=self.sg.check_perc33)
                    self.perc33.start()
                
            self.print_piles()
            # controle des documents de la file des retry
            if not self.sg.amq_perc33_retry.isEmpty():
                if self.retry is None or not self.retry.is_alive():
                    # lancement du traitement en tache de fond
                    self.retry = Thread(target=self.sg.check_retry)
                    self.retry.start()

            # simule le temps de traitement d'un document
            sleep(0.25)

        self.print_piles()

        fin = perf_counter()
        print(f"Temps de traitement: {fin-debut:.2f}s")


if __name__ == "__main__":
    Main().run()

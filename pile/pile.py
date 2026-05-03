import datetime as dt

from time import sleep, perf_counter
from threading import Thread

from documents import DocumentAMQ, DocumentElastic
from databases import ActiveMQ, IndexElastic
from lecture_jdd import lecture_jdd


def fprint(*args, showTime: bool = True, **kwargs):
    if showTime:
        # affichage de l'heure en premier avant le reste
        maintenant = dt.datetime.now(DocumentAMQ.TZ).isoformat()
        print(f"{maintenant} -", *args, **kwargs, flush=True)
    else:
        print(*args, **kwargs, flush=True)


class sigmaGestionListener:

    # Temps de retention d'un document dans la file de retry avant liberation
    RETRY_SEC_PERC33: int = 10

    # Nombre de retry maximal 
    RETRY_NBR_PERC33: int = 2
    DEBUG: bool = False

    # définition des objets auxquels la classe doit accéder
    # index Elastc
    axone_perf3: IndexElastic

    # collections activeMQ
    amq_perc33: ActiveMQ
    amq_perc33_retry: ActiveMQ

    def __init__(self):

        # simule la route PERF3 dans l'index Elastic 
        self.axone_perf3 = IndexElastic("PERF3")

        # creation des 2 files activeMQ
        self.amq_perc33 = ActiveMQ("PERC33")
        self.amq_perc33_retry = ActiveMQ("RETRY")

        # Chargement des jeux de données
        self.threads: list = list()
        self.init_fichier()

    def load_datas(self, wait: int, datas: dict) -> None:
        # Mise en pause s'il s'agit d'un chargement différé
        sleep(wait)

        for database in datas:
            #  Documents Elastic equivalent route PERF3
            if database == "INDEXELASTIC":
                fprint("Ajout des documents PERF3 du jeu de donnees: ", end="")
                for index, nombre in datas[database]:
                    fprint(index, showTime=False, end=", ")
                    self.axone_perf3.add(DocumentElastic(index, nombre))
                print()

            # Documents activeMQ utilisés pour la route PERC33
            elif database == "ACTIVEMQ":
                fprint("Ajout des documents PERC33 du jeu de donnees: ")
                for index, nombre in datas[database]:
                    document = DocumentAMQ(index, nombre)
                    self.amq_perc33.add(document)
                    fprint(f" +  Document ajouté: {document}")

    def init_fichier(self) -> None:
        # Initialisation des Jeux de données
        # depuis un fichier
        donnees = lecture_jdd()

        #  chargement des données avant lancement du processus de traitement
        for wait in donnees:
            databases = donnees.get(wait, {})
            if wait == 0:
                # Chargement du Jeu de données initial
                self.load_datas(0, databases)
            else:
                # ajout des autres jeux de donnees dans une tache
                # devant s'executer dans 'wait' secondes
                thread = Thread(target=self.load_datas, args=(wait, databases))
                thread.start()
                self.threads.append(thread)

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
        message = f"{aj_sup} {chaine:24}{deplace} "
        message += f"{self.amq_perc33_retry}"
        fprint(message)

    def check_perf3(self, document: DocumentAMQ) -> None:
        # regarde si le document existe dans la file PERF3
        if self.axone_perf3.has_document(document.ident):
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
        # en regardant s'il existe dans la file PERF3
        self.check_perf3(doc)

        if doc.header.get("statut") == "REJETE":
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

                # calcul du temps d'attente
                release_time = dt.timedelta(minutes=0, seconds=retry_sec) + \
                    dt.datetime.now(DocumentAMQ.TZ)

                # Mise à jour du temps d'attente dans le document
                doc.header.update({"release": release_time})

                # envoi sur la file des retry
                self.amq_perc33_retry.add(doc)
                return

        # si on arrive ici, cela signifi que l'on a dépilé le document
        # et qu'il n'a pas été envoyé vers la file de retry
        # donc l'affichage indique uniquement sont contenu
        fprint(f"{doc}")

    def check_retry(self) -> None:
        # on regarde le premier document sans le supprimer
        doc = self.amq_perc33_retry.view()
        if doc is None:
            fprint("    /!\\ Retry Queue is empty")
            return

        # on regarde s'il reste du temps avant la liberation du document
        maintenant = dt.datetime.now(DocumentAMQ.TZ)
        release_time = doc.header.get("release", maintenant)
        if maintenant < release_time:
            # le temps de renvoyer le document vers la file initiale
            # n'est pas encore arrive

            # on calcul le temps restant à attendre
            duree = (release_time - maintenant).total_seconds()
            if self.DEBUG:
                fprint("        * wait Doc", doc.ident, doc.payload, "for", duree, "seconds ...")

            # on attend donc uniquement le temps restant
            sleep(duree)
            if self.DEBUG:
                fprint("    << Back to PERC33, Doc", doc.ident, doc.payload)

        # si on arrive ici, cela signifie
        # qu'il faut renvoyer immediatement le document vers la file initiale
        doc = self.amq_perc33_retry.pop()
        if doc is None:
            return

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
        #     ou que le traitement des chargements des jdd n'est pas fini
        while (not self.sg.amq_perc33.isEmpty() or 
          not self.sg.amq_perc33_retry.isEmpty() or 
          (self.retry is not None and self.retry.is_alive()) or 
          any([thread.is_alive() for thread in self.sg.threads])):

            self.print_piles()
            # traitement des documents de la file principale
            if not self.sg.amq_perc33.isEmpty():
                if self.perc33 is None or not self.perc33.is_alive():
                    # lancement du traitement en tache de fond
                    self.perc33 = Thread(target=self.sg.check_perc33)
                    self.perc33.start()
                
            self.print_piles()
            # traitement des documents de la file des retry
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

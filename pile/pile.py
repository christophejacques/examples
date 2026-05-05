#!/usr/bin/env python3
import datetime as dt

from time import sleep, perf_counter
from threading import Thread
from typing import Optional

from documents import DocumentAMQ, DocumentElastic
from databases import ActiveMQ, IndexElastic
from lecture_jdd import lecture_jdd


class Var:
    debut = perf_counter()


def fprint(*args, showTime: bool = True, **kwargs):
    if showTime:
        # affichage de l'heure en premier avant le reste
        # maintenant = dt.datetime.now(DocumentAMQ.TZ)
        fin = perf_counter()
        duree = fin - Var.debut
        duree_str = f"{duree:.2f}"

        print(f"{duree_str:>6}s -", *args, **kwargs, flush=True)
    else:
        print(*args, **kwargs, flush=True)


class sigmaGestionListener:

    # Temps de retention d'un document dans la file de retry avant liberation
    RETRY_SEC_PERC33: int = 10

    # Nombre de retry maximal 
    RETRY_NBR_PERC33: int = 2
    DEBUG: bool = False

    # définition des objets auxquels la classe doit accéder
    # index Elastic
    axone_perf3: IndexElastic

    # collections activeMQ
    amq_perc33: ActiveMQ
    amq_perc34: ActiveMQ
    amq_perc33_retry: ActiveMQ

    def __init__(self):

        # simule la route PERF3 dans l'index Elastic 
        self.axone_perf3 = IndexElastic("PERF3")

        # creation des 2 files activeMQ
        self.amq_perc33 = ActiveMQ("PERC33")  # Entree
        self.amq_perc34 = ActiveMQ("PERC34")  # Sortie

        # creation de la file activeMQ de retry
        self.amq_perc33_retry = ActiveMQ("RETRY")

        # Chargement des jeux de données
        self.threads: list = list()
        self.init_fichier()

    def load_datas(self, wait: int, datas: dict) -> None:
        # Mise en pause s'il s'agit d'un chargement différé
        sleep(wait)

        for database, liste_docs in datas.items():
            #  Documents Elastic equivalent route PERF3
            if database == "INDEXELASTIC":
                fprint("Ajout des documents PERF3 du jeu de donnees: ", end="")
                for index, libelle, statut in liste_docs:
                    fprint(index, showTime=False, end=", ")
                    if statut == "":
                        self.axone_perf3.add(DocumentElastic(index, libelle))
                    else:
                        self.axone_perf3.add(DocumentElastic(
                            index, libelle, header={"statut": statut}))
                print()

            # Documents activeMQ utilisés pour la route PERC33
            elif database == "ACTIVEMQ":
                fprint("Ajout des documents PERC33 du jeu de donnees: ")
                for index, libelle, *_ in liste_docs:
                    document = DocumentAMQ(index, libelle)
                    self.amq_perc33.add(document)
                    fprint(f" +  Document ajouté: {document}")

    def init_fichier(self) -> None:
        # Initialisation des Jeux de données
        # depuis un fichier
        donnees = lecture_jdd("jeu_donnees.conf")

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
        chaine = f"{self.amq_perc33_retry}"
        message += f"{chaine:18}"
        chaine = f"{self.axone_perf3}"
        message += f"{chaine:28} "
        chaine = f"{self.amq_perc34}"
        message += f"{chaine}"
        fprint(message)

    def check_perf3(self, document: DocumentAMQ) -> None:
        # Recherche du document dans Elastic
        doc_elastic: Optional[DocumentElastic]
        doc_elastic = self.axone_perf3.get_document(document.ident)

        if doc_elastic is None:
            # le document n'est pas trouve => on le renvoi avec l'etat INCONNU
            document.header.update({"statut": "INCONNU"})
            return

        # le document existe dans la file PERF3, 
        # on met a jour le statut du document 
        # avec celle du document trouve
        # si le statut n'est pas renseigné il est mis à INTEGRE par defaut
        document.header.update({"statut": 
            doc_elastic.header.get("statut", "INTEGRE")})
            
    def check_perc33(self) -> None:
        doc = self.amq_perc33.pop()
        if doc is None:
            # ce code ne doit jamais être exécuté
            fprint("    /!\\ PERC34 Queue is empty")
            return

        # code permettant de mettre à jour l'état INTEGRE/REJETE du flux
        # en regardant s'il existe dans la file PERF3
        self.check_perf3(doc)

        if doc.header.get("statut") == "INCONNU":
            # mise en place des retry que sur les flux REJETE
            retry_sec: int = sigmaGestionListener.RETRY_SEC_PERC33

            # calcul du nombre de retry à faire
            # initialisé à RETRY_NBR_PERC33 si variable absente
            # sinon decrementation de 1
            nb_retries = doc.header.get("retry", sigmaGestionListener.RETRY_NBR_PERC33)
            if nb_retries <= 0:
                # c'etait le dernier retry, on rejete donc
                doc.header.update({"statut": "REJETE"})

            else:
                # il reste des retry à faire
                nb_retries -= 1
                doc.header.update({"retry": nb_retries})

                if self.DEBUG:
                    fprint(f"    >> GoTo RETRY ({1+nb_retries} fois), Doc {doc.ident}, {doc.payload}")

                # calcul du temps d'attente
                release_time = dt.timedelta(minutes=0, seconds=retry_sec) + \
                    dt.datetime.now(DocumentAMQ.TZ)

                # Mise à jour du temps d'attente dans le document
                doc.header.update({"release": release_time})

                # Supression du statut 'INCONNU'
                doc.header.pop("statut", None)

                # envoi sur la file des retry
                self.amq_perc33_retry.add(doc)
                return

        # si on arrive ici, cela signifie que l'on a dépilé le document
        # et qu'il n'a pas été envoyé vers la file de retry

        # on l'envoi vers la file de reponse avec son statut calculé
        self.amq_perc34.add(doc)

        # donc l'affichage indique uniquement sont contenu
        fprint(f"{doc}")

    def check_retry(self) -> None:
        # on regarde le premier document sans le supprimer
        doc = self.amq_perc33_retry.view()
        if doc is None:
            # ce code ne doit jamais être exécuté
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
        # on commence par le récupérer en le retirant de la liste des retry
        doc = self.amq_perc33_retry.pop()
        if doc is None:
            # ce code ne doit jamais être exécuté
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

    def has_work_ToDo(self) -> bool:
        # la file retry n'est pas vide
        if not self.sg.amq_perc33_retry.isEmpty():
            return True

        # la file perc33 n'est pas vide
        if not self.sg.amq_perc33.isEmpty():
            return True

        # le traitement des retry n'est pas fini
        if self.retry is not None and self.retry.is_alive():
            return True

        # Supprimer une tache de la liste des taches en cours
        # si celle ci est terminee
        index: int = 0
        last: int = len(self.sg.threads)

        while index < last:
            if self.sg.threads[index].is_alive():
                index += 1
                continue

            self.sg.threads.pop(index)
            last -= 1

        # check le traitement de chargement des jdd restant
        return any([thread.is_alive() for thread in self.sg.threads])

    def run(self):
        Var.debut = perf_counter()

        # boucle tant qu'il reste des choses à faire
        while self.has_work_ToDo():

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
        print(f"Temps de traitement: {fin-Var.debut:.2f}s")


if __name__ == "__main__":
    Main().run()

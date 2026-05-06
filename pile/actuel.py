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
    DEBUG: bool = True

    # définition des objets auxquels la classe doit accéder
    # index Elastic
    axone_perf3: IndexElastic

    # collections activeMQ
    amq_perc33: ActiveMQ
    amq_perc34: ActiveMQ

    def __init__(self):

        # simule la route PERF3 dans l'index Elastic 
        self.axone_perf3 = IndexElastic("PERF3")

        # creation des 2 files activeMQ
        self.amq_perc33 = ActiveMQ("PERC33")  # Entree
        self.amq_perc34 = ActiveMQ("PERC34")  # Sortie

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
        donnees = lecture_jdd("jeu_donnees_rejete.conf")

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

        chaine = f"{self.amq_perc33}"
        message = f"{aj_sup} {chaine:24} "
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
                    fprint(f"    >> Wait ({1+nb_retries} fois), Doc {doc.ident}, {doc.payload}")

                sleep(sigmaGestionListener.RETRY_SEC_PERC33)

                if self.DEBUG:
                    fprint("    << Back to PERC33, Doc", doc.ident, doc.payload)

                # Supression du statut 'INCONNU'
                doc.header.pop("statut", None)

                # envoi a nouveau sur la file
                self.amq_perc33.add(doc)
                return

        # si on arrive ici, cela signifie que l'on a dépilé le document
        # et qu'il n'a pas été envoyé vers la file de retry

        # on l'envoi vers la file de reponse avec son statut calculé
        self.amq_perc34.add(doc)

        # donc l'affichage indique uniquement sont contenu
        fprint(f"{doc}")


class Main:

    def __init__(self):
        self.perc33 = None
        self.prev_perc33 = None

        # initialisation du service
        self.sg = sigmaGestionListener()

    def print_piles(self):
        # affiche le contenu des piles si on est pas en mode DEBUG
        if sigmaGestionListener.DEBUG:
            pass
            return 

        self.perc33 = self.sg.amq_perc33.view()

        if self.prev_perc33 != self.perc33:
            # n'affiche les pile que si l'une d'elle a changee
            self.sg.print()

        self.prev_perc33 = self.perc33

    def has_work_ToDo(self) -> bool:
        # la file perc33 n'est pas vide
        if not self.sg.amq_perc33.isEmpty():
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
                # lancement du traitement en tache de fond
                self.sg.check_perc33()
                
            # simule le temps de traitement d'un document
            sleep(0.25)

        self.print_piles()

        fin = perf_counter()
        print(f"Temps de traitement: {fin-Var.debut:.2f}s")


if __name__ == "__main__":
    Main().run()

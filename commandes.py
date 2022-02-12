from abc import ABCMeta
from os import chdir, system, getcwd, getenv, environ
from os.path import isdir
from disques import Disk
import os
import traceback
import datetime
# from abc import abstractmethod


class CONSTANTE:
    HOME_DIR = getenv("HOMEDRIVE") + getenv("HOMEPATH")  # C:\\Users\\utilisateur"


class VarGlobales:
    old_environ = None
    current_directory = getcwd()
    lastest_directory = current_directory
    sourcing = False


class Parametres(metaclass=ABCMeta):
    
    def __init__(self, args=None):
        self.arguments = args


class Commande(Parametres):
    
    def __init__(self, commande, args: list = []):
        Parametres.__init__(self, args)
        self.commande = commande


class stripDoc:
    
    def __init__(self):
        aide_detaille = False
        doc_commande = self.__class__.__doc__
        self.doc_synthese = ""
        self.doc_detaillee = ""
        if doc_commande:
            for ligne in doc_commande.split("\n"):
                if not aide_detaille:
                    aide_detaille = ligne.strip().lower() == "[aide_detaillee]"
                    if aide_detaille:
                        continue
                
                if not aide_detaille:
                    if self.doc_synthese == "":
                        self.doc_synthese = ligne
                    else:
                        self.doc_synthese += f"\n{ligne}"
                
                else:
                    if self.doc_detaillee == "":
                        self.doc_detaillee = ligne
                    else:
                        self.doc_detaillee += f"\n{ligne}"
            
            if not self.doc_detaillee:
                self.doc_detaillee = self.doc_synthese


class noCommande(stripDoc):
    
    def run(self):
        pass


class exitCommande(stripDoc):
    """Sortie de l'interpréteur de commandes
  [AIDE_DETAILLEE]
  EXIT / QUIT
  
  Permet de quitter l'interpréteur de commande"""
    
    def run(self):
        print("exit", self.arguments)
        OperatingSystem.Running = False


class catCommande(stripDoc):
    """Affiche le contenu d'un fichier
  [AIDE_DETAILLEE]
  CAT nom_fichier
  
  Permet d'afficher le contenu du fichier à l'écran"""
    
    def run(self):
        try:
            for ligne in open(" ".join(self.arguments), 'r'):
                print(ligne, end="")
            print()
        
        except Exception as error:
            print("Error:", error)
            return False
        
        if not VarGlobales.sourcing:
            print()
        return True


class clsCommande(stripDoc):
    """Efface l'écran
    Reinitialise la position du curseur
  [AIDE_DETAILLEE]
  CLS
  
  Efface l'écran
  Reinitialise la position du curseur"""
    
    def run(self):
        system("cls")


class historyCommande(stripDoc):
    """Affiche l'historique des dernières commandes utilisées
  [AIDE_DETAILLEE]
  HISTORY
  
  Affiche la liste des dernières commandes exécutées précédées par un numéro d'ordre"""
    
    def load(self):
        try:
            for ligne in open(os.path.join(CONSTANTE.HOME_DIR, "history"), 'r'):
                OperatingSystem.HISTORIQUE.append(ligne)
                if len(OperatingSystem.HISTORIQUE) > 100:
                    OperatingSystem.HISTORIQUE.pop(0)
        
        except Exception as error:
            print("Error:", error)
            return False
        
        return True
    
    def save(self):
        try:
            with open(os.path.join(CONSTANTE.HOME_DIR, "history"), 'w') as f:
                f.writelines(OperatingSystem.HISTORIQUE)
                
        except Exception as error:
            print("Error:", error)
            return False
        
        return True
    
    def add(self):
        args = " ".join(self.arguments)
        OperatingSystem.HISTORIQUE.append("{} {}\n".format(self.commande, args))
        if len(OperatingSystem.HISTORIQUE) > 100:
            OperatingSystem.HISTORIQUE.pop(0)
    
    def run(self):
        for idx, history in enumerate(OperatingSystem.HISTORIQUE):
            print("{:<3} {}".format(idx, history), end="")
        
        if not VarGlobales.sourcing:
            print()


class sourceCommande(stripDoc):
    """Execution du code contenu dans le fichier passé en paramètre
  [AIDE_DETAILLEE]
  SOURCE nom_fichier
  
  Permet d'exécuter le code contenu dans un fichier de commandes'"""
    
    def run(self):
        if len(self.arguments) != 1:
            print("La commande 'source' doit être utilisée avec 1 seul paramètre\n")
            return False
        
        VarGlobales.old_environ = environ.get("SOURCE_FILE")
        environ["SOURCE_FILE"] = self.arguments[0]
        try:
            for ligne in open(self.arguments[0], 'r'):
                VarGlobales.sourcing = True
                execute_commande(ligne)
        
        except Exception as error:
            print("source error:", error)
        
        if VarGlobales.old_environ:
            environ["SOURCE_FILE"] = VarGlobales.old_environ
        else:
            del environ["SOURCE_FILE"]
            VarGlobales.sourcing = False
        print()


class setCommande(stripDoc):
    """Affichage des variables d'environnement
  [AIDE_DETAILLEE]
  SET [variable=chaine]
  
    variable  Nom de la variable d’environnement.
    chaîne    Chaîne de caractères à affecter à la variable.
  
  SET sans paramètres affiche les variables d’environnement définies."""
    
    def run(self):
        args = "".join(self.arguments).split("=")
        if len(args) == 1:
            if args[0] == "":
                for envstr in environ:
                    print(">", envstr, "=", getenv(envstr))
            
            else:
                print("{} = {}".format(args[0], getenv(args[0], "")))
        
        elif len(args) == 2:
            environ[args[0]] = args[1]
            print("{} set to '{}'".format(args[0], args[1]))
        else:
            print("La commande set n'accèpte pas plus de 2 paramètres.")
        
        if not VarGlobales.sourcing:
            print()


class pwdCommande(stripDoc):
    """Affiche le répertoire courant
  [AIDE_DETAILLEE]
  PWD
  
  Affiche le répertoire courant"""
    
    def run(self):
        print(getcwd())
        if not VarGlobales.sourcing:
            print()


class mdCommande(stripDoc):
    r"""Creation d'un répertoire
  [AIDE_DETAILLEE]
  MKDIR
  MD     crée tout répertoire intermédiaire dans le chemin, si nécessaire.
  
  Par exemple, supposez que \a n’existe pas. Alors:
  
      mkdir \a\b\c\d
  
  est équivalent à :
  
      mkdir \a
      chdir \a
      mkdir b
      chdir b
      mkdir c
      chdir c
      mkdir d
  """
    
    def run(self):
        rep = " ".join(self.arguments)
        print(f"Création du répertoire {rep!r}")
        if not VarGlobales.sourcing:
            print()


class rdCommande(stripDoc):
    """Suppression d'un répertoire
  [AIDE_DETAILLEE]
  RMDIR [/S] [/Q] [lecteur:]chemin
  RD [/S] [/Q] [lecteur:]chemin
  
      /S      Supprime tous les répertoires et les fichiers dans le
              répertoire spécifié en plus du répertoire lui-même.
              Utilisé pour supprimer une arborescence.
  
      /Q      Mode silencieux, ne demande pas de confirmation pour supprimer
              une arborescence de répertoires avec /S."""
    
    def run(self):
        rep = " ".join(self.arguments)
        print(f"Suppression du répertoire {rep!r}")
        if not VarGlobales.sourcing:
            print()


class popdCommande(stripDoc):
    """Restaure la valeur précédente du répertoire actif enregistrée
  [AIDE_DETAILLEE]
  POPD
  
  Passe au répertoire stocké par la commande PUSHD."""
    
    def run(self):
        if len(OperatingSystem.HISTPATH) > 0:
            rep = OperatingSystem.HISTPATH.pop()
            histo_source = VarGlobales.sourcing
            VarGlobales.sourcing = True
            cd = cdCommande()
            cd.arguments = [rep]
            cd.run()
            VarGlobales.sourcing = histo_source
        
        if not VarGlobales.sourcing:
            print()


class pushdCommande(stripDoc):
    """Enregistre le répertoire actif
  [AIDE_DETAILLEE]
  PUSHD [chemin | ..]
  
    chemin     Répertoire permettant de définir le répertoire en cours.
  
  Stocke le répertoire en cours pour utilisation par la commande POPD, ensuite
  passe au répertoire spécifié."""
    
    def run(self):
        rep = getcwd()
        # print(f"Sauvegarde PATH {rep!r}")
        OperatingSystem.HISTPATH.append(rep)
        
        if not VarGlobales.sourcing:
            print()


class cdCommande(stripDoc):
    """Changement du répertoire courant
  [AIDE_DETAILLEE]
  CD [/D] [lecteur:][chemin]
  CD [..]
  
    ..   Signifie que vous voulez vous placer sur le répertoire parent.
  
  Entrez CD lecteur: pour afficher le répertoire en cours sur le lecteur.
  Entrez CD sans paramètres pour afficher le lecteur et le répertoire en cours.
  """
    
    def run(self):
        # print("cd > ", self.arguments)
        dest = " ".join(self.arguments).strip()
        if isdir(dest):
            chdir(dest)
        elif dest == "-":
            chdir(VarGlobales.lastest_directory)
        elif dest == "":
            chdir(CONSTANTE.HOME_DIR)
        else:
            print(f"Le répertoire {dest!r} n'existe pas.")
        
        VarGlobales.lastest_directory = VarGlobales.current_directory
        if not VarGlobales.sourcing:
            print()


class dateCommande(stripDoc):
    """Affiche la date du jour
  [AIDE_DETAILLEE]
  DATE
  
  Affiche la date du jour."""
    
    def run(self):
        print("La date du jour est : {}".format(datetime.date.today().strftime("%d/%m/%Y")))
        if not VarGlobales.sourcing:
            print()


class timeCommande(stripDoc):
    """Affiche l'heure actuelle
  [AIDE_DETAILLEE]
  TIME
  
  Affiche l'heure actuelle """
    
    def run(self):
        print("L'heure actuelle est : {}".format(datetime.datetime.now().strftime("%X")))
        if not VarGlobales.sourcing:
            print()


class dirCommande(stripDoc):
    """Liste les répertoires et fichiers
  [AIDE_DETAILLEE]
  DIR [lecteur:][répertoire]
  
  Spécifie le lecteur, le répertoire et/ou les fichiers à répertorier."""
    
    def run(self):
        # system("{} {}".format("dir", " ".join(self.arguments)))
        param = self.arguments
        while param and param[0][0] in ("-", "/"):
            param.pop(0)
        
        # print("param:", param)
        Disk().dir(param[0] if len(param) > 0 else ".")
        if not VarGlobales.sourcing:
            print()


class helpCommande(stripDoc):
    """Aide sur les commandes disponibles
  [AIDE_DETAILLEE]
  HELP [commande]
  
  Si la commande HELP est utilisée sans paramètre,
  elle affiche la liste de toutes les commandes connues
  suivie d'une description simple
  
  Si la commande HELP est utilisée suivi par une commande,
  elle affiche une description détaillée de cette commande"""
    
    def run(self):
        if len(self.arguments) == 0:
            print("Pour plus d’informations sur une commande spécifique, entrez HELP suivi de la commande.")
            taille = 0
            for cmdstr in OperatingSystem.COMMANDES:
                doc = OperatingSystem.COMMANDES[cmdstr].__doc__
                longueur = len(cmdstr)
                if doc and longueur > taille:
                    taille = longueur
            
            taille += 1
            for cmdstr in OperatingSystem.COMMANDES:
                doc = OperatingSystem.COMMANDES[cmdstr]()
                if doc.doc_synthese:
                    print(("{:" + str(taille) + "}").format(cmdstr.upper()),
                          doc.doc_synthese.replace("\n", ("{:" + str(taille) + "}").format("\n")))
        
        elif len(self.arguments) == 1:
            cmdstr = self.arguments[0]
            if cmdstr in OperatingSystem.COMMANDES:
                doc = OperatingSystem.COMMANDES[cmdstr]()
                print(doc.doc_detaillee)
            
            else:
                print(f"La commande {cmdstr!r} est inconnue.")
        
        else:
            print("La commande HELP doit être utilisée seule ou avec 1 seul paramètre.")
        
        if not VarGlobales.sourcing:
            print()


class renCommande(stripDoc):
    """Renomme un ou plusieurs fichier
  [AIDE_DETAILLEE]
  REN [lecteur:][chemin]nom_de_fichier1 nom_de_fichier2.
  
  Vous ne pouvez pas spécifier un nouveau lecteur pour votre destination."""
    
    def run(self):
        if len(self.arguments) == 2:
            print(f"rename {self.arguments[0]!r} en {self.arguments[1]!r}")
        else:
            print(f"La commande {self.commande!r} prend exactement 2 paramètres")
        if not VarGlobales.sourcing:
            print()


class copyCommande(stripDoc):
    """Copie d'un fichier vers un répertoire
  [AIDE_DETAILLEE]
  COPY source cible
  
  Copie d'un fichier vers un répertoire """
    
    def run(self):
        if self.arguments:
            if len(self.arguments) == 1:
                print(f"copy '{self.arguments[0]}' dans '{getcwd()}'")
            else:
                for fichier in self.arguments[:-1]:
                    print("copy", fichier, "dans", self.arguments[-1])
        else:
            print("La commande 'copy' doit avoir au moins 1 paramètre")
        
        if not VarGlobales.sourcing:
            print()


class delCommande(stripDoc):
    """Suppression d'un fichier ou d'un répertoire
  [AIDE_DETAILLEE]
  DEL names
  ERASE  names
  
    names         Spécifie une liste d'un ou plusieurs fichiers ou répertoires.
                  Les caractères génériques peuvent être utilisés pour supprimer plusieurs fichiers. Si un
                  répertoire est spécifié, tous les fichiers du répertoire
                  seront supprimés."""
    
    def run(self):
        if self.arguments:
            for fichier in self.arguments:
                print("del", fichier)
        
        else:
            print("La commande 'del' doit avoir au moins 1 paramètre")
        
        if not VarGlobales.sourcing:
            print()


class echoCommande(stripDoc):
    """Affiche le texte à droite de la commande sur l'écran
  [AIDE_DETAILLEE]
  Affiche des messages ou active/désactive l’affichage des commandes.
  
    ECHO -n [message] Affiche le message à l'écran sans retour à la ligne
    ECHO [message]    Affiche le message à l'écran suivi d'un retour à la ligne
  
  Entrez ECHO sans paramètre pour afficher l’état en cours de la commande."""
    
    AlphaUpper = [chr(65 + i) for i in range(26)]
    AlphaLower = [chr(97 + i) for i in range(26)]
    AlphaNum = [chr(48 + i) for i in range(10)]
    
    ALPHABET_ENVIRON = AlphaUpper + AlphaLower + AlphaNum + ["_"]
    
    @classmethod
    def get_env(cls, variable):
        chaine = getenv(variable)
        if chaine is None:
            chaine = ""
        
        return chaine
    
    @classmethod
    def decode_var(cls, chaine):
        lchaine: int = len(chaine)
        pos1 = chaine.find("$")
        pos2 = 0
        res = ""
        
        while pos1 > -1 and pos2 < lchaine:
            res += chaine[pos2:pos1]
            pos2 = pos1 + 1
            while pos2 < lchaine and chaine[pos2] in echoCommande.ALPHABET_ENVIRON:
                pos2 += 1
            
            if chaine[pos1 + 1] == "{" and chaine[pos2 - 1] == "}":
                # print(f"var={chaine[pos1+2:pos2-1]}")
                res += echoCommande.get_env(chaine[pos1 + 2:pos2 - 1])
            else:
                # print(f"var={chaine[pos1+1:pos2]}")
                res += echoCommande.get_env(chaine[pos1 + 1:pos2])
            
            pos1 = chaine.find("$", pos1 + 1)
        
        res += chaine[pos2:]
        return res
    
    def run(self):
        retour_ligne = True
        chaine = ""
        
        for arg in self.arguments:
            if arg == "-n":
                retour_ligne = False
                continue
            
            chaine += "{} ".format(arg)
        
        print(echoCommande.decode_var(chaine), end=" ")
        
        if retour_ligne:
            print()
        if not VarGlobales.sourcing:
            print()


class aliasCommande(stripDoc):
    """Gestion des alias pour les commandes
  [AIDE_DETAILLEE]
  ALIAS [alias=commande arguments]
  
  La commande ALIAS utilisée sans paramètre permet de liste tous les alias existants.
  
  Lorsque la commande ALIAS est suivi d'un alias,
  alors la commande associée à l'alias est affichée à l'écran
  
  Lorsque la commande ALIAS est suivi d'un alias puis d'une commande et des paramètres
  alors l'alias est créé"""
    
    def run(self):
        # print(f"alias {self.arguments}")
        if self.arguments:
            if len(self.arguments) > 1 or len(self.arguments[0].split("=")) > 1:
                cmd, *args = self.arguments[0].split("=")
                args.extend(self.arguments[1:])
                if args[0] == "":
                    del OperatingSystem.ALIAS[cmd]
                
                else:
                    OperatingSystem.ALIAS[cmd] = args
            
            else:
                alias = self.arguments[0].split("=")[0]
                if alias in OperatingSystem.ALIAS:
                    print("alias {} = '{}'".format(alias, ' '.join(OperatingSystem.ALIAS[alias])))
                else:
                    print(f"alias '{alias}' inexistant.")
        
        else:
            for alias, commande in OperatingSystem.ALIAS.items():
                print(f"alias {alias} = '{' '.join(commande)}'")
        
        if not VarGlobales.sourcing:
            print()


class unaliasCommande(stripDoc):
    """Supprime un alias
  [AIDE_DETAILLEE]
  UNALIAS alias
  
  Supprime un alias de la liste des alias
  La paramètre alias est obligatoire"""
    
    def run(self):
        if self.arguments:
            alias = self.arguments[0]
            if alias in OperatingSystem.ALIAS:
                del OperatingSystem.ALIAS[alias]
            else:
                print(f"alias '{alias}' inexistant.")
        
        else:
            print(f"La commande '{self.commande}' doit être utilisée avec 1 seul paramètre")
        
        if not VarGlobales.sourcing:
            print()


class OperatingSystem(Commande):
    COMMANDES = {
        '': noCommande,
        '.': sourceCommande,
        'alias': aliasCommande,
        'cat': catCommande,
        'cd': cdCommande,
        'cls': clsCommande,
        'copy': copyCommande,
        'date': dateCommande,
        'del': delCommande,
        'dir': dirCommande,
        'echo': echoCommande,
        'exit': exitCommande,
        'help': helpCommande,
        'history': historyCommande,
        'ls': dirCommande,
        'md': mdCommande,
        'mkdir': mdCommande,
        'popd': popdCommande,
        'pushd': pushdCommande,
        'pwd': pwdCommande,
        'quit': exitCommande,
        'rd': rdCommande,
        'ren': renCommande,
        'rename': renCommande,
        'rmdir': rdCommande,
        'set': setCommande,
        'source': sourceCommande,
        'time': timeCommande,
        'unalias': unaliasCommande,
    }
    
    ALIAS = {}
    HISTORIQUE = []
    HISTPATH = []
    History = False
    Running = True
    
    @classmethod
    def prompt(cls) -> str:
        sprompt = getenv("PROMPT", "$P$G")
        res = sprompt.split("$")[0]
        
        for lettre in sprompt.split("$")[1:]:
            if lettre == "A":
                res += "&"
            elif lettre == "B":
                res += "|"
            elif lettre == "C":
                res += "("
            elif lettre == "D":
                res += datetime.date.today().strftime("%d/%m/%Y")
            elif lettre == "E":
                pass
            elif lettre == "F":
                res += ")"
            elif lettre == "G":
                res += ">"
            elif lettre == "H":
                res = res[:-1]
            elif lettre == "L":
                res += "<"
            elif lettre == "N":
                res += getcwd()[0]
            elif lettre == "P":
                res += getcwd().replace(CONSTANTE.HOME_DIR, "~")
            elif lettre == "Q":
                res += "="
            elif lettre == "S":
                res += " "
            elif lettre == "T":
                res += datetime.datetime.now().strftime("%X")
            elif lettre == "V":
                res += "10"
            elif lettre == "_":
                res += "\n"
            elif lettre == "":
                res += "$"
            else:
                res += lettre
        
        return res
    
    def is_commande(self) -> bool:
        return self.commande in OperatingSystem.COMMANDES
    
    def is_alias(self) -> bool:
        est_alias = self.commande in OperatingSystem.ALIAS
        if est_alias:
            # print("c'est un alias")
            while self.commande in OperatingSystem.ALIAS:
                self.arguments = (" ".join(OperatingSystem.ALIAS[self.commande][1:]) + " " + " ".join(
                    self.arguments)).strip().split(" ")
                if len(self.arguments) == 1 and self.arguments[0].strip() == "":
                    self.arguments.pop()
                
                self.commande = OperatingSystem.ALIAS[self.commande][0]
                # print(f"set alias({self.commande}, {self.arguments}):")
        
        return est_alias
    
    def is_runnable(self):
        return self.is_alias() or self.is_commande()
    
    def run(self) -> None:
        # print(f"SystemCommand.run({self.commande}, {self.arguments}):")
        if self.is_runnable():
            OperatingSystem.COMMANDES[self.commande].run(self)
        else:
            print(f"{self.commande!r} n'est pas une commande valide.\n")


def execute_commande(ligne_commande):
    try:
        commande, *args = ligne_commande.lower().split()
    
    except Exception:
        commande = ""
        args = ""
        
    cde = OperatingSystem(commande, args)
    cde.run()
    
    if commande != "" and OperatingSystem.History:
        historyCommande.add(cde)


def main():
    try:
        VarGlobales.current_directory = getcwd()
        
        ligne_commande = input(OperatingSystem.prompt())
        execute_commande(ligne_commande)
    
    except Exception:
        print("Main error:", traceback.print_exc())
        quit()


if __name__ == "__main__":
    try:
        clsCommande().run()
        OperatingSystem.History = False
        execute_commande("source aliases")
        historyCommande().load()
        OperatingSystem.History = True
        while OperatingSystem.Running:
            main()
        
        historyCommande().save()
    
    except Exception:
        print("Error:", traceback.format_exc())

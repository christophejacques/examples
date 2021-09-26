from msvcrt import getch
import json, os, utils.colors as colors


def getNom(c1):
    return c1.nom

class Personne:
    __nombre = 0
    
    def __init__(self, nom="", prenom="", age=0):
        self.id = Personne.__nombre 
        self.nom = nom.title()
        self.prenom = prenom.title()
        self.age = age
        self.role = self.__class__.__name__
        self.manager = None
        
        Personne.__nombre += 1
        
    def __str__(self):
        if self.manager:
            manager_id = self.manager.id
        else:
            manager_id = "None"
            
        return f'{self.id:2}, {manager_id:2}, "{self.role}", "{self.nom}", "{self.prenom}", {self.age}'
    
    def whoami(self,level = 0, prefix = ""):
        print(level * "  ", end="")
        print(f"{prefix}{self}")
        
    def to_dict(self):
        res = {}
        res["id"] = self.id
        res["nom"] = self.nom
        res["prenom"] = self.prenom
        res["age"] = self.age
        res["role"] = self.role
        if self.manager:
            res["manager_id"] = self.manager.id
        return res

    def from_dict(self, dico):
        self.id = dico["id"]
        self.nom = dico["nom"]
        self.prenom = dico["prenom"]
        self.age = dico["age"]

    @classmethod
    def Count(self):
        return self.__nombre


class Manager(Personne):
    
    def __init__(self, nom="", prenom="", age=0):
        if type(nom) == type({}):
            Personne.__init__(self)
        else:
            Personne.__init__(self, nom, prenom, age)
        self.collaborateurs = []
        
        if type(nom) == type({}):
            self.from_dict(nom)

    def gere(self, collaborateur):
        collaborateur.manager = self
        self.collaborateurs.append(collaborateur)
        
    def to_dict(self):
        res = super().to_dict()
        if self.collaborateurs:
            liste = []
            for c in sorted(self.collaborateurs, key=getNom):
                liste.append( c.to_dict() )
            res["collaborateurs"] = liste
        return res
    
    def from_dict(self, dico):
        if dico["role"].lower() == "manager":
            Personne.from_dict(self, dico)
            for c in dico.get("collaborateurs", []):
                if c["role"].lower() == "manager":
                    collab = Manager("", "", 0)
                else:
                    collab = Personne("", "", 0)
                    
                collab.from_dict(c)
                collab.manager = self
                self.collaborateurs.append(collab)
    
    def whoami(self, level = 0, prefix = ""):
        colors.setColor(colors.fcolors.GVERT)
        Personne.whoami(self, level, prefix)
        print(level * "  ", end=len(prefix) * " ")
        colors.setColor(colors.fcolors.ENDC)
        nombre = "s" if len(self.collaborateurs) > 1 else ""
        print(f"Gère : {len(self.collaborateurs)} personne{nombre}.")
        for c in sorted(self.collaborateurs, key=getNom):
            c.whoami(level + 2, "- ")
            if isinstance(c, self.__class__):
                print()


def initialisation():
    m0 = Manager("valérie", "isabelle", 47)
    m0.gere(Personne("petinon", "sophie", 48))

    m3 = Manager("Basque", "Mikael", 44)
    m0.gere(m3)

    m2 = Manager("gosselin", "eric", 50)
    m0.gere(m2)

    m1 = Manager("Audevard", "Didier", 47)
    m1.gere(Personne("Jacques", "Christophe", 48))
    m1.gere(Personne("Bisson", "Aurélien", 30))
    m1.gere(Personne("Cao", "nicolas", 40))
    m1.gere(Personne("Reix", "pascal", 45))
    m1.gere(Personne("Aubry", "gilles", 50))
    m1.gere(Personne("Bernada", "corinne", 50))
    m3.gere(m1)

    m1 = Manager("Rodriguez", "magali", 44)
    m1.gere(Personne("Garcia", "malaury", 30))
    m1.gere(Personne("robin", "nicolas", 30))
    m3.gere(m1)

    m3.gere(Personne("rougerie", "aurélie", 30))
    m3.gere(Personne("vernaelde", "bruno", 30))
    m3.gere(Personne("", "damien", 30))
    m3.gere(Personne("bouyat", "corinne", 30))

    m3.gere(Personne("mounier", "Sylvie", 30))

    m3.gere(Personne("guillon", "philippe", 30))
    m3.gere(Personne("", "samuel", 30))
    m3.gere(Personne("", "eric", 30))
    m3.gere(Personne("cenatiempo", "aline", 30))

    m2.gere(Personne("billat", "christelle", 30))
    m2.gere(Personne("lau", "carole", 30))
    m2.gere(Personne("granger", "katia", 30))
    m2.gere(Personne("machadier", "brice", 30))

    repertoire = "\\".join(__file__.split("\\")[:-1])
    with open(f"{repertoire}\Ressources.json", "w", encoding="utf-8") as fRessources:
        json.dump(m0.to_dict(), fRessources, ensure_ascii=False, indent=2)


try:
    print(f"il y a un total de {Personne.Count()} personnes.")

    repertoire = "\\".join(__file__.split("\\")[:-1])
    with open(f"{repertoire}\Ressources.json", "r", encoding="utf-8") as fRessources:
        root = json.load(fRessources)
        
    print()
    n0 = Manager(root)
    n0.whoami()
        
    print(f"\nil y a un total de {Personne.Count()} personnes.")

except Exception as e:
    print(f"Error : {e}")

#getch()

from dataclasses import dataclass, field
from enum import Enum, auto


class ConditionClause:

    def __init__(self, select_from: object, condition: str, operateur: str = ""):
        self._select_from = select_from
        self._conds: list[dict] = []
        self._conds.append({"conjonction": "Where ", "condition": condition, "operateur": operateur})
        self.level = 0

    def OpenGroup(self, conjonction: str = "", condition: str = ""):
        self.clause("(", conjonction, "")
        self.level += 1
        return self

    def CloseGroup(self):
        if self.level == 0:
            raise Exception("Aucun groupe Ouvrant disponible pour le Groupe Fermant")
        self.clause("", "", ")")
        self.level -= 1
        return self

    def clause(self, conjection: str, condition: str, operateur: str = ""):
        if not self._conds:
            raise Exception("Aucune condition principale n'a été définie")
        self._conds.append({"conjonction": conjection, "condition": condition, "operateur": operateur})
        return self

    def And(self, condition: str = "", operateur: str = ""):
        self.clause(" and ", condition, operateur)
        return self

    def Or(self, condition: str, operateur: str = ""):
        self.clause(" or ", condition, operateur)
        return self

    def __str__(self):
        # print("conds:", self._conds)
        res = f"{self._select_from}"
        if self._conds:
            res += "\n"
            level = 0
            for condition in self._conds:
                espaces = level * "  "
                res += f" {espaces}{condition['conjonction']} "
                if condition['operateur'] and condition['operateur'][0] == "(":
                    res += condition['operateur']
                    level += 1
                res += f"{condition['condition']} "
                if condition['operateur'] and condition['operateur'][0] == ")":
                    res += condition['operateur']
                    level -= 1

        return res


class FromClause:

    def __init__(self, select_liste: object, table_name: str, reference: str):
        self._select = select_liste
        self._from = table_name
        self._ref = reference
        self._inners: list[dict] = []

    def inner_join(self, table_name: str, reference: str):
        if not self._from:
            raise Exception("Aucune table ne peut être jointe")
        self._inners.append({"table": table_name, "reference": reference})
        return self

    def Where(self, condition: str, operateur: str = ""):
        return ConditionClause(self, condition, operateur)

    def __str__(self):
        res = f"{self._select}"
        res += f"\nFrom {self._from} {self._ref}"
        for inner in self._inners:
            res += f"\nInner join {inner['table']} {inner['reference']}"
        return res


class Select:
    def __init__(self, *liste):
        self._champs = liste

    def From(self, table_name: str, reference: str):
        return FromClause(self, table_name, reference)

    def __str__(self):
        res = "Select "
        for champ in self._champs[:-1]:
            res += f"{champ}, "
        if self._champs:
            return res + self._champs[-1]
        else:
            raise Exception("Aucun champ n'est retenu dans la clause Select")


class Databases:

    def __init__(self):
        pass

    def Select(self, *liste):
        return Select(*liste)

    def __str__(self):
        return "A faire"


def exemple():
    db = Databases()
    sl = db.Select("c1", "c2")
    tb = sl.From("table1", "t1").inner_join("table2", "t2")
    fr = tb.Where("champ1=5").And("\n").OpenGroup("champ2=10").Or("champ3=15").CloseGroup()

    print(fr)


class TableException(Exception):
    pass


class ColumnException(Exception):
    pass


class Type(Enum):
    NONE = auto()
    ENTIER = auto()
    DECIMAL = auto()
    CHAINE = auto()
    BOOLEEN = auto()


@dataclass
class Champ:
    nom: str
    type_nom: Enum = Type.NONE
    val_defaut: object = None


@dataclass
class Table:
    nom: str
    champs: list[Champ] = field(default_factory=list)
    relations: list[tuple] = field(default_factory=list)

    def ajouter_relation(self, champ_source: tuple["Table", Champ], champ_dest: tuple["Table", Champ]) -> None:
        if not isinstance(champ_source, tuple) or not isinstance(champ_dest, tuple):
            raise TypeError("Un des parametres n'est pas de type tuple[Table, Champ].")

        if not isinstance(champ_source[0], Table) or not isinstance(champ_source[1], Champ) or (
           not isinstance(champ_dest[0], Table)) or not isinstance(champ_dest[1], Champ):
            raise TypeError("Un des parametres n'est pas de type [Table, Champ].")

        self.relations.append((champ_source, champ_dest))
        champ_dest[0].relations.append((champ_dest, champ_source))

    def ajouter_champ(self, champ: Champ) -> None:
        if not isinstance(champ, Champ):
            raise TypeError("le parametre donnee n'est pas de type Champ")

        self.champs.append(champ)

    def get_champ(self, nom_champ: str) -> tuple["Table", Champ]:
        for un_champ in self.champs:
            if un_champ.nom == nom_champ:
                return self, un_champ

        raise ColumnException(f"Le champ {nom_champ} n'existe pas dans la table {self.nom}.")

    def get_type_champ(self, nom_champ: str) -> Enum:
        return self.get_champ(nom_champ)[1].type_nom

    def __str__(self):
        liste_champs = ""
        for champ in self.champs:
            liste_champs += f"\n  {champ.__class__.__name__}("
            for attribut in filter(lambda x: not x.endswith("__"), dir(champ)):
                liste_champs += f"{attribut}={getattr(champ, attribut)!r}, "
            liste_champs = liste_champs[:-2] + "), "
        liste_champs = liste_champs[:-2]

        if self.relations:
            liste_relations = ""
            for relation in self.relations:
                liste_relations += f"\n    {relation[0][0].nom}.{relation[0][1].nom} = {relation[1][0].nom}.{relation[1][1].nom}, "

            liste_relations = liste_relations[:-2]
            return f"{self.__class__.__name__}(nom={self.nom!r}, champs=[{liste_champs}]," + (
                   f"\n  relations=[{liste_relations}])")
        else:
            return f"{self.__class__.__name__}(nom={self.nom!r}, champs=[{liste_champs}])"              


@dataclass
class Database:
    tables: list[Table] = field(default_factory=list)

    def ajouter_table(self, table: Table) -> None:
        if not isinstance(table, Table):
            raise TypeError("le parametre donnee n'est pas de type Table")

        if len([1 for t in self.tables if t.nom == table.nom]) > 0:
            raise TableException(f"La table {table.nom} existe deja dans la base de donnees.")

        self.tables.append(table)

    def ajouter_relation(self, champ_source: tuple[Table, Champ], champ_dest: tuple[Table, Champ]) -> None:
        if not self.existe_table(champ_source[0].nom):
            raise TableException(f"La table {champ_source[0].nom} n'existe pas dans la base de donnees.")

        if not self.existe_table(champ_dest[0].nom):
            raise TableException(f"La table {champ_dest[0].nom} n'existe pas dans la base de donnees.")
        
        champ_source[0].ajouter_relation(champ_source, champ_dest)

    def existe_table(self, nom_table: str) -> bool:
        for une_table in self.tables:
            if une_table.nom == nom_table:
                return True
        return False

    def get_table(self, nom_table: str) -> Table:
        for une_table in self.tables:
            if une_table.nom == nom_table:
                return une_table

        raise TableException(f"La table {nom_table} n'existe pas dans la base de donnees.")


def main():

    db = Database()

    db.ajouter_table(Table("Personne"))
    db.ajouter_table(Table("Fonction"))
    db.ajouter_table(Table("Profession"))

    pers = db.get_table("Personne")
    pers.ajouter_champ(Champ("Ident", Type.ENTIER))
    pers.ajouter_champ(Champ("Nom", Type.CHAINE))
    pers.ajouter_champ(Champ("Prenom", Type.CHAINE))
    pers.ajouter_champ(Champ("Age", Type.ENTIER))
    pers.ajouter_champ(Champ("ProfessionId", Type.ENTIER))
    pers.ajouter_champ(Champ("FonctionId", Type.ENTIER))

    fonction = db.get_table("Fonction")
    fonction.ajouter_champ(Champ("Ident", Type.ENTIER))
    fonction.ajouter_champ(Champ("Libelle", Type.CHAINE))
    db.ajouter_relation(pers.get_champ("FonctionId"), fonction.get_champ("Ident"))

    prof = db.get_table("Profession")
    prof.ajouter_champ(Champ("Ident", Type.ENTIER))
    prof.ajouter_champ(Champ("Libelle", Type.CHAINE))
    db.ajouter_relation(pers.get_champ("ProfessionId"), prof.get_champ("Ident"))

    print(db.get_table("Personne"))


if __name__ == "__main__":
    main()

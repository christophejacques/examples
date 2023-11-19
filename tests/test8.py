from typing import Self


class TypeChamp:
    libelle: str

    def __init__(self, libelle: str, options: list[str] = [], complements: list[str] = []):
        match libelle.strip().upper():
            case "ENTIER" | "INTEGER" | "INT" | "LONG" | "DOUBLE":
                self.libelle = "INTEGER"
            case "REAL" | "REEL":
                self.libelle = "REAL"
            case "NUMERIC" | "NUMERIQUE":
                self.libelle = "NUMERIC"
            case "TEXTE" | "TEXT" | "CHAR" | "VARCHAR" | "STRING" | "STR":
                self.libelle = "TEXT"
            case "BLOB":
                self.libelle = "BLOB"
            case _:
                raise TypeError(f"La valeur '{libelle}' n'est pas un type de champ valide !")
        
        self.options: str = ""
        for option in options:
            match option.strip().upper():
                case "PRIMARY" | "PRIMARY KEY":
                    self.options += " PRIMARY KEY"
                case "UNIQUE":
                    self.options += " UNIQUE"
                case "AUTO" | "AUTOINCREMENT":
                    self.options += " AUTOINCREMENT"
                case "NULL" | "NUL":
                    self.options += " NULL"
                case "NOT NULL" | "NOT NUL":
                    self.options += " NOT NULL"
                case _:
                    raise TypeError(f"La valeur '{option}' n'est pas une option valide !")

        self.complements: str = ""
        if not complements:
            return

        for complement in complements:
            match str(complement).strip().upper().split():
                case ["CURRENT"] | ["CURRENT_TIMESTAMP"]:
                    self.complements += " DEFAULT CURRENT_TIMESTAMP"
                case ["DEFAULT", default]:
                    self.complements += f" DEFAULT {default}"
                case ["CHECK", *check]:
                    self.complements += f" CHECK({' '.join(check)})"

    def __str__(self) -> str:
        return f"{self.libelle}{self.options}{self.complements}"


class Champ:

    def __init__(self, nom: str, type_champ: TypeChamp):

        if not isinstance(nom, str):
            raise TypeError(f"Le type de la valeur '{nom}' n'est pas str")

        if not isinstance(type_champ, TypeChamp):
            raise TypeError(f"La valeur '{type_champ}' n'est pas un type de champ valide.")

        self.type_champ: str = str(type_champ)
        self.nom: str = nom
        self.table: str = ""

    def setTable(self, table_name: str) -> Self:
        self.table = table_name
        return self

    def getTable(self) -> str:
        return self.table

    def getName(self) -> str:
        return self.nom

    def getType(self) -> str:
        return self.type_champ

    def __str__(self) -> str:
        return f"{self.table}({self.nom})"


class Relation:
    libelle: str
    champs: str
    reference_champs: list[Champ]
    reference_str: str

    def __init__(self, type_relation: str, liste_champs: list[Champ], reference: list[Champ | str] = []):
        match type_relation.strip().upper():
            case "PRIMARY" | "PRIMARY KEY":
                self.libelle = "PRIMARY KEY "
            case "FOREIGN" | "FOREIGN KEY":
                self.libelle = "FOREIGN KEY "
            case "CONSTRAINT":
                self.libelle = "CONSTRAINT "
            case "UNIQUE":
                self.libelle = "UNIQUE "
            case _:
                raise TypeError(f"La valeur '{type_relation}' n'est pas un type de relation valide.")

        if len(liste_champs) == 0:
            raise TypeError("Une relation doit contenir au moins un Champ")

        liste = []
        for champ in liste_champs:
            if not isinstance(champ, Champ):
                raise TypeError(f"La valeur '{champ}' n'est pas de type Champ")
            liste.append(champ.nom)

        self.champs = f"({', '.join(liste)})"
        self.reference_champs = []
        self.reference_str = ""

        if not reference:
            return

        self.reference = " REFERENCES"
        for ref in reference:
            if isinstance(ref, Champ):
                self.reference_str += f" {ref.table}({ref.nom})"
                self.reference_champs.append(ref)
            else:
                self.reference_str += f" {ref}"

    def __str__(self) -> str:
        return f"{self.libelle}{self.champs}{self.reference_str}"


class Table:
    schema: str
    nom: str
    champs: list[Champ]
    relations: list[Relation]

    def __init__(self, nom: str, champs: list[Champ], relations: list[Relation] = []):
        if "." in nom:
            self.schema, self.nom = nom.split(".")
        else:
            self.schema = ""
            self.nom = nom

        for champ in champs:
            if not isinstance(champ, Champ):
                raise TypeError(f"La valeur '{champ}' n'est pas de type Champ.")
            champ.setTable(nom)
        self.champs = champs
        self.add_relations(relations)

    def add_relations(self, relations: list[Relation]) -> None:
        for relation in relations:
            if not isinstance(relation, Relation):
                raise TypeError(f"La valeur '{relation}' n'est pas de type Relation.")
        self.relations = relations

    def drop(self) -> str:
        return f"DROP TABLE IF EXISTS {self.nom}"

    def getSchemaNom(self) -> str:
        return self.schema + ("." if self.schema else "") + self.nom

    def getSchema(self) -> str:
        return self.schema

    def getName(self) -> str:
        return self.nom

    def getChamp(self, nom_champ: str) -> Champ:
        for champ in self.champs:
            if champ.getName().upper() == nom_champ.upper():
                return champ
        raise ValueError(f"Le champ '{nom_champ}' n'appartient pas a la table {self.nom}")

    def __str__(self) -> str:
        lib: str = f"Table {self.schema + '.' if self.schema else ''}{self.nom} (\n"
        for champ in self.champs:
            lib += f"    {champ.getName()} {champ.getType()},\n"
        if self.relations:
            for relation in self.relations:
                lib += f"  {relation},\n"
        return lib[:-2] + ")"


class BaseDeDonnees:
    def __init__(self):
        self.tables: dict[str, list[Table]] = {}
        self.current_schema = "default"

    def __enter__(self) -> Self:
        print("Ouverture de la BD")
        return self

    def __exit__(self, *args) -> None:
        print("Fermeture de la BD", args)

    def set_schema(self, schema: str) -> None:
        self.current_schema = schema
        print("Current schema set to :", schema)

    def getSchemas(self) -> str:
        return ", ".join(schema for schema in self.tables)

    def getTables(self, schema: str = "") -> str:
        if schema:
            if schema not in self.tables:
                return ""

            return ", ".join(table.getName() for table in self.tables[schema] if table.getSchema() == schema)

        return ", ".join(table.getName() for table in self.tables[self.current_schema])

    def getTableByName(self, nom_schema_table: str) -> Table:
        if "." in nom_schema_table:
            schema, nom_table = nom_schema_table.split(".")
        else:
            schema, nom_table = self.current_schema, nom_schema_table

        for table in self.tables[schema]:
            if table.getName().upper() == nom_table.upper() and table.getSchema().upper() == schema.upper():
                return table
        raise Exception(f"La table {nom_table} n'existe pas dans la base de donnees.")

    def hasTableByName(self, nom_schema_table: str) -> bool:
        if "." in nom_schema_table:
            schema, nom_table = nom_schema_table.split(".")
        else:
            schema, nom_table = self.current_schema, nom_schema_table

        for table in self.tables[schema]:
            if table.getName().upper() == nom_table.upper() and table.getSchema().upper() == schema.upper():
                return True
        return False

    def add_table(self, table: Table) -> None:
        if not isinstance(table, Table):
            raise TypeError(f"le parametre {table} n'est pas de type Table")
        if table.getSchema() == "":
            table.schema = self.current_schema

        if self.tables.get(table.getSchema()) is None:
            self.tables[table.getSchema()] = []
        self.tables[table.getSchema()].append(table)

    def drop_table(self, table: Table) -> None:
        if not isinstance(table, Table):
            raise TypeError(f"le parametre {table} n'est pas de type Table")

        for other_table in filter(lambda vtable: vtable != table, self.tables[table.getSchema()]):
            for relation in other_table.relations:
                for champ in relation.reference_champs:
                    if champ.getTable() == table.getSchemaNom():
                        msg = f"La table {table.getSchemaNom()} ne peut etre supprimee "
                        msg += f"car elle est referencee par la table {other_table.getSchemaNom()}"
                        msg += f"({champ.getName()})"
                        raise Exception(msg)

        self.tables[table.getSchema()].remove(table)

    def dropTableByName(self, nom_table: str, error_if_not_exists: bool = True) -> None:
        if error_if_not_exists:
            self.drop_table(self.getTableByName(nom_table))

        elif self.hasTableByName(nom_table):
            self.drop_table(self.getTableByName(nom_table))

    def getChampByFullName(self, full_name: str) -> Champ:
        if len(full_name.strip().split(".")) == 2:
            schema = self.current_schema
            table_name, champ_name = full_name.strip().split(".")
        elif len(full_name.strip().split(".")) == 3:
            schema, table_name, champ_name = full_name.strip().split(".")
        else:
            raise ValueError("Le champ doit etre de la forme '<schema>.table.champ'")

        return self.getTableByName(f"{schema}.{table_name}").getChamp(champ_name)


with BaseDeDonnees() as bd:

    bd.set_schema("ref")

    bd.add_table(Table("grade", 
        [Champ("gradeID", TypeChamp("entier", ["primary", "auto"])), 
        Champ("code", TypeChamp("texte", ["not null", "unique"])), 
        Champ("libelle", TypeChamp("texte", ["not null"]))]))
    print(bd.getTableByName("grade"))

    bd.add_table(Table("travail", 
        [Champ("travailID", TypeChamp("entier", ["primary", "auto"])), 
        Champ("code", TypeChamp("texte", ["not null", "unique"])), 
        Champ("libelle", TypeChamp("texte", ["not null"]))]))
    print(bd.getTableByName("travail"))

    bd.add_table(Table("fonctions", 
        [Champ("fonctionid", TypeChamp("entier", ["primary", "auto"])), 
        Champ("code",  TypeChamp("string", ["not null", "unique"])), 
        Champ("libelle",  TypeChamp("string", ["not null"])), 
        Champ("date", TypeChamp("texte", ["not null"], ["current"]))]))
    print(bd.getTableByName("fonctions"))

    bd.add_table(Table("asp.users", [
        Champ("userid", TypeChamp("entier", ["primary", "auto"])), 
        Champ("nom", TypeChamp("texte", ["not null"])), 
        Champ("prenom", TypeChamp("texte", ["not null"])), 
        Champ("email", TypeChamp("texte", ["not null", "unique"], ["check email like '%@%.%'"])), 
        Champ("actif", TypeChamp("texte", ["not null"], ["DEFAULT 'True'"])), 
        Champ("age", TypeChamp("int", complements=["default 20", "check age < 140"])), 
        Champ("travailID", TypeChamp("int")), 
        Champ("fonctionID", TypeChamp("int")), 
        Champ("date", TypeChamp("texte", ["not null"], ["current"]))]))

    bd.set_schema("asp")
    bd.getTableByName("users").add_relations([
        Relation("primary", [bd.getTableByName("users").getChamp("userid")]), 
        Relation("foreign", [bd.getTableByName("users").getChamp("travailid")], 
        [bd.getTableByName("ref.travail").getChamp("travailID"), 
        "ON DELETE CASCADE", "ON UPDATE NO ACTION"]), 
        Relation("foreign", [bd.getTableByName("users").getChamp("fonctionid")], 
        [bd.getTableByName("ref.fonctions").getChamp("fonctionID"), 
        "ON DELETE CASCADE", "ON UPDATE NO ACTION"]), 
        Relation("unique", [bd.getTableByName("users").getChamp("email")])])

    print(bd.getTableByName("users"))
    print()

    for schema in bd.tables:
        print(f"Tables {schema}:", bd.getTables(schema))

    print(">", bd.getChampByFullName("users.nom"))

    bd.dropTableByName("users")

    bd.set_schema("ref")
    bd.dropTableByName("fonctions")
    bd.dropTableByName("travail")
    bd.dropTableByName("grade")

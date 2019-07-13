import sqlite3, sys


def fonction(*args):
    print(f"fonction(*args): avec {len(args)} arguments")

    for i, arg in enumerate(args):
        print(f"- {i} : {arg}")


class monsql:

    def __init__(self, database):
        self.database = database
        print(f"Base de données ({database}) : Connexion ", end="")
        try:
            self.conn = sqlite3.connect(database)
            print("Ok, curseur ", end="")
            self.curs = self.conn.cursor()
            print("Ok")

        except sqlite3.Error as e:
            self.conn = None
            print(f"Ko ({e})")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn:
            print(f"Fermeture de la bd ({self.database}) : ", end="")
            if self.curs:
                print("curseur ", end="")
                self.curs.close()

            print("Ok, ", end="")
            self.conn.close()
            print("connexion Ok")

    def commit(self):
        print("commit() : ", end="")
        self.conn.commit()
        print("Ok")

    def rollback(self):
        print("rollback() : ", end="")
        self.conn.rollback()
        print("Ok")

    def isconnected(self):
        return self.conn != None

    def existTable(self, nomTable):
        return self.curs.execute("SELECT name FROM sqlite_master WHERE name = ?", (nomTable,)).rowcount > 0

    def createTable(self, nomTable, listeChamps):
        print(f"Création de la table *{nomTable}*", end="")
        tableStr = f"CREATE TABLE {nomTable} (\n"

        for nomchamp, typeChamp in listeChamps[:-1]:
            tableStr += f"    {nomchamp} {typeChamp},\n"

        nomchamp, typeChamp = listeChamps[-1]
        tableStr += f"    {nomchamp} {typeChamp} )"

        # with conn:
        self.curs.execute(tableStr)

        print(" => table créée")

    def getDatas(self, sqlCode):
        print(f"getDatas({sqlCode}) : ", end="")
        self.curs.execute(sqlCode)
        res = self.curs.fetchall()
        print(f"{len(res)} enregs")
        return res

    def deleteData(self, nomTable, *conditions):
        lstCondValues = []
        where_cond = ""
        for n, v in conditions:
            lstCondValues.append(v)
            if where_cond == "":
                where_cond = f"WHERE {n}=?"
            else:
                if n.startswith("OR "):
                    where_cond += f" {n}=?"
                else:
                    where_cond += f" AND {n}=?"

        sqlstring = f"DELETE FROM {nomTable} {where_cond}"

        print(sqlstring, lstCondValues, end=" : ")
        nb = self.curs.execute(sqlstring, lstCondValues)
        print(f"{nb.rowcount} enregs => OK")

    def insertData(self, nomTable, *donnees):

        insertColsNames = f"INSERT INTO {nomTable} VALUES ("
        insertColsValues = []

        for nomChamp, valeurChamp in donnees[:-1]:
            insertColsNames += f":{nomChamp}, "
            insertColsValues.append(valeurChamp)

        nomChamp, valeurChamp = donnees[-1]
        insertColsNames += f":{nomChamp})"
        insertColsValues.append(valeurChamp)

        print(insertColsNames, insertColsValues, end="")
        self.curs.execute(insertColsNames, insertColsValues)
        print(" => OK")


# with monsql("basededonnees.db") as mabd:
with monsql(":memory:") as mabd:
    if mabd.isconnected():
        try:
            if not mabd.existTable("personnes"):
                mabd.createTable("personnes",[("nom", "text"), ("prenom","text"), ("datedenaissance","text")])

            if not mabd.existTable("metiers"):
                mabd.createTable("metiers",[("num", "int"), ("libelle","text")])

            print("Liste des tables :")
            for enreg in mabd.getDatas("SELECT name FROM sqlite_master WHERE type = 'table'"):
                print(f"{enreg}", end=" ")
            print("")

            mabd.insertData("personnes", ("nom", "JACQUES"), ("prenom", "christophe"), ("datedenaissance", "1971-09-02"))
            mabd.insertData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"), ("datedenaissance", "1951-09-16"))

            mabd.deleteData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"))
            mabd.insertData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"), ("datedenaissance", "1951-09-16"))
            mabd.commit()

            for l in mabd.getDatas("PRAGMA table_info(metiers)"):
                print(f"  - {l}")

            for enreg in mabd.getDatas("select * from personnes"):
                print(f"  - {enreg}")

        except sqlite3.OperationalError as oe:
            print(f"Ko ({oe})")
            mabd.rollback()

        except: # (RuntimeError, TypeError, NameError):
            errcls, errlib, errobj = sys.exc_info()
            print(f"{errcls}".split("'")[1] + " :")
            print(f" - ligne {errobj.tb_lineno} : {errlib}")
            mabd.rollback()


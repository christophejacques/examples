import sqlite3, sys
import os, traceback

repertoire = r"C:\Users\utilisateur\OneDrive\Programmation\python\examples"
os.chdir(repertoire)

# ---------------------------------------------------------
#
# codage UTF-8 des instruction affichée via commande print()
#
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# ---------------------------------------------------------

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

        except Exception as e:
            print(f"Err ({e})")

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
        return self.conn is not None

    def existTable(self, nomTable):
        res = self.curs.execute("SELECT name FROM sqlite_master WHERE name = ?", (nomTable,)).fetchone()
        if res is None: return False
        return  len(res) > 0

    def createTable(self, nomTable, listeChamps, cles = ""):
        print(f"Création de la table *{nomTable}*", end="")
        tableStr = f"CREATE TABLE {nomTable} (\n"

        for nomchamp, typeChamp in listeChamps[:-1]:
            tableStr += f"    {nomchamp} {typeChamp},\n"

        nomchamp, typeChamp = listeChamps[-1]
        tableStr += f"    {nomchamp} {typeChamp}"
        if cles:
            tableStr += f",\n{cles[0]}"
            for cle in cles[1:]:
                tableStr += f",\n{cle}"

        tableStr += ")"
        # print(tableStr)
        self.curs.execute(tableStr)

        print(" => table créée")

    def setForeignKeys(self, etat):
        ATTENDU = {
          "ON"  : 1,
          "OFF" : 0
        }
        print(f"set Foreign Keys : {etat} = ", end="")
        self.curs.execute(f"PRAGMA foreign_keys = {etat};")
        res = self.curs.execute("PRAGMA foreign_keys").fetchone()[0] 
        print(res, " Ok" if res == ATTENDU[etat] else " Ko")
        return res == ATTENDU[etat]

    def getDatas(self, sqlCode):
        print(f"getDatas({sqlCode}) : ", end="")
        res = ()
        try:
            self.curs.execute(sqlCode)
            res = self.curs.fetchall()
            print(f"{len(res)} enregs")
        except:
            errcls, errlib, errobj = sys.exc_info()
            print(f"{errcls}".split("'")[1] + " :")
            print(f" - ligne {errobj.tb_lineno} : {errlib}")

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
        print(f"(Id:{nb.lastrowid:03}) {nb.rowcount} enregs => OK")


    def insertData(self, nomTable, *donnees):

        insertColsNames = "("
        insertColsValues = []
        listeColsNames = "("

        for nomChamp, valeurChamp in donnees[:-1]:
            listeColsNames += f"{nomChamp}, "
            insertColsNames += f":{nomChamp}, "
            insertColsValues.append(valeurChamp)

        nomChamp, valeurChamp = donnees[-1]
        listeColsNames += f"{nomChamp})"
        insertColsNames += f":{nomChamp})"
        insertColsValues.append(valeurChamp)

        insertColsNames = f"INSERT INTO {nomTable} {listeColsNames} VALUES {insertColsNames}"

        print(insertColsNames, insertColsValues, end="")
        try:
            res = self.curs.execute(insertColsNames, insertColsValues)
            print(f" => OK (Id:{res.lastrowid:03})")
            self._last_row_id = res.lastrowid

        except Exception as e:
            print(f" => KO", e)
            self._last_row_id = None

        return self._last_row_id


    def execute(self, sqlCode):
        print(f"execute({sqlCode}) : ", end="")
        try:
            self.curs.execute(sqlCode)
            res = True
        except:
            res = False
            errcls, errlib, errobj = sys.exc_info()
            print(f"{errcls}".split("'")[1] + " :")
            print(f" - ligne {errobj.tb_lineno} : {errlib}")

        return res



# with monsql("basededonnees.db") as mabd:
with monsql(":memory:") as mabd:
    if mabd.isconnected():
        try:
            if not mabd.existTable("personnes"):
                mabd.createTable("personnes",
                    [("idPersonne",     "integer PRIMARY KEY AUTOINCREMENT"), 
                     ("nom",            "text not null"), 
                     ("prenom",         "TEXT NOT NULL"), 
                     ("datedenaissance","text"), 
                     ("horodatage",     "TEXT DEFAULT CURRENT_TIMESTAMP")])
            else:
                print("Table personnes existe déjà")

            if not mabd.existTable("metiers"):
                mabd.createTable("metiers",
                    [("idMetier",   "integer PRIMARY KEY AUTOINCREMENT"), 
                     ("libelle",    "text")])
            else:
                print("Table metiers existe déjà")

            if not mabd.existTable("ass_personne_metier"):
                mabd.createTable("ass_personne_metier",
                    [("idPersonne",     "integer NOT NULL"), 
                     ("idMetier",       "integer NOT NULL")],
                     ["PRIMARY KEY (idPersonne, idMetier)",
                      "FOREIGN KEY (idPersonne) REFERENCES personnes(idPersonne)",
                      "FOREIGN KEY (idMetier)   REFERENCES metiers(idMetier)"] )
            else:
                print("Table ass_personne_metier existe déjà")

            mabd.commit()
            mabd.setForeignKeys("ON")

            mabd.deleteData("personnes")
            mabd.commit()

            mabd.insertData("personnes", ("nom", "JACQUES"), ("prenom", "christophe"), ("datedenaissance", "1971-09-02"))
            mabd.insertData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"), ("datedenaissance", "1951-09-16"))

            mabd.deleteData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"))
            mabd.insertData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"), ("datedenaissance", "1951-09-16"))
            mabd.commit()

            mabd.insertData("metiers", ("libelle", "Informaticien"))
            mabd.insertData("metiers", ("libelle", "Fonctionnaire"))

            personne_id = mabd.getDatas("SELECT idPersonne FROM personnes WHERE nom='JACQUES'")[0][0] 
            metier_id = mabd.getDatas("SELECT idMetier FROM metiers WHERE libelle='Informaticien'")[0][0] 
            mabd.insertData("ass_personne_metier", ("idPersonne", personne_id), ("idMetier", metier_id))

            personne_id = mabd.getDatas("SELECT idPersonne FROM personnes WHERE nom='BERNARD'")[0][0] 
            metier_id = mabd.getDatas("SELECT idMetier FROM metiers WHERE libelle='Fonctionnaire'")[0][0] 
            mabd.insertData("ass_personne_metier", ("idPersonne", personne_id), ("idMetier", metier_id))
            mabd.insertData("ass_personne_metier", ("idPersonne", personne_id), ("idMetier", metier_id))
            mabd.insertData("ass_personne_metier", ("idPersonne", 100), ("idMetier", 100))
            mabd.commit()


            for l in mabd.getDatas("PRAGMA table_info(personnes)"):
                print(f"  - {l}")
            print()

            print("Liste des tables :")
            for t in mabd.getDatas("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"):
                for enreg in mabd.getDatas(f"select * from {t[0]}"):
                    print(f"  - {enreg}")
                print()

            for t in mabd.getDatas("""SELECT p.idPersonne, p.nom, pm.idMetier , m.libelle
                FROM personnes p 
                INNER JOIN ass_personne_metier pm on (p.idPersonne = pm.idPersonne)
                INNER JOIN metiers m on (pm.idMetier = m.idMetier)"""):
                print(f"  - {t}")
            print()

            # mabd.execute("DROP table personnes")
            # mabd.commit()


        except sqlite3.OperationalError as oe:
            print(f"Ko ({oe})")
            mabd.rollback()

        except: # (RuntimeError, TypeError, NameError):
            print(traceback.print_exc())
            mabd.rollback()

import msvcrt
#msvcrt.getch()

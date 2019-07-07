import sqlite3
onction(*args):
    print(f"fonction(*args): avec {len(args)} arguments")

    for i, arg in enumerate(args):
        print(f"- {i} : {arg}")


def createTable(nomTable, listeChamps):
    print(f"Création de la table *{nomTable}*", end="")
    tableStr = f"CREATE TABLE {nomTable} (\n"
    for nomchamp, typeChamp in listeChamps[:-1]:
        tableStr += f"    {nomchamp} {typeChamp},\n"

    nomchamp, typeChamp = listeChamps[-1]
    tableStr += f"    {nomchamp} {typeChamp} )"

    with conn:
        c.execute(tableStr)

    print(" => table créée")


def getDatas(sqlCode):
    print(f"def getDatas({sqlCode}):")
    c.execute(sqlCode)
    return c.fetchall()


def insertData(nomTable, *donnees):

    insertColsNames = f"INSERT INTO {nomTable} VALUES ("
    insertColsValues = []

    for nomChamp, valeurChamp in donnees[:-1]:
        insertColsNames += f":{nomChamp}, "
        insertColsValues.append(valeurChamp)

    nomChamp, valeurChamp = donnees[-1]
    insertColsNames += f":{nomChamp})"
    insertColsValues.append(valeurChamp)

    print(insertColsNames, insertColsValues, end="")

    with conn:
        c.execute(insertColsNames, insertColsValues)

    print(" => OK")


# conn = sqlite3.connect("basededonnees.db")
conn = sqlite3.connect(":memory:")
print("database ouverte en mémoire")

c = conn.cursor()

createTable("personnes",[("nom", "text"), ("prenom","text"), ("datedenaissance","text")])

insertData("personnes", ("nom", "JACQUES"), ("prenom", "christophe"), ("datedenaissance", "1971-09-02"))
insertData("personnes", ("nom", "BERNARD"), ("prenom", "brigitte"), ("datedenaissance", "1951-09-16"))

for enreg in getDatas("select * from personnes"):
    print(enreg)

conn.close()
print("database fermée")

print()


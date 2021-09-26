import sqlite3 as sql
from time import sleep
from hashlib import sha512
from random import randint
import os

TAILLE_CLE = 16

def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)

def hash(*valeurs):
    return sha512(str(valeurs).encode("utf-8")).hexdigest()

def creation_cle():
    cle = ""
    for _ in range(TAILLE_CLE):
        cle += chr(randint(33, 122))
        
    return cle


def print_users(c):
    fprint("Table User :")
    e = c.execute("select * from user")
    f = e.fetchone()
    while f is not None:
        for c in f:
            fprint(c)
        print()
        f = e.fetchone()

def isPassword(c, username, password):
    fprint(f"Checking User {username} with password \"{password}\" = ", end="")
    res = False
    e = c.execute("select cle, password from user where username = :username", {"username":username})
    f = e.fetchone()
    if f:
        cle, cryptpass = f
        res = (cryptpass == hash(cle, password))
    fprint(res)
    return res

    
def update_password(c, username, password):
    s = """UPDATE user
           SET  cle             = :cle,
                password        = :password,
                date_modified   = DATETIME('now','localtime')
           WHERE username = :username"""
    cle = creation_cle()
    e = c.execute(s, {"username":username, "cle":cle, "password":hash(cle, password)})
    
    if e.rowcount > 0:
        fprint(f"{username} password updated to : {password}")
        return True
    else:
        fprint(f"{username} password can't be updated to : {password}")
        return False

    
def add_user(c, username, password):
    cle = creation_cle()
    try:
        e = c.execute(f"""insert into user (username, cle, password) 
                                    values (:username, :cle, :password)""", 
                     {"username":username, "cle":cle, "password":hash(cle, password)} )
                     
    except Exception as err:
        print(f"Error add_user({username}):",err)
        return False
        
    if e.rowcount <= 0:
        print(f"Erreur de creation du user {username}")
        
    return e.rowcount > 0

def main():
    os.chdir("C:\\Users\\utilisateur\\OneDrive\\Programmation\\python\\examples")
    fprint("> cd", os.getcwd())
    
    with sql.connect("sample.db") as db:    
        db.create_function("hash", 2, hash)
        c = db.cursor()
        
        c.execute("drop table if exists user")
        c.execute("""CREATE TABLE user (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username        TEXT NOT NULL UNIQUE, 
                        cle             TEXT NOT NULL, 
                        password        TEXT NOT NULL,
                        date_created    TEXT DEFAULT CURRENT_TIMESTAMP,
                        date_modified   TEXT DEFAULT CURRENT_TIMESTAMP)""")
        
        db.commit()
        
        
        add_user(c, "admin", "admin")
        add_user(c, "christophe.jacques1", "")
        db.commit()
        
        #print_users(c)
        isPassword(c, "admin", "Unknown")
        isPassword(c, "admin", "admin")

        #print_users(c)
        isPassword(c, "christophe.jacques1", "Password")
        fprint()
        
        if update_password(c, "christophe.jacques1", "Password"):
            db.commit()
        
        isPassword(c, "christophe.jacques1", "Password")
        fprint()
        
        print_users(c)
        c.close()
        

if __name__ == "__main__":
    try:
        main()
        
    except Exception as e:
        fprint("Error:", e)
        
 
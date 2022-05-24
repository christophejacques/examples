#! python3
# d:\Programmes\Python\python


debug = False


def dprint(*args):
    if debug:
        print(*args)


etat = ""
try:
    with open("C:/Users/utilisateur/OneDrive/Programmation/python/examples/dpkg-debug.log") as f:
        for ligne in f:
            date, heure, action, *liste_champs = ligne.split(" ")

            if action == "install":
                derniere_action = action
                application = liste_champs[0]
                fromVersion = ""
                toVersion = liste_champs[2].strip()
                versions = "v{}".format(toVersion)
                etat = ""
                dprint(derniere_action, application, versions, etat)
            
            if action == "upgrade":
                derniere_action = action
                application = liste_champs[0]
                fromVersion = liste_champs[1]
                toVersion = liste_champs[2].strip()
                versions = "v{} -> v{}".format(fromVersion, toVersion)
                etat = ""
                dprint(derniere_action, application, versions, etat)
            
            elif action == "configure":
                if liste_champs[0] == application:
                    derniere_action = "configuration"
                    fromVersion = ""
                    toVersion = liste_champs[1].strip()
                    versions = "v{}".format(toVersion)
                    etat = ""
                    dprint(derniere_action, application, versions, etat)
            
            elif action == "status":
                if liste_champs[1] == application:
                    if etat != liste_champs[0]:
                        etat = liste_champs[0]
                        dprint(derniere_action, application, versions, etat)
                
    dprint()
    print(derniere_action)
    print(application)
    print(versions)
    print(etat)
    

except Exception as e:
    print("Error")
    print(f"{e}")

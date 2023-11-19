import sys
import os
import re
import traceback

from colors import fcolors

couleurRecherche = fcolors.GVERT
couleurRegexp = fcolors.GJAUNE
couleurMatch = fcolors.GJAUNE
couleurErreur = fcolors.GROUGE

# détermination du nombre de colonnes du terminal
_, colstr = os.popen('mode con | findstr Colonne', 'r').read().split()
colsize = int(colstr)
longeurMaxFichier = (colsize - 5) // 2

argv = sys.argv.copy()[1:]

# argv = ("10", " \(1080.*(\..*)", "\\1", )
nb_args = len(argv)


def fprint(*args, **kw):
    print(*args, end="")


def msg_erreur(msg):
    nom_programme = sys.argv[0].split('\\')[-1]
    print(f"{nom_programme}:", *argv)
    print(msg)
    print()
    print(" %1 : Expression régulière de sélection des fichiers (obligatoire)")
    print(" %2 : Expression régulière des caractères à remplacer (facultatif)")
    print(" %3 : Expression des caractères de remplacement (facultatif)")
    print(" %4 : -exec (effectue le renommage) (facultatif)")
    # getch()
    exit(1)


try:
    todo = False
    regexp_liste = ""
    regexp_source = ""
    regexp_dest = ""
    
    if nb_args == 1:
        regexp_liste, regexp_source = (argv[0],) * 2
        
    elif nb_args == 2:
        regexp_liste, regexp_source, regexp_dest = (argv[0], argv[0], argv[1]) 
        
    elif nb_args == 3:
        if argv[2].lower() in ("exec", "-exec"):
            regexp_liste, regexp_source, regexp_dest = (argv[0], argv[0], argv[1]) 
            todo = True
        else:
            regexp_liste, regexp_source, regexp_dest = argv[:]
        
    elif nb_args == 4:
        if argv[3].lower() not in ("exec", "-exec"):
            msg_erreur(f"Paramètre invalide : {argv[3]}")
        regexp_liste, regexp_source, regexp_dest = (argv[0], argv[1], argv[2]) 
        todo = True
        
    else:
        msg_erreur(f"Nombre de paramètres incorrects : {nb_args}")
        
    repertoire = os.getcwd()
    
    print(f"Répertoire source : {couleurRecherche}{repertoire}{fcolors.ENDC}")
    
    try:
        rxl = re.compile(regexp_liste, re.IGNORECASE)
    except Exception as e:
        print(f"Erreur dans l'expression régulière de recherche: {couleurRegexp}{regexp_liste}\n  {couleurErreur}{e}{fcolors.ENDC}")
        exit(1)
        
    print(f"Recherche des fichiers : {couleurRecherche}{regexp_liste}{fcolors.ENDC}")
    
    try:
        rxs = re.compile(regexp_source, re.IGNORECASE)
    except Exception as e:
        print(f"Erreur dans l'expression régulière de filtrage: {couleurRegexp}{regexp_source}\n  {couleurErreur}{e}{fcolors.ENDC}")
        exit(1)
        
    print(f"Remplacement de: {couleurRegexp}{regexp_source}{fcolors.ENDC}  par: {couleurRegexp}{regexp_dest}{fcolors.ENDC}")
    print()
    
    files_found, nb_files, nb_reps, nb_changed = (0,) * 4
    
    for f in os.listdir('.'): # 'D:\Mes Documents\dwhelper'
        if not os.path.isdir(f):
            files_found += 1
            if rxl.search(f):
                nb_files += 1
                new_file = ""
                new_f = ""
                
                match = rxs.search(f)
                if match:
                    index = 0
                    for m in re.finditer(rxs, f):
                        debut, fin = m.start(), m.end()
                        if index < debut: 
                            fprint(f[index:debut])
                            new_file += f[index:debut]
                            new_f    += f[index:debut]
                            
                        fprint(f"{couleurMatch}{f[debut:fin]}{fcolors.ENDC}")
                        new_file += f"{couleurMatch}{m.expand(regexp_dest)}{fcolors.ENDC}"
                        new_f    += m.expand(regexp_dest)
                        index = fin
                        
                    if index < len(f):
                        fprint(f[index:])
                        new_file += f[index:]
                        new_f    += f[index:]
                        
                    if len(f) < longeurMaxFichier :
                        fprint(" " * (longeurMaxFichier -len(f)))
                    else:
                        fprint("\n    ")
                        
                    if nb_args > 1:
                        fprint("-->", new_file)
                        if todo:
                            try:
                                os.rename(f, new_f)
                                nb_changed += 1
                                fprint(f" {fcolors.GVERT}Ok{fcolors.ENDC}")
                                
                            except Exception as e:
                                print(f" {fcolors.GROUGE}(Ko)")
                                fprint(f"{e}{fcolors.ENDC}")
                else:
                    fprint(f)
                    
                print()
        else:
            nb_reps += 1
            
    print(f"\n{nb_reps} répertoires et {files_found} fichiers trouvés dans le répertoire")
    if nb_changed > 1:
        print(f"{nb_changed} fichiers renommés, ", end="")
    else:
        print(f"{nb_changed} fichier renommé, ", end="")
     
    if nb_files > 1:
        print(f"sur {nb_files} fichiers filtrés")
    else:
        print(f"sur {nb_files} fichier filtré")
     

except Exception:
    traceback.print_exc()

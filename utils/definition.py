from inspect import Parameter
try:
    from colors import *
except ModuleNotFoundError:
    from utils.colors import *
  
import os

if __name__ != "__main__":
    print("loading definition.py")

_, colstr = os.popen('mode con | findstr Colonne', 'r').read().split()
colsize = int(colstr)
print("nombre de colonnes : {}".format(colsize))


def print2screen(type_attributs, liste_attributs):
    setColor(fcolors.VERT)
    print("{}:".format(type_attributs))
    setColor(fcolors.BLANC)

    ligne_str = ""

    for a in liste_attributs:
        if len("  {}{}".format(ligne_str, a)) < colsize:
            if ligne_str:
                ligne_str += ", {}".format(a)
            else:
                ligne_str = "  {}".format(a)
            
        else:
            print(ligne_str)
            ligne_str = ""

    if ligne_str: print(ligne_str)
  

def printdesc(variable):

    setColor(fcolors.JAUNE)
    print("class:=", variable.__class__.__name__, ", desc:=", variable)
    try:
        lst_garbage = []
        lst_fonctions = []
        lst_constantes = []
        lst_variables = []

        ligne_str = ""
        for a in dir(variable):
            try:
                if a.startswith("_"):
                    pass
                
                else:
                    if callable(getattr(variable, a)):
                        lst_fonctions.append(a)
                    else:
                        if a[0] in "AZERTYUIOPQSDFGHJKLMWXCVBN":
                            lst_constantes.append(a)
                        else:
                            lst_variables.append(a)
                      
            except Exception as e:
                # print("error sur attribut : {}, {}".format(a, e))
                lst_garbage.append(a)

        print2screen("Fonctions", lst_fonctions)
        print2screen("Constantes", lst_constantes)
        print2screen("Variables", lst_variables)
        print2screen("Erreurs", lst_garbage)
        print()

    except Exception as e:
        print(traceback.print_exc())


def printdef(variable):
  # --------- --------- --------- --------- --------- --------- --------- --------- 
  print(f"def : {variable}")
  print(fcolors.VERT + "Attributs :" + fcolors.ENDC)
  print("-"*10)

  max_type_size = 0
  max_name_size = 0
  for attribut in dir(variable):
    if not attribut.startswith("__"):
      if not ("method"   in type(getattr(variable, attribut)).__name__ or 
              "function" in type(getattr(variable, attribut)).__name__ ):
        name_size = len(attribut)
        type_size = len(type(getattr(variable, attribut)).__name__)

        if name_size > max_name_size: max_name_size = name_size
        if type_size > max_type_size: max_type_size = type_size
        
  max_name_size += 2
  for attribut in dir(variable):
    if not attribut.startswith("__"):
      if not ("method"   in type(getattr(variable, attribut)).__name__ or 
              "function" in type(getattr(variable, attribut)).__name__ ):
        # print(fcolors.BLEU + f"  {attribut}{' '*100}"[:max_name_size], end="")
        print(fcolors.CYAN + f"  {attribut}{' '*100}"[:max_name_size], end="")
        print(fcolors.ENDC + " as " + fcolors.JAUNE, end="")
        print(f"{type(getattr(variable, attribut)).__name__}{' '*100}"[:max_type_size], end="")
        resultat = f" = {getattr(variable, attribut)}".replace("\n", ", ")
        print(fcolors.ENDC, end="")
        if len(resultat) < colsize - max_name_size - max_type_size - 4:
          print(resultat)
        else:
          print(resultat[:colsize - max_name_size - max_type_size - 4 - 5], "...")

  import inspect
  # --------- --------- --------- --------- --------- --------- --------- --------- 
  max_name_size = 0
  for attribut in dir(variable):
    if not attribut.startswith("__"):
      if  ("method"   in type(getattr(variable, attribut)).__name__ or 
           "function" in type(getattr(variable, attribut)).__name__ ):
        name_size = len(attribut)
        if name_size > max_name_size: max_name_size = name_size



  max_name_size += 2
  methods = {"noArg":[], "Args":[], "Other":[]}
  method_list = []
  args_method_list = []
  other_method_list = []


  for attribut in dir(variable):
    if not attribut.startswith("__"):
      if  ("method"   in type(getattr(variable, attribut)).__name__ or
           "function" in type(getattr(variable, attribut)).__name__ ):
        try:
          res = getattr(variable, attribut)()
          is_liste = False
          if (isinstance(res, list) or isinstance(res, set)):
            is_liste = True
            resultat = " = "
            
            for val in res:
              if len(resultat) < 4:
                resultat += f"{val}\n"
              else:
                resultat += f"{' '*30} - {val}\n"
          else:
            resultat = f" = {res}".replace("\n", ", ")
            
          if is_liste or len(resultat) < colsize - max_name_size - 4:
            methods["noArg"].append({"attr":attribut, "valeur":f"{resultat}"})
          else:
            methods["noArg"].append({"attr":attribut, "valeur":f"{resultat[:colsize - max_name_size - 4 - 5]}..."})
          
        except Exception as e:
          err = f"{e}".replace(f"{attribut}() ", "")
          if "argument" in f"{e}":
            methods["Args"].append({"attr":attribut, "err":err})
          
          else:
            methods["Other"].append({"attr":attribut, "err":err})

            
  # --------- --------- --------- --------- --------- --------- --------- --------- 
  if len(methods["noArg"]) > 0:
    print()
    print(fcolors.VERT + "Methods :" + fcolors.ENDC)
    print("-"*8)
    
    for une_methode in methods["noArg"]:
      print(fcolors.VIOLET, end="")
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" ")
      print(fcolors.ENDC, end="")
      print(f"{une_methode['valeur']}")


  # --------- --------- --------- --------- --------- --------- --------- --------- 
  if len(methods["Args"]) > 0:
    print()
    print(fcolors.VERT + "Methods with args :" + fcolors.ENDC)
    print("-"*18)
    
    for une_methode in methods["Args"]:
      print(fcolors.VIOLET, end="")
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" : ")
      print(fcolors.ENDC, end="")
      print(inspect.getfullargspec(getattr(variable, une_methode['attr'])).annotations, end="")
      print(f"  {une_methode['err']}")
    
    
  # --------- --------- --------- --------- --------- --------- --------- --------- 
  if len(methods["Other"]) > 0:
    print()
    print(fcolors.VERT + "Other Methods :" + fcolors.ENDC)
    print("-"*14)
    
    for une_methode in methods["Other"]:
      print(fcolors.VIOLET, end="")
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" : ")
      print(fcolors.ENDC, end="")
      print(f"{une_methode['err']}")
    
    
  print()

if __name__ == "__main__":
  printdef(printdesc)
  from msvcrt import getch
  getch()
  print("fin")
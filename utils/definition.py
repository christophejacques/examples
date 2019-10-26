from inspect import Parameter
from utils.colors import *


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
        print(fcolors.BLEU + f"  {attribut}{' '*100}"[:max_name_size], end="")
        print(fcolors.ENDC + " as " + fcolors.JAUNE, end="")
        print(f"{type(getattr(variable, attribut)).__name__}{' '*100}"[:max_type_size], end="")
        resultat = f" = {getattr(variable, attribut)}".replace("\n", ", ")
        print(fcolors.ENDC, end="")
        if len(resultat) < 80:
          print(resultat)
        else:
          print(resultat[:80], "...")

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
          resultat = f" = {getattr(variable, attribut)()}".replace("\n", ", ")
          if len(resultat) < 100:
            methods["noArg"].append({"attr":attribut, "valeur":f"{resultat}"})            
          else:
            methods["noArg"].append({"attr":attribut, "valeur":f"{resultat[:100]}..."})
          
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
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" ")
      print(f"{une_methode['valeur']}")


  # --------- --------- --------- --------- --------- --------- --------- --------- 
  if len(methods["Args"]) > 0:
    print()
    print(fcolors.VERT + "Methods with args :" + fcolors.ENDC)
    print("-"*18)
    
    for une_methode in methods["Args"]:
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" : ")
      print(inspect.getfullargspec(getattr(variable, une_methode['attr'])).annotations, end="")
      print(f"  {une_methode['err']}")
    
    
  # --------- --------- --------- --------- --------- --------- --------- --------- 
  if len(methods["Other"]) > 0:
    print()
    print(fcolors.VERT + "Other Methods :" + fcolors.ENDC)
    print("-"*14)
    
    for une_methode in methods["Other"]:
      print(f"  {une_methode['attr']}(){' '*100}"[:max_name_size+2], end=" : ")
      print(f"{une_methode['err']}")
    
    
  print()


from os import system

class fcolors:
  ENDC     = '\033[0m'
  
  NOIR     = '\033[30m'
  ROUGE    = '\033[31m'
  VERT     = '\033[32m'
  JAUNE    = '\033[33m'
  BLEU     = '\033[34m'
  VIOLET   = '\033[35m'
  CYAN     = '\033[36m'
  BLANC    = '\033[37m'

  GNOIR    = '\033[90m'
  GROUGE   = '\033[91m'
  GVERT    = '\033[92m'
  GJAUNE   = '\033[93m'
  GBLEU    = '\033[94m'
  GMAGENTA = '\033[95m'
  GCYAN    = '\033[96m'
  GBLANC   = '\033[97m'
  
  BOLD      = '\033[1m'
  CITALIC   = '\33[3m'
  UNDERLINE = '\033[4m'
  CBLINK    = '\33[5m'
  CBLINK2   = '\33[6m'
  CSELECTED = '\33[7m'
  
  
class bcolors:
  ENDC   = '\033[0m'
  
  NOIR    = '\033[40m'
  ROUGE   = '\033[41m'
  VERT    = '\033[42m'
  JAUNE   = '\033[43m'
  BLEU    = '\033[44m'
  MAGENTA = '\033[45m'
  CYAN    = '\033[46m'
  BLANC   = '\033[47m'

  GNOIR    = '\033[100m'
  GROUGE   = '\033[101m'
  GVERT    = '\033[102m'
  GJAUNE   = '\033[103m'
  GBLEU    = '\033[104m'
  GMAGENTA = '\033[105m'
  GCYAN    = '\033[106m'
  GBLANC   = '\033[107m'

def pushCursor():
  print("\033[s", end="")
  
def popCursor():
  print("\033[u", end="")
  
def setColor(color):
  print(color, end="")
  
  
def gotoXY(x, y):
  return "\033[" + str(y) + ";" + str(x) + "H"

  
def printXY(x, y, *texte, **kw):
  print( gotoXY(x, y), *texte , **kw)

  
# Activation des code ANSI dans le terminal
system('color')

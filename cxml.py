import msvcrt
from xml.dom.minidom import parse, Document, Element
import traceback

if __name__ != "__main__":
  print("loading xml")

class unElement(Element):

  def __init__(self, elt):
    Element.__init__(self, elt.tagName)
    if elt.childNodes:
        self.childNodes = elt.childNodes        
  
  def hasElementByTagName(self, tag):
    return len(self.getElementsByTagName(tag)) > 0
    
  def cgetElementsByTagName(self, tag, *args):
    lres = []
    for unElt in Element.getElementsByTagName(self, tag):
      lres.append(unElement(unElt))

    return lres

  def getDataFromTextElement(self, tag_name):
    res = ""
    for unNode in self.getElementsByTagName(tag_name):
      for nodeTexte in unNode.childNodes:
        if nodeTexte.nodeType == nodeTexte.TEXT_NODE:
          res += "{}".format(nodeTexte.data.strip())

    return res


class XML(unElement):

  def __init__(self, nom_fichier):
    self.racine = parse(nom_fichier)
    self.racine.tagName = "root"
    unElement.__init__(self, self.racine)
    
  def __enter__(self):
    return self.racine


try:
  x = XML("C:/Users/utilisateur/OneDrive/Programmation/python/examples/fichier.xml") 
  #x = XML("C:/Users/cjacq/OneDrive/Programmation/python/examples/fichier.xml") 
  
  for xml in x.getElementsByTagName("html"):
    print("balise html")
    for balise in xml.getElementsByTagName("head"):
      print("balise head")
      if unElement(balise).hasElementByTagName("h1"): print(unElement(balise).getDataFromTextElement("h1"))
      print("P:", unElement(balise).getDataFromTextElement("P"))
      print()

    for balise in xml.getElementsByTagName("body"):
      print("balise body")
      for ligne in xml.getElementsByTagName("ligne"):
        if unElement(ligne).hasElementByTagName("h1"): print("h1:", unElement(ligne).getDataFromTextElement("h1"))
        if unElement(ligne).hasElementByTagName("h2"): print("h2:", unElement(ligne).getDataFromTextElement("h2"))
        print("P:", unElement(ligne).getDataFromTextElement("P"))
        print()

except Exception as e:
  print(traceback.print_exc())

print("Appuyez sur une touche")
msvcrt.getch()

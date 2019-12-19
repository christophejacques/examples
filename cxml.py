from msvcrt import getch
from utils.definition import printdesc
from xml.dom.minidom import parse, Document, Element
import traceback
from os import environ
from utils.colors import *

if __name__ != "__main__":
  print("loading xml")


class UnElement(Element):
  
  def __init__(self, elt):
    Element.__init__(self, elt.tagName)
    if elt.childNodes:
        self.childNodes = elt.childNodes
  
  @property
  def firstChild(self):
    return UnElement(super().firstChild)
  
  @property
  def lastChild(self):
    return UnElement(super().lastChild)
  
  def hasElementByTagName(self, tag):
    return len(super().getElementsByTagName(tag)) > 0
    
  def getElementsByTagName(self, tag):
    return list(map(UnElement, super().getElementsByTagName(tag)))

  def getTagNames(self):
    lres = []
    for balise in self.childNodes:
      if balise.nodeType == balise.ELEMENT_NODE:
        lres.append(balise.tagName)
        
    return lres

  def getDataFromTextElement(self, tag_name):
    res = ""
    premiere_node, *_ = self.getElementsByTagName(tag_name)
    for node_texte in premiere_node.childNodes:
      if node_texte.nodeType == node_texte.TEXT_NODE:
        res += "{}".format(node_texte.data.strip())

    return res

  def getDataFromTextsElements(self, tag_name):
    res = ""
    for unNode in self.getElementsByTagName(tag_name):
      for nodeTexte in unNode.childNodes:
        if nodeTexte.nodeType == nodeTexte.TEXT_NODE:
          res += "{}".format(nodeTexte.data.strip())

    return res


couleur_balise = fcolors.BLEU


def parcourt(balise, niveau=0):
  espace = "  " * niveau
  res = False
  for une_balise in balise.childNodes:
    if une_balise.nodeType == une_balise.ELEMENT_NODE:
      setColor(couleur_balise)
      print("\n{}<{}>".format(espace, une_balise.tagName), end="")
      setColor(fcolors.ENDC)
      if parcourt(une_balise, niveau+1):
        setColor(couleur_balise)
        print("</{}>".format(une_balise.tagName), end="")
        setColor(fcolors.ENDC)
      else:
        setColor(couleur_balise)
        print("\n{}</{}>".format(espace, une_balise.tagName), end="")
        setColor(fcolors.ENDC)
      res = False

    elif une_balise.nodeType == une_balise.TEXT_NODE:
      stxt = "{}".format(une_balise.data.strip())
      if stxt:
        setColor(fcolors.JAUNE)
        print(stxt, end="")
        setColor(fcolors.ENDC)
        res = True

  return res


class XML(UnElement):

  def __init__(self, nom_fichier):
    self.racine = parse(nom_fichier)
    self.racine.tagName = "root"
    UnElement.__init__(self, self.racine)
    
  def __enter__(self):
    return self.racine


try:
  username = environ["USERNAME"]
  x = XML("C:/Users/{}/OneDrive/Programmation/python/examples/fichier.xml".format(username))

  parcourt(x)
  exit(0)

  if True:
    for html in x.getElementsByTagName("html"):
      print("{} ({}) => {}".format(html.tagName, len(html.getTagNames()), ", ".join(html.getTagNames())))
      for head in html.getElementsByTagName("head"):
        print("  {} ({}) => {}".format(head.tagName, len(head.getTagNames()), ", ".join(head.getTagNames())))
        if head.hasElementByTagName("h1"): print("    {}".format(head.getDataFromTextElement("h1")))

      for body in html.getElementsByTagName("body"):
        print("  {} ({}) => {}".format(body.tagName, len(body.getTagNames()), ", ".join(body.getTagNames())))
        for balise in body.getElementsByTagName("ligne"):
          print("    {} ({}) => {}".format(balise.tagName, len(balise.getTagNames()), ", ".join(balise.getTagNames())))
          if balise.hasElementByTagName("h1"): print("      h1:", balise.getDataFromTextElement("h1"))
          if balise.hasElementByTagName("h2"): print("      h2:", balise.getDataFromTextElement("h2"))
          if balise.hasElementByTagName("P") : print("      P:" , balise.getDataFromTextElement("P"))


  printdesc(x)
  y = x.firstChild
  printdesc(y)


except Exception as e:
  print(traceback.print_exc())


#getch()


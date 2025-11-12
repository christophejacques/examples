from requests import Session, Response, codes
from html.parser import HTMLParser
from typing import Tuple


DEBUG = False
MY_HEADER: dict = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
      'Connection': 'keep-alive',
      }


def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def attributs_contient_classes(
        attributs_actuels: list, 
        classes_recherchees: list) -> bool:

    trouve: bool = len(classes_recherchees[-1]) == 0

    # recherche si un des attributs est "classe""
    for attribut, valeurs in attributs_actuels:
        if attribut == "class":
            trouve = True

            # recherche dans l'attribut "classe" trouvé
            # s'il contient toutes les classes demandées
            for une_classe in classes_recherchees[-1]:
                if une_classe not in valeurs.split():
                    # une des classes n'est pas trouvée
                    # le résultat est donc faux
                    trouve = False
                    break

    return trouve


class Directory:

    def __init__(self, recorded: bool, attrs: list):
        self.recorded = recorded
        self.attrs = attrs


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.level: int = 0
        self.path: str = ""
        self.result: list = list()
        self.liste_recherche = list()
        self.datas: list = list()
        self.has_data: bool = False
        self.skip_branch: bool = False

    def handle_startendtag(self, tag, attrs):
        if self.finish:
            return
            
        path = self.path+ f" {tag}"
        dprint(f"Start-End: {path} {attrs}")

        debut = path.find(self.recherche)
        if debut >= 0:
            if path[debut:] == self.recherche:
                trouve = attributs_contient_classes(attrs, self.classes)
                if trouve:
                    # self.found = True
                    dprint(f"- start-add end: {self.path} {attrs}")
                    self.result.append({
                        "path": path,
                        "attrs": attrs,
                        "text": ""
                        })

        elif self.found and not self.tout:
            self.findnext()

    def handle_starttag(self, tag, attrs):
        if self.finish:
            return

        self.has_data = False            
        path = self.path + (" " if self.path else "") + tag
        
        debut = path.find(self.recherche)
        if debut >= 0:
            if path[debut:] == self.recherche:
                trouve = attributs_contient_classes(attrs, self.classes)
                if trouve:
                    self.found = True
                else:
                    self.found = False

        elif self.found and not self.tout:
            self.findnext()

        if tag in ("br", "link", "meta"):
            return 
        
        self.path = path
        self.attrs = attrs
        self.datas.append(Directory(False, attrs))
        self.level += 1 
        dprint(f"Start: {self.path} {attrs} {[d.recorded for d in self.datas]}")

    def handle_endtag(self, tag):
        if self.finish:
            return

        debut = self.path.find(self.recherche)
        # print(f"check end: {self.path}", "/", self.recherche)
        if self.found and debut >= 0 and not self.datas[-1].recorded:
            dprint(f"- add end: {self.path} {self.datas[-1].attrs} {[d.recorded for d in self.datas]}")
            self.result.append({
                "path": self.path,
                "attrs": self.datas[-1].attrs,
                "text": ""
                })

        # print("check end:", debut, self.found, self.path, self.recherche)
        if self.found and debut >= 0 and self.path[debut:] == self.recherche and not self.tout:
            self.findnext()

        self.level -= 1
        if self.datas:
            self.datas.pop()
        
        while self.path.split(" ")[-1] != tag:
            self.path = " ".join(self.path.split(" ")[:-1])

        self.path = " ".join(self.path.split(" ")[:-1])
        # dprint(f"Pop ({tag}): {self.path} {[d.recorded for d in self.datas]}")
        
    def handle_data(self, data):
        if self.finish or not self.found:
            return

        link_text = data.strip()
        if link_text:
            self.has_data = True

        if link_text and self.recherche in self.path:
            self.datas[-1].recorded = True
            dprint("- add data:", self.path, self.datas[-1].attrs, [d.recorded for d in self.datas])
            self.result.append({
                "path": self.path,
                "attrs": self.datas[-1].attrs,
                "text": link_text
                })

    def load_str(self, document: str) -> Tuple[bool, str]:
        self.document = document
        return True, "loaded"

    def load_url(self, url: str) -> Tuple[bool, str]:
        session: Session = Session()
        reponse: Response = session.get(url, timeout=(5, 15), headers=MY_HEADER)

        if not reponse.ok:
            return False, f"{reponse}: {reponse.url}"

        type_page, *encoding = reponse.headers.get("Content-Type").split(";")  # type: ignore[union-attr]

        if not "text/html" in type_page:
            return False, f"type_page problem : {type_page}"

        return self.load_str(reponse.text)


    def init_find(self, recherche):
        self.found = False
        self.classes = list()
        for selector in recherche.split():
            self.classes.append(selector.split(".")[1:])
        print("classes:", self.classes)

        self.recherche = " ".join([t.split(".")[0] for t in recherche.split()])
        print("recherche:", self.recherche)
        dprint()

    def find(self, recherche: str, tout: bool=False):
        self.datas = list()
        self.init_find(recherche)

        self.tout = tout
        self.finish = False
        self.result.clear()
        self.level = 0
        self.feed(self.document)

    def findnext(self):
        if self.liste_recherche:
            dprint("find next")
            self.init_find(self.liste_recherche.pop(0))
            self.skip = False
        else:
            dprint("finish")
            self.finish = True

    def findall(self, recherche: str):
        self.find(recherche, tout=True)

    def findsequence(self, liste_recherche: list[str]):
        self.liste_recherche = liste_recherche
        self.find(self.liste_recherche.pop(0))

    def get_result(self):
        return self.result



if __name__ == "__main__":

    result = """
    <html>
        <head>
            <title>Titre de la fenetre</title>
            <meta content="html/text" />
        </head>
        <body>
            <div>Fausse alerte</div>
            <div class="tip tup top">trouvé</div>
            <div class="no-data"></div>
        </body>
        <script>
            document.write('He ho !');
        </script>
    </html>
    """

    result = """
    <html>
        <body>
            <div>Erreur1</div>
            <div class="tip tup top">
                <span class="gras"></span>
            </div>
            <div>Erreur2</div>
            <div class="box" />
            <div>Erreur3</div>
        </body>
    </html>
    """
    url: str = "https://www.python.org/"

    parser = MyHTMLParser()

    # ok, result = parser.loadstr(result)
    ok, result = parser.load_url(url)
    if not ok:
        exit()

    # parser.findall("div.top")
    # parser.findall("html body div div div section div div h2 span")
    parser.findall("html body div div div section div div.small-widget p a")
    # parser.findall("img.python-logo")

    # parser.findsequence([
    #     "span.icon-get-started", 
    #     "span.icon-documentation"])
    parser.close()

    print()
    for res in parser.get_result():
        print(res)
    print("\nend level:", parser.level)

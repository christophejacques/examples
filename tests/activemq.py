from requests import Session, Response, codes
from html.parser import HTMLParser
from typing import Tuple


DEBUG = True
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


class Directory:

    def __init__(self, recorded: bool, attrs: list):
        self.recorded = recorded
        self.attrs = attrs


class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.session: Session = Session()

        self.level: int = 0
        self.path: str = ""
        self.result: list = list()
        self.liste_recherche = list()
        self.datas: list = list()
        self.classes: list = list()
        self.ident: list = list()
        self.has_data: bool = False
        self.skip_branch: bool = False

    @staticmethod
    def attributs_match_class(attributs_actuels: list, data_attrs: list) -> bool:
        trouve = False

        # recherche si un des attributs est "classe""
        for attribut, valeurs in attributs_actuels:
            if attribut == "class":
                trouve = True

                # recherche dans l'attribut "classe" trouvé
                # s'il contient toutes les classes demandées
                for une_classe in data_attrs:
                    if une_classe not in valeurs.split():
                        # une des classes n'est pas trouvée
                        # le résultat est donc faux
                        return False

        return trouve

    @staticmethod
    def attributs_match_ident(attributs_actuels: list, data_attrs: list) -> bool:
        trouve = False

        # recherche si un des attributs est "classe""
        for attribut, valeurs in attributs_actuels:
            if attribut == "id":
                trouve = True

                # recherche dans l'attribut "id" trouvé
                # s'il contient l'identifiant demandé
                for un_id in data_attrs:
                    if un_id not in valeurs.split():
                        # une des classes n'est pas trouvée
                        # le résultat est donc faux
                        return False

        return trouve

    def attributs_match_path(self) -> bool:
        look_for_classes: bool 
        look_for_identif: bool 

        dprint("reche:", self.recherche, "|", self.path)
        dprint("attrs:", [d.attrs for d in self.datas])

        trouve: bool = True
        nb_items = len(self.recherche.split())
        for i in range(nb_items, 0, -1):
            trouve = False
            dprint(" * check:", self.classes[-i], self.ident[-i], "/", self.datas[-i].attrs, end= " -> ")

            look_for_classes = len(self.classes[-i]) > 0
            look_for_identif = len(self.ident[-i]) > 0

            if not (look_for_classes or look_for_identif):
                dprint("Vrai")
                trouve = True
                continue

            if look_for_classes:
                dprint(" CC ", end="")
                trouve = self.attributs_match_class(self.datas[-i].attrs, self.classes[-i])
                if not trouve:
                    dprint("Faux(c)")
                    break

            elif look_for_identif:
                dprint(" CI ", end="")
                trouve = self.attributs_match_ident(self.datas[-i].attrs, self.ident[-i])
                if not trouve:
                    dprint("Faux(i)")
                    break

            dprint(trouve)

        return trouve

    def handle_startendtag(self, tag, attrs):
        if self.finish:
            return
            
        path = self.path+ f" {tag}"
        dprint(f"Start-End: {path} {attrs}")

        debut = path.find(self.recherche)
        if debut >= 0:
            if path[debut:] == self.recherche:
                trouve = self.attributs_match_path()
                if trouve:
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

        if tag in ("br", "link", "meta"):
            return 
        
        self.level += 1 
        self.has_data = False            
        path = self.path + (" " if self.path else "") + tag
        self.path = path
        self.attrs = attrs
        self.datas.append(Directory(False, attrs))
        
        dprint(f"Start: {path} {attrs}")

        debut = path.find(self.recherche)
        if debut >= 0:
            if path[debut:] == self.recherche:
                trouve = self.attributs_match_path()
                if trouve:
                    self.found = True
                else:
                    self.found = False

        elif self.found and not self.tout:
            self.findnext()


    def handle_endtag(self, tag):
        if self.finish:
            return

        debut = self.path.find(self.recherche)
        # print(f"check end: {self.path}", "/", self.recherche)
        if self.found and debut >= 0 and not self.datas[-1].recorded:
            dprint(f"- add end: {self.path} {self.datas[-1].attrs}")
            self.result.append({
                "path": self.path,
                "attrs": self.datas[-1].attrs,
                "text": ""
                })

        # print("check end:", debut, self.found, self.path, self.recherche)
        if self.found and debut >= 0 and self.path[debut:] == self.recherche and not self.tout:
            self.findnext()

        while self.path.split(" ")[-1] != tag:
            self.pop()

        self.pop()
                
    def pop(self):
        self.path = " ".join(self.path.split(" ")[:-1])
        self.level -= 1
        if self.datas:
            self.datas.pop()

    def handle_data(self, data):
        if self.finish or not self.found:
            return

        link_text = data.strip()
        if link_text:
            self.has_data = True

        if link_text and self.recherche in self.path:
            self.datas[-1].recorded = True
            dprint("- add data:", self.path, self.datas[-1].attrs)
            self.result.append({
                "path": self.path,
                "attrs": self.datas[-1].attrs,
                "text": link_text
                })

    def load_str(self, document: str) -> Tuple[bool, str]:
        self.document = document
        return True, "loaded"

    def load_url(self, url: str) -> Tuple[bool, str]:
        try:
            reponse: Response = self.session.get(url, timeout=(5, 15), headers=MY_HEADER)
        except Exception as erreur:
            return False, f"{erreur}"

        if not reponse.ok:
            return False, f"{reponse}: {reponse.url}"

        type_page, *encoding = reponse.headers.get("Content-Type").split(";")  # type: ignore[union-attr]

        if not "text/html" in type_page:
            return False, f"type_page problem : {type_page}"

        return self.load_str(reponse.text)


    def init_find(self, recherche: str):
        self.found = False
        self.classes = list()
        self.ident = list()

        for selector in recherche.split():
            self.classes.append(selector.split(".")[1:])
        print("classes:", self.classes)
        self.recherche = " ".join([t.split(".")[0] for t in recherche.split()])

        for selector in self.recherche.split():
            self.ident.append(selector.split("#")[1:])
        print("ident:", self.ident)
        self.recherche = " ".join([t.split("#")[0] for t in self.recherche.split()])

        print("recherche:", self.recherche)
        dprint()

    def find(self, recherche: str, tout: bool=False, exact: bool=False):
        self.datas = list()
        self.init_find(recherche)

        self.tout = tout
        self.exact = exact
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

    def print(self): 
        print()
        for res in self.get_result():
            print(res)
        print("\nend level:", parser.level)


if __name__ == "__main__":

    result2 = """
    <html>
        <body class="bg">
            <div>Erreur1</div>
            <div class="tip tup top">
                <span id="gras" class="gras"></span>
                <span id="gris" class="gris"></span>
                <span id="gros" class="gros"></span>
            </div>
            <div id="erreur">Erreur2</div>
            <div class="box" />
            <div>Erreur3</div>
        </body>
    </html>
    """
    url: str = "https://www.python.org/"

    parser = MyHTMLParser()

    # ok, result = parser.load_url(url)
    # if not ok:
    #     print(result)
    #     exit()

    # parser.findall("html body div div div section div div h2")
    # parser.findall("html body div div div section div div h2.widget-title span")
    # parser.findall("html body div div div section div div.small-widget p a")
    # parser.findall("img.python-logo")
    # parser.print()


    ok, result = parser.load_str(result2)
    if not ok:
        print(result)
        exit()

    parser.findall("body.bg div#erreur")
    # parser.findall("span")
    # parser.findall("div.top span#gris")

    # parser.findsequence([
    #     "span.icon-get-started", 
    #     "span.icon-documentation"])

    parser.print()
    parser.close()

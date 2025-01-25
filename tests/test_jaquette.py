import webbrowser
from requests import Session, Response, codes
from html.parser import HTMLParser
from typing import Optional


MY_HEADER: dict = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
      'Connection': 'keep-alive',
      }


def fprint(*args):
    print(*args, flush=True)


class Tag:

    __tag: str
    __classes: list
    __ctrl_cls: bool

    def __init__(self, tag_classes: str):
        self.__tag, *self.__classes = tag_classes.split(".")
        self.__ctrl_cls = False

    def setCtrlClasses(self, controle: bool) -> None:
        self.__ctrl_cls = controle

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False

        if  self.__tag != other.__tag:
            return False

        if self.__ctrl_cls:
            if len(self.__classes) != len(other.__classes):
                return False

            compare = zip(self.__classes, other.__classes)
            for items in list(compare):
                if items[0] != items[1]:
                    return False

        return True

    def __str__(self):
        return f"{self.__tag} {self.__classes}"


class TagSelector:

    __selector: list

    def __init__(self, liste_tags: Optional[list[Tag]] = list()):

        if not isinstance(liste_tags, list):
            raise Exception("La variable liste_tags n'est pas de type list.")

        for tag in liste_tags:
            if not isinstance(tag, Tag):
                raise Exception(f"La valeur ({tag}) de la liste liste_tags n'est pas de type Tag.")

        self.__selector = liste_tags.copy()

    def clear(self) -> None:
        self.__selector = list()

    def add_tag(self, tag: Tag) -> None:
        if not isinstance(tag, Tag):
            raise Exception(f"la variable tag ({tag}) n'est pas de type Tag")

        self.__selector.append(tag)

    def setCtrlClasses(self, controle: bool) -> None:
        for tag in self.__selector:
            tag.setCtrlClasses(controle)

    def begins_with(self, other, with_classes: bool = False) -> bool:
        if not isinstance(other, TagSelector):
            raise Exception(f"({other}) n'est pas de type TagSelector")

        if with_classes:
            pass

        compare = zip(self.__selector, other.__selector)
        for items in list(compare):
            print("begins:", *items)
            if items[0] != items[1]:
                return False

        return True

    def __str__(self) -> str:
        ls_str: str = ""
        for tag in self.__selector:
            ls_str += f" {tag} >"

        return ls_str[:-1].strip()

    def __eq__(self, other) -> bool:
        if not isinstance(other, TagSelector):
            return False

        size: int = len(self.__selector)
        if size != len(other.__selector) or size == 0:
            return False

        liste_tests: list[bool] = [self.__selector[i] == other.__selector[i] for i in range(size)]
        return all(liste_tests)


if 1 == 1:
    selector = TagSelector()
    for text in ["article.post", "header.entry-header", "h1"]:
        tag = Tag(text)
        # print(tag)
        selector.add_tag(tag)

    selector.setCtrlClasses(True)
    print("begins:", selector.begins_with(TagSelector([Tag("article")])))

    # print(selector)
    # print(selector == TagSelector([Tag("article.post"), Tag("header.entry-header"), Tag("h1")]))

    selector.setCtrlClasses(False)
    # print("begins:", selector.begins_with(TagSelector([Tag("article"), Tag("header"), Tag("h1")])))
    # print("begins:", selector.begins_with(TagSelector([Tag("article"), Tag("header")])))
    print("begins:", selector.begins_with(TagSelector([Tag("article")])))
    print(selector == TagSelector([]))
    exit()


class HTMLRelativeTagListParser(HTMLParser):

    def __init__(self, liste_tag: list):
        super().__init__()
        self.liste_tag = liste_tag
        self.current_tag_liste = liste_tag.copy()
        self.current_tag = self.current_tag_liste.pop(0)

        self.begin: bool = False
        self.found: bool = False
        self.get_data: bool = False
        self.innerText: str = ""

    def handle_data(self, data):
        if self.get_data:
            self.get_data = False
            self.innerText = data.strip()

    def handle_starttag(self, tag, attrs):
        if self.found:
            return

        if tag.lower() != self.current_tag:
            # tag non trouve en reinitialise si besoin
            if self.begin:
                self.current_tag_liste = self.liste_tag.copy()
                self.current_tag = self.current_tag_liste.pop(0)

            self.begin = False
            return

        if self.current_tag_liste:
            # il reste des tags a trouver
            self.current_tag = self.current_tag_liste.pop(0)
            self.begin = True

        else:
            # le dernier tag est trouve
            self.found = True
            self.get_data = True
            self.result = tag, attrs


class HTMLTagParser(HTMLParser):

    def __init__(self, tag: str, type_style: str, valeurs_style: str):
        # fprint(f"HTMLTagParser.__init__({tag}, {type_style}, {valeurs_style!r})")
        # fprint(dir(self))
        super().__init__()
        self.tag: str = tag.lower()
        self.type_style: str = type_style.lower()
        self.valeurs_style: list = valeurs_style.split()
        self.result: str = ""
        self.found: bool = False
        self.getData: bool = False
        self.innerText: str = ""

    def handle_data(self, *args):
        if self.getData:
            self.getData = False
            self.innerText = args[0].strip()

    def handle_starttag(self, tag, attrs):
        if self.found:
            return

        if tag.lower() != self.tag:
            return

        loop: bool = False
        for attr, valeur in filter(lambda x: x[0] == self.type_style, attrs):
            loop = True
            valeur_split: list[str] = valeur.split()

            for valeur_style in self.valeurs_style:
                if not valeur_style in valeur_split:
                    return

        if loop:
            self.found = True
            self.getData = True
            self.result = tag, attrs


class PropertyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.url: str = ""
        self.found: bool = False

    def handle_startendtag(self, tag, attrs):
        if self.found or tag != 'meta':
            return

        if attrs[0] == ("property", "og:image") and attrs[1][0] == "content":
            self.url = attrs[1][1]
            self.found = True


class MyHTMLParser(HTMLParser):
    checked_tags: tuple = ("html", "head", "body", "header", "footer", 
        "form", "p", "a", "span", "div", "main", "ul", "li", "ol", "img", 
        "table", "tr", "td")

    def __init__(self, emplacement: str):
        super().__init__()
        self.css_chemin: list = list()
        self.emplacement: str = emplacement
        self.url: str = ""
        self.found: bool = False

    def handle_starttag(self, tag, attrs):
        if self.found:
            return

        if not tag.lower() in self.checked_tags:
            return

        # print(f"<{tag}>", attrs)
        if tag != "img":
            self.css_chemin.append(tag)
            return

        if tag == 'img':
            if self.emplacement != "/".join(self.css_chemin) + f"/{tag}":
                return

            for attr in attrs:
                if attr[0] == 'src':
                    self.url = attr[1]
                    self.found = True
                    # print("/".join(self.css_chemin), end="/")
                    # print(tag)

    def handle_startendtag(self, tag, attrs):
        if self.found:
            return

        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src' and "/covers/full/" in attr[1]:
                    self.url = attr[1]
                    self.found = True

        # print(f"<{tag}/>", attrs)

    def handle_endtag(self, tag):
        if self.found:
            return
        if not tag.lower() in self.checked_tags:
            return
        if not tag in self.css_chemin:
            return

        pop_tag = self.css_chemin.pop()
        # print("pop_tag=", pop_tag)


def get_image_text(session: Session, url: str) -> tuple:

    reponse: Response = session.get(url, timeout=(5, 15), headers=MY_HEADER)

    if not reponse.ok:
        return False, f"{reponse}: {reponse.url}"

    type_page, *encoding = reponse.headers.get("Content-Type").split(";")  # type: ignore[union-attr]

    if not "text/html" in type_page:
        return False, f"type_page problem : {type_page}"

    # html_parser: HTMLTagParser = HTMLTagParser("h5", "class", "card-title m-b-10 m-t-0")
    # html_parser: HTMLTagParser = HTMLTagParser("img", "class", "image")
    # html_parser: HTMLTagParser = HTMLTagParser("p", "class", "level has-text-grey-dark")
    html_parser: HTMLRelativeTagListParser = HTMLRelativeTagListParser( 
        ["main", "article", "header", "h1"])
    html_parser.feed(reponse.text)
    html_parser.close()

    # return html_parser.found, html_parser.result
    return html_parser.found, html_parser.result, html_parser.innerText


def get_image_link(session: Session, url: str) -> tuple[bool, str]:

    reponse: Response = session.get(url, timeout=(4, 10), headers=MY_HEADER)

    if not reponse.ok:
        return False, f"{reponse}: {reponse.url}"

    type_page, *encoding = reponse.headers.get("Content-Type").split(";")  # type: ignore[union-attr]

    if not "text/html" in type_page:
        return False, f"type_page problem : {type_page}"

    # html_parser: MyHTMLParser = MyHTMLParser("html/body/div/div/div/main/div/div/div/div/div/a/img")
    html_parser: PropertyHTMLParser = PropertyHTMLParser()
    html_parser.feed(reponse.text)
    html_parser.close()

    return html_parser.found, html_parser.url


def download_image(session: Session, url: str, filename: str) -> None:
    img_filename: str = url.split("/")[-1]
    *_, extension = img_filename.split(".")
    filename = f"{filename}.{extension}"
    print(" =>", filename, end=" : ", flush=True)
    image = session.get(url)
    
    if not image.ok:
        print("Erreur de telechargement", flush=True)
        return

    type_fichier, extension = image.headers.get("Content-Type").split("/")  # type: ignore[union-attr]
    if type_fichier == "image":
        with open("img\\" + filename, "wb") as fh_img:
            fh_img.write(image.content)
        print("Done", flush=True)
    else:
        print("Not an image", flush=True)


def main() -> None:
    URLs: list[str] = [
        # "https://www.javdatabase.com/movies/jul-125/",
        # "https://www5.javmost.com/STARS-490/",
        # "https://onejav.com/search/JUL-064",
        "https://www4.javhdporn.net/video/jul-064/"
        ]
    session: Session = Session()
    trouvee: bool = False
    image_url: str = ""

    for url in URLs:
        # trouvee, image_url = get_image_link(session, url)
        print(f"get_image_text({url})", flush=True)
        has_text, resultat, text = get_image_text(session, url)
        if has_text:
            print(f"{resultat=}")
            for source in filter(lambda x: x[0] == "class", resultat[1]):
                print(" = ".join(source))

            print(f"{text=}")

        if trouvee:
            print("Download", image_url, flush=True, end="")
            # webbrowser.open(image_url)
            filename: str = url.split("/")[-2].upper()
            # download_image(session, image_url, filename)
            print()
        else:
            print("No Image found:", url, flush=True)


main()

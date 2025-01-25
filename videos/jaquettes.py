import re
import os
import sys
import urllib.request as ur

from requests import Session, codes
from html.parser import HTMLParser


DEBUG: bool = False  # False | True
CODE_OK = codes["OK"]
TYPES_IMAGE: tuple = ("JPG", "JPEG", "PNG", "BMP")
TYPES_VIDEO: tuple = ("MP4", "AVI", "MOV", "MKV", "WMV")
MY_HEADER: dict = {
      # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class MyHTMLParser(HTMLParser):
    emplacement: list[str]
    
    def __init__(self, balise, attribut, chemin, checkattrs: dict = {}):
        super().__init__()
        self.BALISE = balise
        self.ATTRIBUT = attribut
        self.CHEMIN = chemin
        self.emplacement = list()
        self.full_filename = None

    def handle_starttag(self, tag, attrs):
        if not self.full_filename is None:
            return

        if tag == self.BALISE and "/".join(self.CHEMIN) == "/".join(self.emplacement):
            if [attr[0] for attr in attrs if attr[0] == self.ATTRIBUT]:
                if not self.full_filename:
                    self.full_filename = [attr[1] for attr in attrs if attr[0] == self.ATTRIBUT][0]
                    if DEBUG:
                        fprint("Trouve:", self.full_filename)
        self.emplacement.append(tag)

    def handle_startendtag(self, tag, attrs):
        if not self.full_filename is None:
            return

        if tag == self.BALISE and "/".join(self.CHEMIN) == "/".join(self.emplacement):
            if [attr[0] for attr in attrs if attr[0] == self.ATTRIBUT]:
                if not self.full_filename:
                    self.full_filename = [attr[1] for attr in attrs if attr[0] == self.ATTRIBUT][0]

    def handle_endtag(self, tag):
        try:
            while tag != self.emplacement.pop(): 
                pass
        except Exception:
            pass


def string_format(chaine, **kwargs) -> str:
    g = re.search('({.*})', chaine)
    if g:
        nom_variable, *fonction = g.group().strip("{}").split(":")
        if fonction:
            valeur = getattr(kwargs.get(nom_variable), *fonction)()
        else:
            valeur = kwargs.get(nom_variable)
        return chaine.replace(g.group(), valeur)
    else:
        return chaine


def search_url_then_image(img_name) -> str:
    # KV-213 ou KV-217
    URL: str = "https://jav.guru/?s=" + img_name.upper()
    with Session() as s:
        if DEBUG:
            fprint("check:", URL)
        p1 = s.get(URL, timeout=(4, 10), headers=MY_HEADER)
        if p1.status_code != CODE_OK: 
            return ""

        if "text/html" in p1.headers.get("Content-Type", ""):
            html_parser = MyHTMLParser("a", "href", ["html", "body", "div", "div", "div", "main", "div", "div", "div", "div"])
            html_parser.feed(p1.text)
            if html_parser.full_filename is None: 
                return ""

            URL = html_parser.full_filename
            p2 = s.get(URL, timeout=(4, 10), headers=MY_HEADER)
            if p2.status_code != CODE_OK or "text/html" not in p1.headers.get("Content-Type", ""):
                return ""

            html_parser = MyHTMLParser(
                "img", "src", ["html", "body", "div", "div", "div", "main", "article", "div", "div", "div", "div", "div"])
            html_parser.feed(p2.text)
            return html_parser.full_filename

    return ""


def get_image_from_path(p_img_name) -> str:

    sites: list = [
        ("https://javgg.net/jav/{img_name:lower}/", 
            ["html", "body", "div", "div", "div", "div", "div", "a", "div"],
            "src"),
        ("https://maxjav.com/?s={img_name:upper}", 
            ["html", "body", "div", "div", "div", "div", "p"],
            "src"),
        ("https://www.javpornstreaming.com/japanese_videos/{img_name:lower}",  # SDDE-110
            ["html", "body", "div", "div", "div", "div"],
            "src"),
        ("https://watchjavonline.com/{img_name:lower}",   # SDDE-206
            ["html", "body", "div", "div", "div", "div", "div", "div", "article", "div", "div", "div", "div"],
            "src"),
        ("https://bejav.tv/{img_name:lower}/",  # LAF-39
            ["html", "body", "div", "section", "div", "div", "div", "div", "div", "div", "picture", "source"],
            "data-src"),
    ]

    while sites:
        if not DEBUG:
            fprint(".", end="")
        source, chemin, attr = sites.pop(0)
        with Session() as s:
            URL = string_format(source, img_name=p_img_name)
            # print(URL, chemin)
            if DEBUG:
                fprint("check:", URL)
            try:
                p1 = s.get(URL, timeout=(4, 10), headers=MY_HEADER)
            except Exception as e:
                continue
                fprint(e)
            
            if p1.status_code != CODE_OK: 
                continue

            if "text/html" in p1.headers.get("Content-Type", ""):
                html_parser = MyHTMLParser("img", attr, chemin )
                html_parser.feed(p1.text)
                if html_parser.full_filename:
                    # print("found", html_parser.full_filename)
                    return html_parser.full_filename

    return ""


def get_image_from_meta_property(p_img_name) -> str:

    sites: list[str] = [
        "https://www2.javhdporn.net/video/{img_name}/",
        "https://3xplanet.net/{img_name}/",
        "https://yavtube.com/movie/{img_name:upper}",
        "https://sextb.net/{img_name}"
        ]
    found = False

    while sites and not found:
        if not DEBUG:
            fprint(".", end="")
        URL: str = string_format(sites.pop(0), img_name=p_img_name)
        with Session() as s:
            if DEBUG:
                fprint("check:", URL)
            p1 = s.get(URL, timeout=(4, 10), headers=MY_HEADER)
            if p1.status_code != CODE_OK: 
                continue

            charset = p1.encoding
            meta_property_trouve = False
            if "text/html" in p1.headers.get("Content-Type"):
                for bligne in p1.iter_lines():
                    ligne = bligne.decode(charset).strip()

                    if '<meta property' in ligne:
                        meta_property_trouve = True
                    elif meta_property_trouve:
                        continue

                    if meta_property_trouve and '"og:image"' in ligne:
                        try:
                            codes, lien = ligne.split("content=")
                            _, site, *_ = lien.split('"')
                        except Exception:
                            continue
                        return site

    return ""


def download_image(directory: str, img_name: str):
    fprint("Downloading", img_name, end=" ")
    if DEBUG: print()

    downloaded = False
    site_added = 0  # 0
    sites = [
        "https://img2.javmost.com/file_image/", 
        "https://nonecss.com/file_image/",
        ]
    sites = [(site + img_name) for site in sites]

    basename: str = img_name.split(".")[0]
    sites += [string_format("https://fivetiu.com/{basename:lower}/cover-n.jpg", basename=basename)]

    while not downloaded and sites:
        url = sites.pop(0)

        try:
            if DEBUG:
                fprint("check:", url)
            req = ur.Request(url, headers=MY_HEADER)
            page = ur.urlopen(req, timeout=10)
            
            type_fichier, extension = page.getheader("Content-Type").split("/")
            if type_fichier == "image":
                with open(directory + "\\" + img_name, "wb") as fh_img:
                    fh_img.write(page.read())
                fprint(" Done", end="")
                downloaded = True
            else:
                print("x", end="")

        except ur.HTTPError as httperror:
            if not DEBUG:
                fprint(".", end="")

        except Exception as e:
            fprint("Erreur:", e)

        if not downloaded:
            if site_added >= 3:
                fprint(" Not found", end="")
            else:
                if not DEBUG:
                    fprint(".", end="")
                if not sites and site_added == 0:
                    site_added += 1
                    if not DEBUG:
                        fprint(" Checking", end=" ")
                    another_site = get_image_from_meta_property(img_name.split(".")[0].lower())
                    if another_site:
                        sites.append(another_site)

                if not sites and site_added == 1:
                    site_added += 1
                    if not DEBUG:
                        fprint(" .", end="")
                    another_site = get_image_from_path(img_name.split(".")[0])
                    if another_site:
                        sites.append(another_site)

                if not sites and site_added == 2:
                    site_added += 1
                    if not DEBUG:
                        fprint(" .", end="")
                    another_site = search_url_then_image(img_name.split(".")[0])
                    if another_site:
                        sites.append(another_site)
                    else:
                        fprint(" Not found", end="")

    print()


def download_jaquettes(directory: str) -> None:
    print()
    fprint("Scanning: ", directory)
    liste = os.scandir(directory)
    fichiers: dict = {}

    for item in liste:
        if item.is_file():
            position_point = item.name.rindex(".")
            extension = item.name[1+position_point:].upper()
            fichier = item.name[:position_point].upper()
            cle_fichier = fichier.split()[0].strip("[]")

            if "-" in cle_fichier and extension in TYPES_IMAGE + TYPES_VIDEO:
                part_un, part_deux, *_ = cle_fichier.split("-")
                if part_deux.isnumeric():
                    cle = f"{part_un}-{part_deux}"
                    if fichiers.get(cle, None) is None:
                        fichiers[cle] = {}
                    if extension in TYPES_IMAGE:
                        fichiers[cle]["IMAGE"] = (item.name, extension, item.stat().st_size)
                    elif extension in TYPES_VIDEO:
                        fichiers[cle]["VIDEO"] = (item.name, extension, item.stat().st_size)

    ok, total, image, video = (0,)*4
    for file, detail in sorted(fichiers.items()):
        image += 1 if detail.get("IMAGE") else 0
        video += 1 if detail.get("VIDEO") else 0
        if detail.get("IMAGE") and detail.get("VIDEO"):
            ok += 1
        total += 1

    fprint("", total - image, "fichiers sans image")
    fprint("", total - video, "fichiers sans video")
    fprint("", ok, "fichiers avec image et video")
    fprint("", total, "fichiers au total")

    print()
    index: int = 0
    nb_files: int = len(list(filter(lambda x: x[1].get("IMAGE", None) is None, list(fichiers.items()))))
    # print(f"{nb_files=}")
    size: int = len(str(nb_files))
    for file, detail in sorted(fichiers.items()):
        # print(detail.get("IMAGE"))
        if not detail.get("IMAGE"):
            index += 1
            print(f"{index:0{size}} / {nb_files}", end= " ")
            download_image(directory, f"{file}.jpg")


if sys.argv[1:]:
    directory = os.path.abspath(" ".join(sys.argv[1:]))
    download_jaquettes(directory)

else:
    download_jaquettes(".")

import re
import os
import sys
import urllib.request as ur

from requests import Session, codes
from html.parser import HTMLParser

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

Directories = [
    r"E:\Videos\Japan\Eimi Fukada",
    r"E:\Videos\Japan\Hinata Marin", 
    r"D:\Mes Documents\dwhelper\Japan",
    r"D:\Mes Documents\dwhelper",
    r"E:\Videos\Japan\Yui Hatano",
    r"E:\Videos\Japan\SDDE",
    r"E:\Videos\Japan",
    ]

KS_DIRECTORY = Directories[6]


class MyHTMLParser(HTMLParser):
    def __init__(self, balise, attribut, chemin, checkattrs: dict = {}):
        super().__init__()
        self.BALISE = balise
        self.ATTRIBUT = attribut
        self.CHEMIN = chemin
        self.emplacement = []
        self.full_filename = None

    def handle_starttag(self, tag, attrs):
        if tag == self.BALISE and "/".join(self.CHEMIN) == "/".join(self.emplacement):
            if [attr[0] for attr in attrs if attr[0] == self.ATTRIBUT]:
                if not self.full_filename:
                    self.full_filename = [attr[1] for attr in attrs if attr[0] == self.ATTRIBUT][0]
        self.emplacement.append(tag)

    def handle_startendtag(self, tag, attrs):
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
        ("https://maxjav.com/?s={img_name:upper}", 
            ["html", "body", "div", "div", "div", "div", "p"]),
        ("https://www.javpornstreaming.com/japanese_videos/{img_name:lower}",  # SDDE-110
            ["html", "body", "div", "div", "div", "div"]),
        ("https://watchjavonline.com/{img_name:lower}",   # SDDE-206
            ["html", "body", "div", "div", "div", "div", "div", "div", "article", "div", "div", "div", "div"])
    ]

    while sites:
        print(".", end="", flush=True)
        source, chemin = sites.pop(0)
        # print(source, chemin)
        with Session() as s:
            URL = string_format(source, img_name=p_img_name)
            try:
                p1 = s.get(URL, timeout=(4, 10), headers=MY_HEADER)
            except Exception as e:
                continue
                print(e)
            
            if p1.status_code != CODE_OK: 
                continue

            if "text/html" in p1.headers.get("Content-Type", ""):
                html_parser = MyHTMLParser("img", "src", chemin)
                html_parser.feed(p1.text)
                if html_parser.full_filename:
                    return html_parser.full_filename

    return ""


def get_image_from_meta_property(p_img_name) -> str:
    sites: list[str] = [
        "https://www2.javhdporn.net/video/{img_name}/",
        "https://3xplanet.net/{img_name}/",
        "https://yavtube.com/movie/{img_name:upper}"
        ]
    found = False

    while sites and not found:
        print(".", end="", flush=True)
        URL: str = string_format(sites.pop(0), img_name=p_img_name)
        with Session() as s:
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
    print("Downloading", img_name, end=" ", flush=True)
    downloaded = False
    site_added = 0
    sites = [
        "https://img2.javmost.com/file_image/", 
        "https://nonecss.com/file_image/",
        ]
    sites = [(site + img_name) for site in sites]

    while not downloaded and sites:
        url = sites.pop(0)
        req = ur.Request(url, headers=MY_HEADER)
        try:
            page = ur.urlopen(req, timeout=10)
            
            type_fichier, extension = page.getheader("Content-Type").split("/")
            if type_fichier != "image":
                return

            with open(directory + "\\" + img_name, "wb") as fh_img:
                fh_img.write(page.read())
            print(" Done", end="")
            downloaded = True

        except ur.HTTPError:
            if site_added >= 3:
                print(" Not found", end="")
            else:
                print(".", end="")
                if not sites and site_added == 0:
                    site_added += 1
                    print(" Checking", end=" ")
                    another_site = get_image_from_meta_property(img_name.split(".")[0].lower())
                    if another_site:
                        sites.append(another_site)

                if not sites and site_added == 1:
                    site_added += 1
                    print(" .", end="")
                    another_site = get_image_from_path(img_name.split(".")[0])
                    if another_site:
                        sites.append(another_site)

                if not sites and site_added == 2:
                    site_added += 1
                    print(" .", end="")
                    another_site = search_url_then_image(img_name.split(".")[0])
                    if another_site:
                        sites.append(another_site)
                    else:
                        print(" Not found", end="")

            # for ligne in str(e.fp.read()).split("<p>")[1:]:
            #     print(ligne.split("</p>")[0])
        except Exception as e:
            print(e)

    print()


def download_jaquettes(directory: str) -> None:
    print()
    print("Scanning: ", directory)
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

    print("", total - image, "fichiers sans image")
    print("", total - video, "fichiers sans video")
    print("", ok, "fichiers avec image et video")
    print("", total, "fichiers au total")

    print()
    for file, detail in sorted(fichiers.items()):
        if not detail.get("IMAGE"):
            download_image(directory, f"{file}.jpg")


if sys.argv[1:]:
    directory = os.path.abspath(" ".join(sys.argv[1:]))
    download_jaquettes(directory)

else:
    download_jaquettes(".")

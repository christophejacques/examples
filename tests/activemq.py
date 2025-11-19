import json
import base64
import requests.utils as requti
import datetime
import time

from datetime import datetime as dt
from requests import Session, Response, codes
from html.parser import HTMLParser
from typing import Tuple, Optional


print("DEBUT", flush=True)
heure_debut = time.perf_counter()

DEBUG = False
MY_HEADER: dict = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
      'Connection': 'keep-alive',
      }

DOCUMENT: dict = {
      "idDemandeAide": "CHRIS0026",
      "codeEnvoi": 2,
      "horodatageSIGestion": "2025-11-15T08:24:01.325741+0100",
      "codePartenaire": "CVL",
      "listeDossiers": {
        "idDossiersPartenaire": ["CJA0002"]
      }
    }


def to_string(texte) -> str:
    if isinstance(texte, dict):
        return json.dumps(texte)

    return str(texte).replace("'", '"')


def maintenant() -> str:
    tz = datetime.timezone(datetime.timedelta(hours=1))
    return dt.isoformat(dt.now(tz))


def urlquote(texte: str) -> str:
    return requti.quote(texte)  # type: ignore[attr-defined]


def urlunquote(texte: str) -> str:
    return requti.unquote(texte)  # type: ignore[attr-defined]


def decode_text(texte: str) -> str:
    try:
        variable = json.loads(texte.replace("'", '"'))
    except json.JSONDecodeError:
        variable = texte
    except TypeError:
        variable = str(texte)

    return variable


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
        self.session: Optional[Session] = None

        self.level: int = 0
        self.path: str = ""
        self.result: list = list()
        self.liste_recherche = list()
        self.datas: list = list()
        self.classes: list = list()
        self.ident: list = list()
        self.has_data: bool = False

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
                self.found = self.attributs_match_path()

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
        if self.session is None:
            self.session = Session()

        dprint("Load:", url)

        try:
            reponse: Response = self.session.get(url, timeout=(2, 5), headers=MY_HEADER)

        except Exception as erreur:
            return False, f"{erreur}"

        if not reponse.ok:
            return False, f"{reponse}: {reponse.url}"

        type_page, *encoding = reponse.headers.get("Content-Type").split(";")  # type: ignore[union-attr]

        if not "text/html" in type_page:
            return False, f"type_page problem : {type_page}"

        return self.load_str(reponse.text)

    def post_data(self, url: str, secret: str, pdata: list) -> Tuple[bool, str]:

        # ActiveMQ default keys 
        # -----------------------
        # "secret={secret}"
        # "JMSDestination={nom_queue}"
        # "JMSDestinationType=queue"
        # "JMSPersistent=true"
        # "JMSCorrelationID="
        # "JMSReplyTo="
        # "JMSPriority="
        # "JMSType="
        # "JMSTimeToLive="
        # "JMSXGroupID="
        # "JMSXGroupSeq="
        # "AMQ_SCHEDULED_DELAY="
        # "AMQ_SCHEDULED_PERIOD="
        # "AMQ_SCHEDULED_REPEAT="
        # "AMQ_SCHEDULED_CRON="
        # "JMSMessageCount=1"
        # "JMSMessageCountHeader=JMSXMessageCounter"
        # "JMSText="

        if self.session is None:
            self.session = Session()

        print("Post:", url)

        referer = url[:url.index("/", 10)] + "/admin/send.jsp"

        headers = MY_HEADER.copy()
        headers.update({
            "Content-Type": "application/x-www-form-urlencoded", 
            "Upgrade-Insecure-Requests": "1",
            "Priority": "u=0, i",
            "Referer": referer
        })

        # Transformation des donnees afin d'etre compatible avec le format "urlencoded"
        data = "&".join([f"{key}={urlquote(to_string(value))}" for key, value in pdata])

        try:
            response = self.session.post(url, data=data, headers=headers)

        except Exception as erreur:
            return False, f"{erreur}"

        if not response.ok:
            return False, f"{response}: {response.url}"

        return True, "Posted"


    def init_find(self, recherche: str):
        self.found = False
        self.classes = list()
        self.ident = list()

        for selector in recherche.split():
            self.classes.append(selector.split(".")[1:])
        dprint("classes:", self.classes)
        self.recherche = " ".join([t.split(".")[0] for t in recherche.split()])

        for selector in self.recherche.split():
            self.ident.append(selector.split("#")[1:])
        dprint("ident:", self.ident)
        self.recherche = " ".join([t.split("#")[0] for t in self.recherche.split()])

        dprint("recherche:", recherche)
        dprint()

    def find(self, recherche: str, tout: bool=False, exact: bool=False):
        # Parametres :
        # 
        # @recherche : chemin au format css
        # "." indique de filtrer sur la classe de l'element
        # "#" indique de filtrer sur l'identifiant l'element
        # 
        # @tout : ne s'arrete pas apres avoir trouve une occurrence
        #    mais les recherches toutes jusqu'a la fin de la page
        # 
        # @exact : ne recherche que les correspondances exactes
        #    au format css recherche (sans rechercher ses fils)
        # 
        self.path = ""
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

    def test_nb_results(self, nombre: int) -> bool:
        nb_result: int = len(self.result)
        if nb_result == nombre:
            return True

        print(f"Le nombre de résultats '{nb_result}' ne correspond pas à l'attendu '{nombre}'.")
        return False

    def print(self): 
        print()
        for res in self.get_result():
            print(res)
        print("\nend level:", parser.level)


if __name__ == "__main__":

    scheme: str = "http"
    user: str = "admin"
    passwd: str = "admin"

    host: str = "172.27.207.196"
    port: str = "8161"

    browse_path: str = "/admin/browse.jsp"
    message_path: str = "/admin/message.jsp"
    send_path: str = "/admin/send.jsp"

    queue: str = "ActiveMQ.queue.cja"

    auth: str = f"{user}:{passwd}"
    adresse: str = f"{host}:{port}"

    secret_css_selector: str = "form input"
    browse_css_selector: str = "table#messages tbody tr td a"
    msg_css_selector: str = "table tbody tr td div.message pre.prettyprint"
    header_css_selector: str = "td.layout table#header tbody"
    properties_css_selector: str = "td.layout table#properties tbody"

    credentials: str = base64.b64encode(auth.encode('latin-1')).decode('latin-1')
    MY_HEADER.update({
        "Authorization": f"Basic {credentials}"        
    })

    parser = MyHTMLParser()

    # mettre à True pour Ajouter un nouveau document
    if False:
        # load Send html page
        url: str = f"{scheme}://{adresse}{send_path}"

        # Récupération du secret afin de pouvoir utiliser l'action POST avec
        ok, result = parser.load_url(url)
        if not ok:
            print(result)
            exit()

        parser.find(secret_css_selector)
        ok = parser.test_nb_results(1)
        if not ok:
            exit()

        for resultat in parser.result:
            for attribut in resultat["attrs"]:
                key, value = attribut
                if key == "value":
                    secret = value


        # Create new Document
        payload: dict = DOCUMENT

        data: list = [
            ("secret", secret),
            ("JMSDestination", queue),
            ("JMSDestinationType", "queue"),
            ("JMSPersistent", "true"),
            ("JMSMessageCount", 1),
            ("JMSMessageCountHeader", "JMSXMessageCounter"),
            ("JMSText", payload),
        ]
        properties: list = [
            ("codeEnvoi", payload.get("codeEnvoi", 0)),
            ("routeId", "PERF3"),
            ("key", "START"),
            ("idDemandeAide", payload.get("idDemandeAide", "")),
            ("horodatageSIGestion", payload.get("horodatageSIGestion", "")),
            ("horodatageSynapse", maintenant()),
        ]
        data += properties

        url = f"{scheme}://{adresse}/admin/sendMessage.action"
        ok, result = parser.post_data(url, secret, data)
        if not ok:
            print(result)
            exit()

        print("OK", result)
        print()


    # GET activeMQ liste des messages
    url = f"{scheme}://{adresse}{browse_path}?JMSDestination={queue}"

    ok, result = parser.load_url(url)
    if not ok:
        print(result)
        exit()

    parser.findall(browse_css_selector)
    messages: list = list(
        filter(lambda r: r["attrs"][0][1].startswith("message.jsp"), 
            parser.result))

    # calcul du nb de documents (messages / 2)
    print(len(messages), "message(s) trouvé(s).\n")

    headers: set = set()
    csv_messages: list = list()
    un_message: dict

    # GET all activeMQ documents
    for parsed_html in messages[:]:
        # Recuperation d'un idMessage

        un_message = dict()

        # filtre sur l'attribut href
        for attrs in parsed_html["attrs"]:
            if attrs[0] == "href":
                href = attrs[1]
                break

        # filtre sur les parametres du href
        for extract_params in href.split("?"):
            if extract_params[0] == "href":
                break

        # filtre sur le parametre "id="
        for un_param in extract_params.split("&"):
            if un_param.startswith("id="):
                break

        # filtre sur la valeur du parametre 
        for valeur_param in un_param.split("="):
            if valeur_param != "id":
                id_message = valeur_param
                break

        dprint("idMessage =", urlunquote(id_message))

        # Recuperation des informations de l'idMessage trouve
        parametres : list = [
            f"JMSDestination={queue}",
            f"id={id_message}"
        ]

        params = "&".join(parametres)
        url = f"{scheme}://{adresse}{message_path}?{params}"

        ok, result = parser.load_url(url)
        if not ok:
            print(result)
            exit()


        # Recherche des proprietes
        if True:
            parser.find(header_css_selector)

            dprint("Headers :")
            label = False
            key = ""

            for ligne in parser.result:
                if label:
                    label = False
                    dprint(f"  {key:20}= {ligne["text"]}")
                    clef = f"headers.{key}"
                    headers.add(clef)
                    un_message[clef] = f"{ligne["text"]}"

                elif ligne["path"].endswith("tr td"):
                    for k, v in ligne["attrs"]:
                        if k == "class" and v == "label":
                            key = ligne["text"]
                            label = True
                            break


        # Recherche des proprietes
        if True:
            parser.find(properties_css_selector)

            dprint("Properties :")
            label = False
            key = ""
            for ligne in parser.result:
                if label:
                    label = False
                    dprint(f"  {key:20}= {ligne["text"]}")
                    clef = f"properties.{key}"
                    headers.add(clef)
                    un_message[clef] = f"{ligne["text"]}"

                elif ligne["path"].endswith("tr td"):
                    for k, v in ligne["attrs"]:
                        if k == "class" and v == "label":
                            key = ligne["text"]
                            label = True
                            break

        if True:
            # Recherche du payload
            parser.find(msg_css_selector)
            for ligne in parser.result:
                variable = decode_text(ligne["text"])
                dprint("payload:\n ", variable)
                un_message["payload"] = f"{ligne["text"]}"

        csv_messages.append(un_message)
        dprint()

    parser.close()


    # Creation d'un fichier au format CSV 
    with open("activemq.csv", "w") as csvhandle:
        # entete de colonnes
        csv_msg = ""
        for header in sorted(headers):
            csv_msg += header + ";"

        csv_msg += "payload\n"
        csvhandle.write(csv_msg)

        # contenu des lignes
        for un_message in csv_messages:
            csv_msg = ""
            for header in sorted(headers):
                csv_msg += un_message.get(header, "") + ";"

            csv_msg += un_message.get("payload", "") 
            csvhandle.write(csv_msg + "\n")
            print(csv_msg)


print(f"FIN. durée = {time.perf_counter() - heure_debut:.2f}s")

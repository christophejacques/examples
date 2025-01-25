DEBUG: bool = False
DETAILS: bool = False


class Erreur:
    level: int = 0
    libelle: str = ""

    def __init__(self, level=None, libelle: str = ""):
        self.level = level
        self.libelle = libelle

    def __add__(self, other):
        if self.level is None:
            self.level = other.level
        else:
            self.level += 0 if other.level is None else other.level

        self.libelle = other.libelle
        return self

    def __radd__(self, other):
        return self + other

    def init(self) -> None:
        self.level = 0
        self.libelle = ""

    def is_none(self) -> bool:
        return self.level is None

    def is_ok(self) -> bool:
        if self.level is None:
            return False
        return self.level == 0

    def is_ko(self) -> bool:
        if self.level is None:
            return False
        return self.level != 0

    def __str__(self) -> str:
        match self.level:
            case None:
                return "None"
            case 0:
                return "0"
        return f"{self.level} - {self.libelle}"


class Commande_result:

    def __init__(self, error_level=None) -> None:
        self.content: list = []
        self.filename: str = ""
        self.erreur: Erreur = Erreur(level=error_level)

    def __add__(self, other):
        cr = Commande_result()
        cr.content = self.content + other.content
        cr.erreur = self.erreur + other.erreur
        # print("code erreur =", cr.erreur)
        return cr

    def __radd__(self, other):
        cr = Commande_result()
        cr.content = self.content + other.content
        cr.erreur = self.erreur + other.erreur
        # print("code erreur += ", cr.erreur)
        return cr

    def est_non_vide(self):
        return len(self.content) > 0

    def to_file(self, filename: str) -> Erreur:
        if DEBUG:
            print("set sortie_standard:", filename)

        try:
            with open(filename): 
                pass
        except Exception as except_error:
            self.erreur = Erreur(
                getattr(except_error, "errno"), 
                f"{getattr(except_error, 'strerror')} : {getattr(except_error, 'filename')}")
        finally:
            self.filename = filename

        return self.erreur

    def from_file(self, filename: str) -> Erreur:
        self.erreur.init()
        if DEBUG:
            print("get entree_standard:", filename)
        if self.filename:
            return self.erreur

        try:
            with open(filename, 'r') as f:
                result = f.readlines()
                for ligne in result:
                    self.print(ligne.strip("\n"))

        except Exception as except_error:
            self.erreur = Erreur(
                getattr(except_error, "errno"), 
                f"{getattr(except_error, 'strerror')} : {getattr(except_error, 'filename')}")

        return self.erreur

    def copy(self):
        content: Commande_result = Commande_result()
        content.content = self.content.copy()
        content.erreur = self.erreur
        return content

    def print(self, ligne: str | list[str]) -> None:
        if isinstance(ligne, str):
            self.content.append(ligne)
            if DEBUG:
                print("print ->", ligne)
        elif isinstance(ligne, list):
            self.content.extend(ligne)
            if DEBUG:
                for une_ligne in ligne:
                    print("print ->", une_ligne)

        else:
            msg = f"le champ ligne est de type {ligne.__class__.__name__}"
            msg += " au lieu de str ou list."
            raise TypeError(msg)

    def to_screen(self):
        for ligne in self.content:
            print(ligne)

        if self.erreur.is_ko():
            print(self.erreur.libelle)


class Commande:

    def __init__(self, commande: str = ""):
        self.params: str = ""
        self.stdin: Commande_result = Commande_result()
        self.stdout: Commande_result = Commande_result()
        if commande:
            self.split_cmd(commande)

    def split_cmd(self, commande: str) -> None:
        # print("split:", commande)
        if len(commande.strip()) > 0:
            cmde, *parms = commande.split()
            params = " ".join(parms)
        else:
            cmde = ""
            parms = []
            params = ""

        self.set_cmd(cmde)
        if parms:
            self.set_params("".join(params))

    def set_cmd(self, commande: str) -> None:
        self.commande: str = commande

    def set_params(self, params: str) -> None:
        self.params = params

    def set_stdin(self, stdin: Commande_result) -> None:
        self.stdin = stdin.copy()

    def print(self, ligne: str) -> None:
        self.stdout.print(ligne)

    def run(self) -> Commande_result:
        if DEBUG:
            print(f"Run: {self.commande}, params: {self.params}, stdin: {len(self.stdin.content)} lines")

        self.stdout.erreur.init()
        match self.commande.lower():
            case "":
                # suite a une commande entre parentheses
                self.stdout = self.stdin.copy()
                if DETAILS:
                    for ligne in self.stdout.content:
                        print("->", ligne)

            case "cat":
                if self.stdin.content:
                    if not self.stdout.filename:
                        self.stdout = self.stdin.copy()
                else:
                    for fichier in filter(lambda x: not x.startswith("-"), self.params.split()):
                        self.stdout.erreur = self.stdout.from_file(fichier)
                        if not self.stdout.erreur.is_ok():
                            break

            case "grep":
                # print("stdin:", self.stdin.content)
                filtre = " ".join(filter(lambda x: not x.startswith("-"), self.params.split()))
                liste: list = list(filter(lambda x: x.count(filtre) > 0, self.stdin.content))
                self.stdout.print(liste)

            case "wc":
                if "-l" in self.params:
                    self.stdout.print(str(len(self.stdin.content)))

            case "echo":
                self.stdout.print(self.params)

            case "cut":
                if len(self.params.split()) == 0:
                    self.stdout.erreur = Erreur(1, "La commande 'cut' necessite au moins un parametre.")
                    
                elif self.params[:2] not in ("-c", "-f"):
                    self.stdout.erreur = Erreur(1, "La commande 'cut' n'accepte que les parametres -c ou -f.")
                    
                elif len(self.params.split()) > 2:
                    self.stdout.erreur = Erreur(1, "La commande 'cut' ne peut avoir plus de 2 parametres.")
                    
                else:
                    if self.params[:2] == "-c":
                        sep: str
                        sdebut: str
                        sfin: str

                        params: str = self.params[2:].strip()
                        sdebut, sep, sfin = params.partition("-")
                        debut: int = 0 if sdebut == "" else eval(sdebut)-1
                        fin: int = (0 if sfin == "" else eval(sfin)) 

                        if sep == "":
                            for ligne in self.stdin.content:
                                self.stdout.print(ligne[debut])
                        elif sfin == "":
                            for ligne in self.stdin.content:
                                self.stdout.print(ligne[debut:])
                        else:
                            for ligne in self.stdin.content:
                                self.stdout.print(ligne[debut:fin])
                    else:
                        # param -f x
                        param: str = self.params[2:].strip()
                        if not param.isnumeric():
                            self.stdout.erreur = Erreur(1, f"Le parametre '{param}' de la commande 'cut' doit etre numerique.")
                        else:
                            index: int = eval(param)
                            for ligne in self.stdin.content:
                                resultat: list = ligne.split()
                                if index <= len(resultat):
                                    self.stdout.print(resultat[index-1])
                                else:
                                    self.stdout.print("")

            case other:
                self.stdout.erreur = Erreur(1, f"Commande '{other}' non trouvee.")

        if DEBUG:
            print(f"Run.Erreur: {self.stdout.erreur}, stdout: {len(self.stdout.content)} lines")
            print()

        return self.stdout
        

class CommandLine:
    commandes: str

    def __init__(self, ligne: str) -> None:
        self.commandes = ligne

    def commande_runnable(self, prev_sep: str, prev_result: Commande_result) -> bool:
        res: bool = False

        if prev_result.erreur.is_none():
            res = True
        elif prev_sep == "&&" and prev_result.erreur.is_ok():
            res = True
        elif prev_sep == "||" and prev_result.erreur.is_ko():
            res = True
        elif prev_sep in ["|", ""]:
            res = True

        return res

    def partition_commande(self, commande: str) -> Commande:
        # print("partition:", commande)
        cmd: Commande = Commande()

        if ">" in commande:
            cmd_params, sep, sortie_standard = commande.partition(">")
            if cmd_params[-1] == "2":
                print("envoie de l'erreur standard")
            else:
                cmd.stdout.to_file(sortie_standard.strip())
                if not cmd.stdout.erreur.is_ok():
                    print("erreur envoie file")
            commande = cmd_params

        if "<" in commande:
            cmd_params, sep, entree_standard = commande.partition("<")
            cmd.stdin.from_file(entree_standard.strip())
            if not cmd.stdin.erreur.is_ok():
                print("erreur recup file")        
            commande = cmd_params

        cmd.split_cmd(commande)
        return cmd

    def parse_commandes(self, commandes: str) -> Commande_result:
        resultat: Commande_result = Commande_result()
        prev_result: Commande_result = Commande_result()
        prev_sep: str = ""

        commandes = commandes.strip()
        if DEBUG:
            print("Parse:", commandes)

        index: int = 0
        longueur: int = len(commandes)
        caracteres: list[str] = []

        while index < longueur:
            caracteres.clear()
            caracteres.append(commandes[index])
            if index+1 < longueur:
                caracteres.append(commandes[index+1])

            match caracteres:
                case ["(", _]:
                    nb_parentheses = 1
                    index2 = index
                    while index2 < longueur:
                        index2 += 1
                        match commandes[index2]:
                            case "(":
                                nb_parentheses += 1
                            case ")":
                                nb_parentheses -= 1
                                if nb_parentheses <= 0:
                                    break

                    if self.commande_runnable(prev_sep, prev_result):
                        sub_cmd: str = commandes[1+index:index2].strip()
                        if DETAILS:
                            print("sub_cmd:", sub_cmd)
                        prev_result = self.parse_commandes(sub_cmd)
                        if DETAILS:
                            print(f"sub_cmd: '{sub_cmd}' done, stdout: {len(prev_result.content)} lines")

                    commandes = commandes[1+index2:].strip()
                    if DETAILS:
                        print(f"reste cmds: {commandes}")
                    index = -1
                    longueur = len(commandes)

                case ["&", nextchar]:
                    if self.commande_runnable(prev_sep, prev_result):
                        next_cmd: str = commandes[:index].strip()
                        if DETAILS:
                            print(f"{prev_sep} cmd runnable: *{next_cmd}*")

                        commande = self.partition_commande(next_cmd)
                        if next_cmd == "":
                            if DETAILS:
                                print(f"recup stdout > stdin: {len(prev_result.content)} lines")
                            commande.stdin = prev_result.copy()
                        prev_result = commande.run()
                    else:
                        if DETAILS:
                            print("Skip cmd:", commandes[:index])
                        prev_result = Commande_result(prev_result.erreur.level)

                    if nextchar != "&":
                        prev_sep = "&"
                    else:
                        prev_sep = "&&"
                        resultat += prev_result

                        commandes = commandes[2+index:].strip()
                        index = -1
                        longueur = len(commandes)

                case ["|", nextchar]:
                    if self.commande_runnable(prev_sep, prev_result):
                        next_cmd = commandes[:index].strip()
                        if DETAILS:
                            print(f"{prev_sep} cmd runnable: *{next_cmd}*")
                        commande = self.partition_commande(next_cmd)
                        if next_cmd == "" or prev_sep == "|":
                            if DETAILS:
                                print(f"recup stdout > stdin: {len(prev_result.content)} lines")
                            commande.stdin = prev_result.copy()
                        prev_result = commande.run()
                    else:
                        if DETAILS:
                            print("Skip cmd:", commandes[:index])
                        prev_result = Commande_result(prev_result.erreur.level)

                    if nextchar == "|":
                        prev_sep = "||"
                        resultat += prev_result
                        commandes = commandes[2+index:].strip()
                    else:
                        prev_sep = "|"
                        commandes = commandes[1+index:].strip()

                    index = -1
                    longueur = len(commandes)

            index += 1

        # print(f"> '{prev_sep}' &", prev_result.erreur.level, "=", self.commande_runnable(prev_sep, prev_result))
        # print("rez:", resultat.content)
        if self.commande_runnable(prev_sep, prev_result):
            next_cmd = commandes[:index].strip()
            if DETAILS:
                print(f"{prev_sep} cmd runnable: *{next_cmd}*")
            commande = self.partition_commande(next_cmd)

            if prev_sep == "|":
                commande.stdin = prev_result.copy()
                prev_result = commande.run()
            else:
                if prev_sep == "":
                    commande.stdin = prev_result.copy()
                prev_result = commande.run()

            resultat += prev_result

        return resultat

    def run(self) -> Commande_result:
        print(f"[user:~] $ {self.commandes}")
        resultat: Commande_result = self.parse_commandes(self.commandes)

        return resultat


for index in range(1, 8):
    match index:
        case 1:
            CommandLine("cat < api_siret.py | grep -i import | wc -l ").run().to_screen()
        case 2:
            CommandLine("cat -o -i api_siret.py test.py | grep import").run().to_screen()
        case 3:
            CommandLine("(echo Hello World || echo End this)").run().to_screen()
        case 4:
            CommandLine("echo ligne | wc -l 2> /dev/null && echo Fini").run().to_screen()
        case 5:
            CommandLine("Echo un deux && ((Echo trois quatre | grep trois) | grep quatre) && echo cinq six").run().to_screen()
        case 6:
            CommandLine("echo a 1 && echo b 2 || echo c 3 && echo d 4 && echo e 5 | cut -f1").run().to_screen()
        case 7:
            CommandLine("echo Les chaussettes de l'archiduchesse | cut -f 2").run().to_screen()
    print()

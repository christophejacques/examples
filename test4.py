DEBUG: bool = False


class Commande_result:

    def __init__(self) -> None:
        self.content: list = []
        self.filename: str = ""

    def est_non_vide(self):
        return len(self.content) > 0

    def to_file(self, filename: str) -> None:
        if DEBUG:
            print("set sortie_standard:", filename)
        self.filename = filename

    def from_file(self, filename: str) -> None:
        if DEBUG:
            print("get entree_standard:", filename)
        if self.filename:
            return

        with open(filename, 'r') as f:
            result = f.readlines()
            for ligne in result:
                self.print(ligne.strip("\n"))

    def copy(self):
        content: Commande_result = Commande_result()
        content.content = self.content.copy()
        return content

    def print(self, ligne: str | list) -> None:
        if isinstance(ligne, str):
            self.content.append(ligne)
        elif isinstance(ligne, list):
            self.content.extend(ligne)
        else:
            msg = f"le champ ligne est de type {ligne.__class__.__name__}"
            msg += " au lieu de str ou list."
            raise TypeError(msg)

    def to_screen(self):
        for ligne in self.content:
            print(ligne)


class Commande:

    def __init__(self):
        self.params: str = ""
        self.stdin: Commande_result = Commande_result()
        self.stdout: Commande_result = Commande_result()

    def set_cmd(self, commande: str) -> None:
        self.commande: str = commande

    def set_params(self, params: str) -> None:
        self.params = params

    def set_stdin(self, stdin: Commande_result) -> None:
        self.stdin = stdin.copy()

    def print(self, ligne: str) -> None:
        self.stdout.print(ligne)

    def run(self) -> None:
        match self.commande.lower():
            case "cat":
                if self.stdin.content:
                    if not self.stdout.filename:
                        self.stdout = self.stdin.copy()
                else:
                    for fichier in filter(lambda x: not x.startswith("-"), self.params.split()):
                        self.stdout.from_file(fichier)

            case "grep":
                filtre = " ".join(filter(lambda x: not x.startswith("-"), self.params.split()))
                self.stdout.print(list(filter(lambda x: x.count(filtre) > 0, self.stdin.content)))

            case "wc":
                if "-l" in self.params:
                    self.stdout.print(str(len(self.stdin.content)))

            case "echo":
                self.stdout.print(self.params)

        if DEBUG:
            print(f"Run: {self.commande}, params: {self.params}")
            print(self.stdout.content)
            print()
        

class CommandLine:

    def __init__(self, ligne: str) -> None:
        self.pile_commandes: list = []
        self.split_commandes(ligne.strip())

    def split_commandes(self, ligne: str):
        index: int = 0
        longeur: int = len(ligne)
        caractere: str = ""
        get_stdin: bool = False
        while index < longeur:
            caractere = ligne[index]
            match caractere:
                case "|" | "&":
                    self.pile_commandes.append({"get_stdin": get_stdin, "command": ligne[:index]})
                    if ligne[1+index] == caractere:
                        index += 1
                        get_stdin = False
                    else:
                        get_stdin = True

                    ligne = ligne[1+index:].strip()
                    index = 0
                    longeur = len(ligne)

            index += 1

        self.pile_commandes.append({"get_stdin": get_stdin, "command": ligne})

    def run(self) -> Commande_result:
        entree_standard: str = ""
        sortie_standard: str = ""
        previous_sortie: Commande_result = Commande_result()
        commande: Commande

        for element in self.pile_commandes:
            cmd = element["command"]
            if DEBUG:
                print(f"[Analyse: {cmd}]")
            commande = Commande()
            params = ""
            if element["get_stdin"]:
                if DEBUG:
                    print("recuperation de la sortie standard de la precedente commande")
                commande.stdin = previous_sortie.copy()

            if ">" in cmd:
                cmd_params, sep, sortie_standard = cmd.partition(">")
                commande.stdout.to_file(sortie_standard.strip())
            else:
                cmd_params = cmd

            if "<" in cmd_params:
                cmd_params, sep, entree_standard = cmd_params.partition("<")
                commande.stdin.from_file(entree_standard.strip())

            cmde, *parms = cmd_params.split()
            params = " ".join(parms)
            commande.set_cmd(cmde)
            if parms:
                commande.set_params("".join(params))

            commande.run()
            previous_sortie = commande.stdout.copy()

        return previous_sortie


match 2:
    case 1:
        cl = CommandLine("cat < /bat/song.xml | grep -i container | wc -l ")
        cl.run().to_screen()

    case 2:
        CommandLine("cat -o -i /bat/ip.bat  /bat/ip.bat | grep on").run().to_screen()
        # CommandLine("cat -o -i /bat/song.xml").run().to_screen()

    case 3:
        CommandLine("echo Hello World | grep -i Hello").run().to_screen()
    case 4:
        CommandLine("wc -l > /dev/null && echo Fini").run().to_screen()

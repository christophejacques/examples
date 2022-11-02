import traceback
from datetime import datetime
import time
from tempfile import gettempdir


class LogLevel:
    DATA = {
            "": 0,
            "DEBUG": 1,
            "INFO": 2,
            "WARNING": 3,
            "ERROR": 4,
            "CRITIQUE": 5,
            "TRACE": 6
        } 
    MINLEVEL = 0
    TAILLE_MAX_STR = max([len(x) for x in DATA])

    def __init__(self, valeur):
        self.can_be_logged = False
        if type(valeur) == int:
            for level, i in LogLevel.DATA.items():
                if valeur == i:
                    self.can_be_logged = i >= LogLevel.MINLEVEL
                    self.s_level = level
                    self.i_level = i
                    return
            raise KeyError(valeur)
        else:
            self.i_level = LogLevel.DATA[valeur.upper()]
            self.s_level = valeur
            self.can_be_logged = self.i_level >= LogLevel.MINLEVEL

    @property
    def value(self):
        return self.i_level

    def __str__(self):
        return self.s_level

    def set_minimum(self):
        LogLevel.MINLEVEL = self.i_level


LogLevel("").set_minimum()
DEBUG = True
COMPTEUR: list = []
logger = None


class Logger:
    def __init__(self, filename):
        self.file = open(f"{gettempdir()}\\{filename}", mode="w")
        self.file.write("Fichier créé le : ")
        self.file.write(f"{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        self._log = []

    def close(self):
        if self.file:
            self.file.close()

    def show_loglevels(self):
        self.log(LogLevel("TRACE"), "Liste des niveaux de Logs tracés : [")
        for level in LogLevel.DATA:
            self.log(LogLevel(level), "{} {}".format(LogLevel(level).value, level))
        self.log(LogLevel("TRACE"), "]")

    def log(self, level, msg, **kwargs):
        if not level.can_be_logged:
            return

        if kwargs:
            for kwarg in kwargs:
                if kwarg not in ("join",):
                    raise TypeError(f"log() got an unexpected keyword argument '{kwarg}'.")
        if COMPTEUR:
            compteur = COMPTEUR[-1]
            addstr = "  " * compteur
        else:
            addstr = ""

        if kwargs.get("join"):
            self._log[-1] += msg
            self.file.write(msg)
        else:
            self._log.append(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S.%f")[:-4] + " - " + msg)
            mon_format = "\n{} - {:<" + str(LogLevel.TAILLE_MAX_STR) + "} - {}{}"
            # print(mon_format)
            self.file.write(
                mon_format.format(datetime.now().strftime('%d/%m/%Y %H:%M:%S.%f'), 
                str(level), addstr, msg))

    def print(self):
        for ligne in self._log:
            print(ligne)


def list_to_str(liste):
    return [val if type(val) == str else str(val) for val in liste]


def debug(log_fonction=True):
    def decorateur(fonction):
        def get_params(*args, **kwargs):
            if not COMPTEUR:
                compteurf = 0
                COMPTEUR.append(0)
            else:
                compteurf = COMPTEUR[-1]

            if log_fonction:
                debut = time.perf_counter()
                logger.log(LogLevel("DEBUG"),  f"@begin[{compteurf}, {fonction.__name__}(")
                logger.log(LogLevel("DEBUG"), ", ".join(list_to_str(args)), join=True)
                logger.log(LogLevel("DEBUG"), ") ]", join=True)

            compteur_inner = COMPTEUR[-1]+1
            COMPTEUR.append(compteur_inner)
            try:
                res = fonction(*args, **kwargs)
            except Exception as e:
                res = None
                logger.log(LogLevel("ERROR"), f"#!Error: {e}")  
                logger.log(LogLevel("ERROR"), traceback.format_exc())
                COMPTEUR.remove(compteur_inner)
                if log_fonction:
                    fin = time.perf_counter()
                    logger.log(LogLevel("DEBUG"), f"@end[{compteurf}, {fonction.__name__} ] durée={fin-debut:0.2f}s")
                raise e

            COMPTEUR.remove(compteur_inner)
            if log_fonction:
                fin = time.perf_counter()
                logger.log(LogLevel("DEBUG"), f"@end[{compteurf}, {fonction.__name__} ] durée={fin-debut:0.2f}s")
            return res

        return get_params
    return decorateur


@debug()
def fib(n):
    if n <= 2: 
        return 1
    else:   
        return fib(n-2) + fib(n-1)


@debug()
def submain2(n):
    res = fib(n)
    restr = f"Fib({n})={res}"
    logger.log(LogLevel("INFO"), restr)
    print(restr)


@debug()
def submain1(n):
    res = fib(n)
    restr = f"Fib({n})={res}"
    logger.log(LogLevel("INFO"), restr)
    print(restr)
    submain2(n)


@debug()
def main():
    # for i in range(28,31):
    # for i in range(2,4):
    i = 5
    res = fib(i)
    restr = f"Fib({i})={res}"
    print(restr)
    logger.log(LogLevel("INFO"), restr)
    # submain1(i)
    # b = test


try:
    logger = Logger("testlog.txt")
    # logger.show_loglevels()
    logger.log(LogLevel("TRACE"), "Debut")
    if __name__ == '__main__':
        main()
        a = 1/0

except Exception as e:
    logger.log(LogLevel("ERROR"), f"Erreur: {e}")
    print("Erreur")

if logger:
    logger.log(LogLevel("TRACE"), "Fin")
    logger.close()

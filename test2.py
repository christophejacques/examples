#! c:\bat\python.bat -3.10
import sys
import urllib.request as ur
import datetime as dt
import requests


URL = "https://www.youtube.com/ChristopheJacquesMichael/"
URL = "http://perso.numericable.com/cjacques/OSIRIS_LFI/Actualisation_Financeurs.txt"


s = requests.Session()
r = s.get(URL)
print(dir(r))
for h in r.headers:
    print(h, ":", r.headers.get(h))

if not r.ok:
    exit(1)

content = "".join(filter(lambda l: "/" in l, r.headers.get("Content-Type", "").split(";")))
print("CONTENT:", content)

match content.split("/"):
    case ["text", "plain"]:
        for i, ligne in enumerate(r.iter_lines()):
            if i > 5: break
            ident, libelle, code = ligne.decode().split("|")
            print(" ", f"{ident[:5]} | {code.strip():20} | {libelle.strip()}")
            if not ident.isnumeric():
                print("-"*80)

    case ["text", "html"]:
        for i, ligne in enumerate(r.iter_lines()):
            print(" ", f"{ligne.strip()[:80]}")


def timeit(fonction):
    def get_params(*args: object, **kwargs: object):
        debut = dt.datetime.now()
        res = fonction(*args, **kwargs)
        fin = dt.datetime.now()
        print(f"durée: {fin-debut}")
        return res
    return get_params


@timeit
def fonc():
    rq = ur.Request(URL)
    # print(dir(rq))
    if rq.headers:
        print("HEADERS:", rq.headers)
    print("FULL URL:", rq.full_url)
    print("TYPE:", rq.type)
    print("HOST:", rq.host)
    print("SELECTOR:", rq.selector)
    
    with ur.urlopen(URL) as page:
        print(dir(page))
        # print("URL:", page.url)
        print("STATUS:", page.status)
        print("HEADERS:")
        for h in page.headers:
            print("-", h, ":", page.headers.get(h))
        print("CODE:", page.code)
        print("READ:")
        if page.code == 200:
            for ligne in map(lambda l: l.strip().decode(), page.readlines()[:5]):
                print("-", ligne)


fonc()
exit(0)


def fonction(a: int | str) -> bool:
    return str(a) == "0"


def get_match(a: object):
    match a:
        case None:
            res = "None"
        case [fichier, *params]:
            res = f"fichier: {fichier}\nliste: {params}"
        case _:
            res = f"Type variable: {a.__class__.__name__}"
    return res


def main(args):
    print("args:", get_match(args))


if __name__ == "__main__":
    main(sys.argv)
else:
    pass

import sys
import urllib.request as ur
import datetime as dt
import requests


URL = "https://www.youtube.com/ChristopheJacquesMichael/"

def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


s = requests.Session()
r = s.get(URL)
for h in r.headers:
    fprint(h, ":", r.headers.get(h))

if not r.ok:
    exit(1)

content = "".join(filter(lambda texte: "/" in texte, r.headers.get("Content-Type", "").split(";")))
fprint("CONTENT:", content)
print()

match content.split("/"):
    case ["text", "plain"]:
        for i, ligne in enumerate(r.iter_lines()):
            if i > 5: 
                break
            ident, libelle, code = ligne.decode().split("|")
            fprint(" ", f"{ident[:5]} | {code.strip():20} | {libelle.strip()}")
            if not ident.isnumeric():
                fprint("-"*80)

    case ["text", "html"]:
        for i, ligne in enumerate(r.iter_lines()):
            fprint(" ", f"{ligne.strip()[:160]}")

    case _:
        fprint("content:", content, "non pris en compte")


def timeit(fonction):
    def get_params(*args: object, **kwargs: object):
        debut = dt.datetime.now()
        res = fonction(*args, **kwargs)
        fin = dt.datetime.now()
        fprint(f"duree: {fin-debut}")
        return res
    return get_params


@timeit
def fonc():
    print()
    rq = ur.Request(URL)
    # print(dir(rq))
    if rq.headers:
        print("HEADERS:", rq.headers)
    fprint("FULL URL:", rq.full_url)
    fprint("TYPE:", rq.type)
    fprint("HOST:", rq.host)
    fprint("SELECTOR:", rq.selector)
    
    with ur.urlopen(URL) as page:
        print("URL:", page.url)
        fprint("STATUS:", page.status)
        fprint("HEADERS:")
        for h in page.headers:
            fprint("-", h, ":", page.headers.get(h))
        fprint("CODE:", page.code)
        fprint("READ:")
        
        if page.status == 200:
            for ligne in map(lambda texte: texte.strip().decode(), page.readlines()[:5]):
                fprint("-", ligne[:120])




if __name__ == "__main__":
    fonc()

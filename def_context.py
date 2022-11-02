from urllib.request import urlopen
from contextlib import contextmanager
# , closing


@contextmanager
def monurlopen(url, **kwargs):
    print("Setup context manager()")
    erreur = False
    page = None
    try:
        page = urlopen(url)
    except Exception as e:
        erreur = True
        print("  Init Error:", e)

    try:
        if erreur:
            yield []
        else:
            yield page
    except Exception as e:
        if kwargs.get("catch_error"):
            print("  In context Error:", e)
        else:
            raise e

    finally:
        print("Exit context manager", end=": ")
        if not erreur and page:
            page.close()
            print("Context Manager closed", end=", ")
        print("Ok")


with monurlopen("https://www.python.org/", catch_error=True) as mapage:
    if hasattr(mapage, "status"):
        print("  Response:", mapage.status)
    for i, line in enumerate(mapage):
        print(" ", line.decode(), end="")
        if i > 2:
            break
    a = 1 / 0
    print("Il n'y a eu aucune erreur !")


print("Fin")
# input()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from msvcrt import getch

# ---------------------------------------------------------
#
# codage UTF-8 des instruction affichée via commande print()
#
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# ---------------------------------------------------------

def printf(*args, **kwargs):
    print(*args, **kwargs, flush=True)


printf("loading Firefox webdriver : ", end="")

driver = webdriver.Firefox()
printf("Ok")
driver.set_window_rect(1000, 1, 920, 1050)

printf("loading 'http://www.python.org' : ", end="")
driver.get("http://www.python.org")

# pause implicite de 10s
driver.implicitly_wait(10)

assert "Python" in driver.title
printf("Ok")

elem = driver.find_element_by_name("q")

printf("Recherche sur : try except")
elem.clear()
elem.send_keys("try except")
elem.send_keys(Keys.RETURN)


def wait_for_element(source, type_element, nom_element, continu = True):

    loop_count = 1
    found = False
    res = None

    while not found:
        try:
            if type_element == "ID":
                res = source.find_element_by_id(nom_element)

            elif type_element == "TAG_NAME":
                res = source.find_element_by_tag_name(nom_element)

            elif type_element == "TAGs_NAME":
                res = source.find_elements_by_tag_name(nom_element)

            elif type_element == "CSS_SELECTOR":
                res = source.find_element_by_css_selector(nom_element)

            elif type_element == "LINK_TEXT":
                res = source.find_element_by_link_text(nom_element)

            else:
                raise BaseException("type_element '{}' inconnu !".format(type_element))

            found = True


        except BaseException:
            raise

        except:
            msg = "{:%Y%m%d-%H%M%S}_wait_elt_{}-{}_n_{}.png"\
                .format(datetime.datetime.now(), type_element, nom_element, loop_count)
            printf(msg)

            loop_count += 1
            found = loop_count > 3
            if not continu:
                driver.save_screenshot("screenshots\\{}".format(msg) )
                raise

    return res


num_page = 1
max_page = 3

try:
    while num_page < max_page:

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list-recent-events.menu")))

        conteneur = wait_for_element(driver, "ID", "content", False)
        form = wait_for_element(conteneur, "TAG_NAME", "form", False)
        ul_elt = wait_for_element(form, "CSS_SELECTOR", "ul.list-recent-events.menu")
        titres = wait_for_element(ul_elt, "TAGs_NAME", "a")

        printf("nb results = {}".format(len(titres)))

        for lien in titres:
            printf("- {}".format(lien.text))

        num_page += 1
        suivant = wait_for_element(form, "LINK_TEXT", "Next »")
        suivant.click()

        if "No results found." in driver.page_source:
            printf("Aucun resultat trouvé !")
            num_page = max_page


except:
    printf("erreur detectee !")
    raise

finally:
    driver.close()

printf("Appuyez sur une touche")
getch()
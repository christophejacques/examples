from typing import Generator, Self


class Element:
    __tag: str
    __attrs: dict

    def __init__(self, tag: str, attrs: list[tuple]):
        self.__tag = tag.lower()
        self.__attrs = dict()
        for k, v in attrs:
            self.__attrs[k.lower()] = v.lower()

    def getAttrs(self) -> dict:
        return self.__attrs

    def getTag(self) -> str:
        return self.__tag

    def __eq__(self, other) -> bool:
        if not isinstance(other, Element):
            raise Exception("other n'est de type Element")
        if self.__tag != other.__tag:
            return False

        return True

    def __str__(self) -> str:
        return self.__tag + f"{self.__attrs}"


class XPath:
    __elts: list[Element]
    __index : int

    def __init__(self):
        self.__elts = list()
        self.__index = -1

    def hasElement(self) -> bool:
        return len(self.__elts) > 0

    def getFirstElement(self) -> Element:
        if len(self.__elts) == 0:
            raise Exception("Aucun element n'est present")

        self.__index = 0
        return self.__elts[0]

    def hasNextElement(self) -> bool:
        return self.__index <= len(self.__elts)

    def getNextElement(self) -> Element:
        self.__index += 1
        return self.__elts[self.__index]

    def getAllElements(self) -> Generator:
        for element in self.__elts:
            yield element

    def add(self, element: Element) -> Self:
        if not isinstance(element, Element):
            raise Exception("element n'est de type Element")

        self.__elts.append(element)
        return self

    def pop(self) -> Element:
        element = self.__elts.pop()
        return element

    def begins_with(self, xpath, check_attrs: bool=False) -> bool:
        if not isinstance(xpath, XPath):
            raise Exception("xpath n'est de type XPath")

        self_size = len(self.__elts)
        xpath_size = len(xpath.__elts)
        if self_size == 0 or self_size < xpath_size:
            return False

        controle = zip(self.__elts, xpath.__elts)
        for i1, i2 in controle:
            if not i1 == i2:
                print(i1, "!=", i2)
                return False

            if check_attrs and i1.getAttrs() != i2.getAttrs():
                print(i1, "(attrs) !=", i2, "(attrs)")
                return False


        print(xpath, "in", self)
        return True

    def __str__(self) -> str:
        chaine: str = " > "
        # for elt in sorted(self.__elts, key=lambda x: x.getTag()):
        for elt in self.getAllElements():
            chaine += f"{elt} / "

        return f"[{chaine[3:-3]}]"


print("Debut")
d = Element("div", [("class", "hidden")])
a = Element("A", [("class", "hidden"), ("href", "http://www.google.fr")])

x = XPath()
x.add(d)
x.add(a)

print(x)
x.begins_with(XPath().add(Element("a", [("class", "button")])))
x.begins_with(XPath().add(Element("div", [("class", "button")])))
x.begins_with(XPath().add(Element("div", [("class", "button")])), check_attrs=True)

print(x.pop())
print(x)

from xml.dom.minidom import parseString, Element


fstring = """
<DIR attr="valeur" size="12">
    <UN>
        <name>fdcr</name>
        <extension>.ods</extension>
        <vide/>
    </UN>
    <DEUX attrib="cinq">
        <name>fdcop</name>
        <age>15</age>
    </DEUX>
</DIR>"""


class myXml():
    DEBUG = True

    def __init__(self, xml_string):
        self.dictionnaire = {}
        self.node_tagname = ""
        self.node_tagvalue = ""
        self.chemin = []
        self.integrate(xml_string)

    def integrate(self, xml_string):
        self.root = None
        try:
            parse = parseString(xml_string)
            if parse:
                self.get_list(parse)

        except Exception as e:
            print("Error:", e)

    def __str__(self):
        res = "{\n"
        for cle, valeur in self.dictionnaire.items():
            res += f" '{cle}': '{valeur}',\n"
        res = res + "}"
        return res

    def get_attributes(self, node):
        if not node.hasAttributes(): 
            return ""

        res = " "
        for attr, valeur in node.attributes.items():
            res += f"{attr}='{valeur}' "
        return res.rstrip()

    def get_list(self, current, level=0):
        res = False
        for node in current.childNodes:
            if node.nodeType == Element.TEXT_NODE:
                if self.DEBUG: 
                    print(node.data.strip(), end="")
                self.node_tagvalue = node.data.strip()

            elif node.nodeType == Element.ELEMENT_NODE:
                res = True
                if self.DEBUG: 
                    print("\n" + "  "*level + f"<{node.nodeName}{self.get_attributes(node)}>", end="")

                self.node_tagname = node.nodeName
                self.node_tagvalue = ""
                self.chemin.append(self.node_tagname)

                if self.get_list(node, level+1):
                    if self.DEBUG: 
                        print("\n" + "  "*level + f"</{node.nodeName}>", end="")
                else:
                    if self.DEBUG: 
                        if self.node_tagvalue == "":
                            print("</>", end="")
                        else:
                            print(f"</{node.nodeName}>", end="")
                    if self.node_tagvalue:
                        self.dictionnaire["/" + "/".join(self.chemin)] = self.node_tagvalue

                self.chemin.pop()

        return res


mon_xml = myXml(fstring)
# print(f"\n{mon_xml}")

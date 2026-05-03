from typing import List, Optional

from documents import DocumentAMQ, DocumentElastic


class DataBase:
    # classe de base pour définir les classes
    # ActiveMQ et Elastic

    def __init__(self, name: str):
        self.contenu: List = list()
        self.name: str = name

    def isEmpty(self) -> bool:
        return len(self.contenu) <= 0

    def __len__(self) -> int:
        return len(self.contenu)

    def __str__(self) -> str:
        contenu = [doc.ident for doc in self.contenu]
        return f"{self.name} " + str(contenu)


class ActiveMQ(DataBase):

    contenu: List[DocumentAMQ]

    def add(self, document: DocumentAMQ) -> None:
        # ajout du document dans la file activeMQ
        self.contenu.append(document)

    def pop(self) -> Optional[DocumentAMQ]:
        if self.isEmpty():
            return None

        doc = self.contenu.pop(0)
        return doc

    def view(self) -> Optional[DocumentAMQ]:
        if self.isEmpty():
            return None

        doc = self.contenu[0]
        return doc


class IndexElastic(DataBase):

    contenu: List[DocumentElastic]

    def add(self, document: DocumentElastic) -> None:
        # ajout du document dans l'index
        self.contenu.append(document)

    def has_document(self, ident: int) -> bool:
        for document in self.contenu:
            if ident == document.ident:
                return True

        return False

import pickle
from base64 import b64encode, b64decode
import traceback
from enum import Enum, auto


def crc16(data):
    if data is None:
        return 0
    crc = 0xFFFF

    for i in range(len(data)):
        crc ^= data[i] << 8
        for j in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF


class TypeTransfert(Enum):

    MESSAGE = auto()
    PICKLE = auto()
    NONE = auto()


class Paquet:

    DEBUTPAQUET = b'!'
    FINPAQUET = b'$'
    SEPARATEUR = b'#'

    def __init__(self):
        self.objet = None
        self.type = None
        self.error = None

    def encode(self, objet, type_objet=TypeTransfert.PICKLE):
        # Encoding :
        # DEBUT <type> SEP <crc16_init> SEP <crc16_encodee> SEP <objet> FIN
        self.__init__()
        try:
            if type_objet.__class__ != TypeTransfert:
                self.error = "TypeError : le type du champ type_objet n'est pas TypeTransfert mais {}".format(type_objet.__class__.__name__)
                return None
            self.type = type_objet
            self.objet = objet

            if self.type == TypeTransfert.PICKLE:
                objet = pickle.dumps(objet)

            if type(objet) != bytes:
                objet = bytes(str(objet), encoding="UTF-8")

            msg = Paquet.DEBUTPAQUET
            msg += bytes(str(type_objet.value), encoding="UTF-8") + Paquet.SEPARATEUR
            msg += bytes(str(crc16(objet)), encoding="UTF-8") + Paquet.SEPARATEUR

            objet_b64 = b64encode(objet)
            msg += bytes(str(crc16(objet_b64)), encoding="UTF-8") + Paquet.SEPARATEUR
            msg += objet_b64
            msg += Paquet.FINPAQUET

        except Exception as e:
            self.error = "decodeError: {}".format(e)
            traceback.print_exc()
            return None

        return msg

    def decode(self, paquet):
        # Decoding :
        # DEBUT <type> SEP <crc16_init> SEP <crc16_encodee> SEP <objet> FIN
        self.__init__()
        try:
            if type(paquet) != bytes:
                self.error = "Le paquet n'est pas de type bytes"
                return None
            if not (paquet.startswith(Paquet.DEBUTPAQUET) and paquet.endswith(Paquet.FINPAQUET)):
                self.error = "Le paquet n'a pas de début et/ou de fin"
                return None

            # trame = paquet.removeprefix(Paquet.DEBUTPAQUET).removesuffix(Paquet.FINPAQUET)
            trame = paquet[len(Paquet.DEBUTPAQUET):-len(Paquet.FINPAQUET)]

            msg_split = trame.split(Paquet.SEPARATEUR)
            if len(msg_split) != 4:
                self.error = "La trame encodée n'a pas pu être décodée"
                return None

            self.type, crc16_init, crc16_encodee, objet_b64 = msg_split
            if crc16(objet_b64) != int(crc16_encodee):
                self.error = "CRC Error lors du décodage de la trame encodée en Base64"
                return None

            self.objet = b64decode(objet_b64)
            if crc16(self.objet) != int(crc16_init):
                self.error = "CRC Error lors du décodage de la trame décodée"
                return None

            self.type = int(self.type)
            if self.type == TypeTransfert.MESSAGE.value:
                self.objet = self.objet.decode("UTF-8")
            elif self.type == TypeTransfert.PICKLE.value:
                self.objet = pickle.loads(self.objet)
            elif self.type == TypeTransfert.NONE.value:
                pass
            else:
                self.error = "Le type du paquet est incorrecte: {}".format(self.type)
                return None

        except Exception as e:
            self.error = "decodeError: {}".format(e)
            traceback.print_exc()
            return None

        return self.objet


def main():
    objet = {'entier': 5,
        'float': 3.74,
        'string': "val'orisé".encode("utf-8").decode("ansi"),
        'cde': "!USER vénère".encode("utf-8").decode("ansi"),
        'liste': [1, 2, 3, True, "Texte"],
        'bool': True}

    p = Paquet()
    # objet = 1.25
    # Encoding
    oEncode = p.encode(objet)
    if p.error:
        print(p.error)
        exit(1)
    else:
        print(oEncode, "\n")

    # Decoding
    oDecode = p.decode(oEncode)
    if p.error:
        print(p.error)
    else:
        print(type(oDecode))
        print(oDecode, "\n")


if __name__ == '__main__':
    main()

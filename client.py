import socket
from time import sleep
from threading import Thread
import traceback
from msvcrt import kbhit
from coding import Paquet
import sys


HOST = socket.gethostname()
print("Lancement depuis:", HOST)
# if len(sys.argv) != 2:
#     print("Utilisation: client <nom_utilisateur>")
#     exit(1)

USER = " ".join(sys.argv[1:]).strip()
if USER:
    HOST = USER
print("Connect to :", HOST)


class Client:

    def __init__(self, host="localhost"):
        self.server_open = False
        self.server_running = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(5)
        self.host = host
        self.port = 8081
        try:
            print("Connexion au serveur: {}:{}".format(self.host, self.port))
            self.server.connect((self.host, self.port))
        except (TimeoutError, socket.timeout):
            print("TimeoutError: Impossible de se connecter au serveur")
        except ConnectionRefusedError:
            print("ConnectionRefusedError: Impossible de se connecter au serveur")
        except socket.gaierror:
            print("gaierror: Impossible de se connecter au serveur")
        except Exception:
            traceback.print_exc()
        else:
            print("Sock name:", self.server.getsockname())
            self.paquet = Paquet()
            self.server_open = True

    def close(self):
        if self.server:
            sleep(1)
            self.server.close()
        self.server_open = False
        self.server_running = False

    def is_server_alive(self):
        if self.server_open:
            send_msg = self.paquet.encode(
                {"commande": "IS_SERVER_ALIVE", "args": ""})
            try:
                self.server.send(send_msg)
            except (ConnectionAbortedError, ConnectionResetError):
                self.server_open = False
                self.server_running = False

    def send(self, commande, args):
        if self.server_open:
            send_msg = self.paquet.encode(
                {"commande": commande,
                 "args": args})

            try:
                self.server.send(send_msg)
            except (ConnectionAbortedError, ConnectionResetError):
                self.server_open = False
                self.server_running = False

    def traitement(self):
        message = self.paquet.decode(self.message)
        # print(message)
        if message and message.get("commande", None):
            commande = message["commande"]
            if commande in ("KO"):
                print(message["args"])
            elif commande in ("SAY"):
                print(message["args"])
            elif commande not in ("OK", "KO"):
                print(f"Demande de traitement de la commande : {commande}")
                print("args:", message.get("args", ""))
            else:
                chaine = message.get("args", None)
                if chaine:
                    print(chaine)
                return True
        else:
            print("Aucune commande en provenance du serveur")

        return False

    def get_char(self):
        retry = 2
        car, card = b"", b""
        while self.server_running and self.waiting_server and retry > 0:
            try:
                car = self.server.recv(1)
                card += car

            except socket.timeout:
                pass
            except UnicodeDecodeError:
                retry -= 1
                if retry == 0:
                    card = b"?"
            except (ConnectionAbortedError, ConnectionResetError):
                # WinError 10053, 10054
                retry = 0
                card = b""
                self.server_running = False

            except Exception:
                print("Recv Car Error:")
                retry = 0
                traceback.print_exc()
                card = b""
            else:
                retry = 0

        return card

    def thread_recv(self):
        self.waiting_server = True
        self.server_running = True
        if self.server:
            while self.server_running and self.waiting_server:
                try:
                    fin_message = False
                    while self.server_running and not fin_message and self.waiting_server:
                        self.message = b""
                        car = None
                        while self.server_running and self.waiting_server:
                            try:
                                car = self.get_char()

                            except socket.timeout:
                                print("#", end="", flush=True)
                                pass
                            except Exception as e:
                                if hasattr(e, "args"):
                                    print("args:", e.args)
                                    if e.args in (10038):
                                        break
                                traceback.print_exc()

                            if self.server_running and self.waiting_server and car is not None and len(car) > 0:
                                self.message += car
                                if car == Paquet.FINPAQUET:
                                    break

                        if self.server_running and self.message and self.waiting_server:
                            fin_message = self.traitement()

                except Exception:
                    traceback.print_exc()

        self.server_open = False
        self.server_running = False
        print("Server thread closed")

    def launch_server(self):
        Thread(target=self.thread_recv, args=()).start()

    def close_waiting_server(self):
        print("Closing server connection")
        if self.server_running and self.server_open:
            self.waiting_server = False
            while self.server_open:
                sleep(1)


ATTENTE = ["-", "/", "|", "\\"]
client = Client(HOST)
if client.server_open:
    client.launch_server()
    print()
    connected = True
    index = 0
    while connected and client.server_open:
        message = ""
        print(chr(8)*2 + ATTENTE[index] + ">", end="", flush=True)
        index = 0 if index >= 3 else index+1
        client.is_server_alive()
        try:
            if kbhit():
                message = input().strip()
            else:
                sleep(0.5)

        except KeyboardInterrupt:
            connected = False
            message = ""
            client.close_waiting_server()

        if len(message) > 0 and message[0] == "!":
            commande = message[1:].upper()

            if commande in ("QUIT", "EXIT", "BYE"):
                connected = False
                client.close_waiting_server()

            elif commande in ("SERVER_SHUTDOWN", "SHUTDOWN_SERVER", "SHUTDOWN"):
                connected = False
                client.send(commande.split()[0], "")
                client.close_waiting_server()

            else:
                # Envoie la commande au serveur
                client.send(commande.split()[0], " ".join(message.split()[1:]))

        elif connected and message != "":
            client.send("SAY", message)

    client.close()

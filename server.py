# Python program to implement server side of chat room.
import socket
import traceback
from threading import Thread
from coding import Paquet


SERVER_TIMEOUT = 5
CLIENT_TIMEOUT = 5


class Commandes:

    def __init__(self):
        self.noms = {}

    def add_commande(self, cmd, for_client, alias, fonction=None, params=None):
        self.noms[cmd] = {
            "client": for_client,
            "alias": alias,
            "fonction": fonction,
            "params": params
        }
        if params:
            print("params:", params)

    def help(self):
        yield("Liste des commandes :")
        for variable in self.noms:
            if self.noms[variable]["client"]:
                yield("- " + ", ".join(self.noms[variable]["alias"]))

    def get_commande(self, cmd):
        for variable in self.noms:
            if cmd in self.noms[variable]["alias"]:
                return variable
        return None


class Server:
    RUNNING = True

    @classmethod
    def stop(self):
        print("Stopping Server")
        Server.RUNNING = False


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.settimeout(SERVER_TIMEOUT)

# takes the first argument from command prompt as IP address
IP_address = "localhost"
IP_address = socket.gethostname()  # "192.168.1.32"
Port = 8081

server.bind((IP_address, Port))
print("Server bind", (IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []
nom_clients = {}


def client_thread(conn, addr):

    print("Connexion d'un client :", addr)
    conn.settimeout(CLIENT_TIMEOUT)

    def init_thread():
        cde = Commandes()
        cde.add_commande("IS_SERVER_ALIVE", False, ["IS_SERVER_ALIVE"])
        cde.add_commande("SHUTDOWN", True, ["SHUTDOWN", "SHUTDOWN_SERVER", "SERVER_SHUTDOWN"])
        cde.add_commande("EXIT", True, ["BYE", "EXIT", "QUIT"])
        cde.add_commande("LIST", True, ["LIST", "LISTE"])
        cde.add_commande("SAY", True, ["SAY", "TELL", "DIRE"])
        cde.add_commande("HELP", True, ["HELP", "AIDE", "?"])
        cde.add_commande("USER", True, ["USER", "NAME", "NOM", "UTILISATEUR"])
        cde.add_commande("LOGIN", True, ["CONNECT", "LOGIN"])
        cde.add_commande("LOGOUT", True, ["DISCONNECT", "LOGOUT"])
        return cde

    def liste_clients(connection):
        msg = "Liste des participants :"
        message = {"commande": "SAY", "args": msg}
        print(msg)
        connection.send(paquet.encode(message))
        for client in list_of_clients:
            client = nom_clients.get(client.getpeername())
            if client:
                msg = f"- {client}"
                message = {"commande": "SAY", "args": msg}
                print(msg)
                connection.send(paquet.encode(message))

        return {"commande": "OK"}

    def deja_connecte():
        return {"commande": "KO", "args": "Vous êtes déjà connecté."}

    def rename_client(addr, nom):
        nom = nom.strip()
        if len(nom) > 20:
            return {"commande": "KO", "args": "La taille du nom ne peut être supérieure à 20 caractères"}

        if nom:
            print("Connexion de", nom)
            nom_clients[addr] = nom
            return {"commande": "OK", "args": f"Renommage: {nom}"}

        return {"commande": "KO", "args": "Il faut donner un nom après la commande USER"}

    def shutdown_server():
        global no_error

        no_error = False
        Server.stop()
        return {"commande": "OK"}

    def aide_clients():
        for cmd in cde.help():
            message = {"commande": "SAY", "args": cmd}
            print(cmd)
            conn.send(paquet.encode(message))
        return {"commande": "OK"}

    def say_all(conn, message):
        # Calls broadcast function to send message to all
        message_to_send = f"{nom_clients[conn.getpeername()]}> {message}"
        print(message_to_send)
        broadcast(message_to_send, conn)
        return {"commande": "OK"}

    cde = init_thread()
    paquet = Paquet()
    user_connected = False

    # sends a message to the client whose user object is conn
    msg = f"Server> Welcome to this chatroom ! {addr}"
    message = {"commande": "SAY", "args": msg}
    conn.send(paquet.encode(message))
    message = {"commande": "OK"}
    conn.send(paquet.encode(message))

    client_running = True

    no_error = True
    while Server.RUNNING and client_running and no_error:

        try:
            message_received = False
            message = b""
            msg = {}
            while not message_received and Server.RUNNING and client_running:
                retry = 2
                car, card = b"", b""
                while client_running and Server.RUNNING and retry > 0:
                    try:
                        car = conn.recv(1)
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
                        client_running = False

                    except Exception:
                        print("Recv Car Error:")
                        retry = 0
                        traceback.print_exc()
                        card = b""

                    else:
                        retry = 0

                if client_running and (card == b"" or card == Paquet.FINPAQUET):
                    message_received = True
                    message += card
                    msg = paquet.decode(message)
                    if msg:
                        if msg["commande"] != "IS_SERVER_ALIVE":
                            print("Msg:", msg)

                elif client_running:
                    message += card

            if client_running and msg and msg.get("commande", None):
                commande = msg["commande"]
                alias = cde.get_commande(commande)
                if alias != "IS_SERVER_ALIVE":
                    print("alias:", alias)
                if alias in cde.noms:
                    if user_connected:
                        if alias == "IS_SERVER_ALIVE":
                            message = None
                        elif alias == "LIST":
                            message = liste_clients(conn)
                        elif alias == "LOGOUT":
                            message = {"commande": "OK", "args": "Vous êtes déconnecté."}
                            user_connected = False
                        elif alias == "HELP":
                            message = aide_clients()
                        elif alias == "SHUTDOWN":
                            message = shutdown_server()
                        elif alias == "USER":
                            message = rename_client(addr, msg["args"])
                        elif alias == "SAY":
                            message = say_all(conn, msg["args"])
                        elif alias == "LOGIN":
                            message = deja_connecte()

                    elif alias == "LOGIN":
                        message = rename_client(addr, msg["args"])
                        if message["commande"] == "OK":
                            user_connected = True
                    elif alias == "IS_SERVER_ALIVE":
                        message = None
                    else:
                        message = {"commande": "KO",
                                   "args": "Utilisez la commande !LOGIN pour vous connecter."}

                else:
                    message = {"commande": "KO",
                               "args": "Commande inconnue : {}".format(msg["commande"])}

                if message:
                    print(message, "to", conn.getpeername())
                    conn.send(paquet.encode(message))

            elif client_running:
                # indiquer au client que le traitement de son message est KO
                message = {"commande": "KO", "args": "Aucune commande"}
                print(message, "to", conn.getpeername())
                conn.send(paquet.encode(message))

        except Exception as e:
            if hasattr(e, "args"):
                no_error = False
                if e.args[0] != 10054:
                    print("Exception:", e)
                    traceback.print_exc()
            else:
                print("Exception:", e)
                traceback.print_exc()
            continue
    remove(conn)
    conn.close()


def broadcast(message, connection):
    paquet = Paquet()

    # print("broadcast from", nom_clients[connection.getpeername()])
    for client in list_of_clients:
        if client != connection:
            # print("broadcast to", nom_clients[client.getpeername()])
            try:
                msg = {"commande": "SAY", "args": message}
                client.send(paquet.encode(msg))
                msg = {"commande": "OK"}
                client.send(paquet.encode(msg))

            except Exception as e:
                print("broadcast Error:", e)
                print(f"Remove client {nom_clients[conn.getpeername()]}")
                # if the link is broken, we remove the client
                remove(client)
                client.close()


def remove(connection):

    if connection in list_of_clients:
        list_of_clients.remove(connection)
        client = nom_clients.get(connection.getpeername())
        if client:
            print(f"Déconnexion de : {client}")
            del nom_clients[connection.getpeername()]
        else:
            print(f"Déconnexion de : {connection.getpeername()}")


while Server.RUNNING:

    try:
        conn, addr = server.accept()
    except socket.timeout:
        conn = None
    except Exception:
        traceback.print_exc()
        conn = None

    if conn:
        list_of_clients.append(conn)

        # creates and individual thread for every user that connects
        Thread(target=client_thread, args=(conn, addr)).start()

server.close()

from __future__ import annotations
from typing import Optional, Callable, Dict, List, Self, Generator, Any
from enum import Enum, auto
from functools import wraps


def definition_types(*params):
    def get_fct(fonction):
        @wraps(fonction)
        def ctrl_params(*args, **kwargs):
            for index, arg in enumerate(args):
                if params[index] is Self:
                    if index == 0:
                        continue
                    msg = "Fonction "
                    msg += fonction.__name__ 
                    msg += f"(param n°{index}) -> '"
                    msg += arg.__class__.__name__ 
                    msg += "' au lieu de 'Self'"
                    raise TypeError(msg)

                elif not isinstance(arg, params[index]):
                    msg = "Fonction "
                    msg += fonction.__name__ 
                    msg += f"(param n°{index}) -> '"
                    msg += arg.__class__.__name__ 
                    msg += "' au lieu de '" 
                    msg += params[index].__name__ + "'"
                    raise TypeError(msg)

            res = fonction(*args, **kwargs)
            return res
        return ctrl_params 
    return get_fct


class Action:
    ident: int = 0
    code: str = "INIT"
    data: Any = None

    def __init__(self, ident=None):
        if ident is None:
            self.ident = id(self)
        else:
            self.ident = ident

    @definition_types(Self, str, Dict)
    def update(self, code: str, data=None) -> None:
        self.code = code
        self.data = data

    def __str__(self) -> str:
        return f"(id:{self.ident}) {self.code}:{self.data}"


class Communication:
    DEBUG: bool = False
    session: Dict[int, Dict[int, Callable]] = dict()

    @definition_types(Self, Action, int, Callable)
    def init_port(self, action: Action, port: int, callback: Callable) -> None:
        if not Communication.session.get(port):
            Communication.session[port] = dict()
            # print("Initialisation du Port:", port)
        
        if action.code != "INIT":
            raise ValueError("L'initialisation d'un port ne peut s'effectuer que par un code action INIT")

        client_id: int = action.ident
        Communication.session[port][client_id] = callback

    @definition_types(Self, int, int)
    def close_port(self, serveur_id: int, port: int) -> None:
        if not Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'a pas encore été initialisé")

        if not Communication.session.get(port, {}).get(serveur_id):
            raise Exception(f"Le port {port} n'est pas initialisé pour {serveur_id}")

        if len(Communication.session.get(port, {})) > 1:
            raise Exception(f"Il reste des connexions ouvertes sur le port {port}")

        del Communication.session[port]
        if Communication.DEBUG:
            print("Fermeture du Port:", port)

    @definition_types(Self, int, int)
    def close_communication(self, client_id: int, port: int) -> None:
        if client_id not in Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'est pas initialisé pour {client_id}")

        del Communication.session[port][client_id]
        if Communication.session[port]:
            return

        del Communication.session[port]
        if Communication.DEBUG:
            print("Fermeture communication du Port:", port)

    @definition_types(Self, int, int)
    def has_client(self, client_id: int, port: int) -> bool:
        if not Communication.session.get(port, {}):
            return False

        return client_id in Communication.session.get(port, {})

    @definition_types(Self, int, int)
    def get_clients(self, serveur_id: int, port: int) -> Generator[int]:
        liste: List = list(Communication.session.get(port, {}))
        for instance_id in liste:
            if instance_id == serveur_id:
                continue

            yield instance_id

    @definition_types(Self, int, int, Action)
    def sendTo(self, dest_id: int, port: int, data: Action) -> None:
        if dest_id not in Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'est pas initialisé pour {dest_id}")

        fonction = Communication.session[port][dest_id]
        fonction(data)

    @definition_types(Self, int, int, Action)
    def send(self, client_id: int, port: int, data: Action) -> None:
        if client_id not in Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'est pas initialisé pour {client_id}")

        for instance_id in list(Communication.session.get(port, {})):
            if instance_id == client_id:
                continue

            fonction = Communication.session[port][instance_id]
            fonction(data)


class Fonction(Enum):
    COMMUNICATION = auto()
    TOOLS = auto()
    KEYS = auto()
    SOUND = auto()
    THEME = auto()
    REGISTRE = auto()
    IRQ = auto()
    MOUSE = auto()


class OS:
    @classmethod
    def get_fonction(cls, fonction: Fonction) -> Any:
        if not isinstance(fonction, Fonction):
            raise TypeError("Le parametre doit être de type 'Fonction'.")
            
        match fonction:
            case Fonction.COMMUNICATION:
                return Communication()

        raise TypeError("La fonctionnalite {fonc!r} n'existe pas.")


class Server:
    DEBUG: bool = False
    PORT: int = 32165
    communication: Communication
    clients: List[int] = list()
    
    def __init__(self, name: str):
        self.name = name
        self.action = Action()
        self.os = OS()
        self.communication = self.os.get_fonction(Fonction.COMMUNICATION)
        self.communication.init_port(self.action, Server.PORT, self.receive)

        if Server.DEBUG:
            print("Server", self.name, "initialized on port:", Server.PORT, "with id:", self.action.ident)

    def __enter__(self, *args) -> Self:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    @definition_types(Self)
    def close(self) -> None:
        if Server.DEBUG:
            print("Shutdown Server", self.name)
        action: Action = Action(self.action.ident)
        action.update("CLOSE", {"port": Server.PORT})

        # for client_id in self.communication.get_clients(self.action.ident, Server.PORT):
        for client_id in list(self.clients):
            # on demande au client de fermer sa connexion sur le port
            self.send(client_id, action)

            # on force la deconnexion du client du port
            self.unregister_client(client_id)

        # on ferme le port
        self.communication.close_port(self.action.ident, Server.PORT)

    @definition_types(Self, int, Action)
    def send(self, client_id: int, action: Action) -> None:
        if Server.DEBUG:
            print("  >", self.name, ":", "send to", f"id:{client_id}", "...", action)
        self.communication.sendTo(client_id, Server.PORT, action)

    @definition_types(Self, Action)
    def send_all(self, action: Action) -> None:
        sender_id: int = action.ident
        for client_id in self.communication.get_clients(self.action.ident, Server.PORT):
            if client_id != sender_id:
                self.send(client_id, action)

    @definition_types(Self, Action)
    def register_client(self, action) -> None:
        client_id = action.ident
        if not client_id:
            return 

        if client_id not in self.clients:
            self.clients.append(client_id)

            # print("#", self.name, f"New client {client_name} added (id:{client_id})")
            self.action.update("SERVER_RESPONSE", {"connected": True})
            self.send(client_id, self.action)

    @definition_types(Self, int)
    def unregister_client(self, client_id: int) -> None:
        if client_id not in self.clients:
            return

        self.clients.remove(client_id)
        if self.communication.has_client(client_id, Server.PORT):
            try:
                self.communication.close_communication(client_id, Server.PORT)
            except Exception as communication_erreur:
                print(communication_erreur)

    @definition_types(Self, Action)
    def receive(self, action: Action) -> None:
        match action.code:
            case "INIT":
                self.register_client(action)

            case "CLOSE":
                self.unregister_client(action.ident)

            case "MESSAGE":
                self.send_all(action)

            case _:
                return


class Client:
    DEBUG: bool = True
    communication: Communication
    server_id: Optional[int] = None
    
    def __init__(self, name: str):
        self.name = name
        self.os = OS()
        self.communication = self.os.get_fonction(Fonction.COMMUNICATION)
        self.action = Action()
        self.isConnected = False

    @definition_types(Self, int)
    def init_port(self, port: int) -> None:
        self.communication.init_port(self.action, port, self.receive)

        action = Action(self.action.ident)
        action.update("INIT", {"id": self.action.ident, "name": self.name})

        if Client.DEBUG:
            print(">", self.name, "looking for server", action)
        self.communication.send(self.action.ident, port, action)

    @definition_types(Self, int)
    def close_port(self, port: int) -> None:
        action = Action(self.action.ident)
        action.update("CLOSE", {"id": self.action.ident})

        self.send(port, action)

    @definition_types(Self, int, Action)
    def send(self, port: int, action: Action) -> None:
        if self.server_id is None:
            raise Exception("Aucun serveur de connecté")

        print(self.name, "send ...", action)
        self.communication.sendTo(self.server_id, port, action)

    @definition_types(Self, Action)
    def receive(self, action: Action) -> None:
        match action.code:
            case "SERVER_RESPONSE":
                self.isConnected = action.data.get("connected", False)
                if self.isConnected:
                    self.server_id = action.ident
                else:
                    print(self.name, "is NOT connected !")
                
            case "CLOSE":
                self.isConnected = False
                self.server_id = None

            case "MESSAGE":
                if not self.isConnected:
                    print("client", self.name, "is not connected")
                    return

            case _:  # INIT
                return

        if Client.DEBUG:
            print("<", self.name, "receive from", action)


if __name__ == "__main__":
    with Server("SRV") as s:
        c1 = Client("CLI1")
        c1.init_port(s.PORT)

        print()
        c2 = Client("CLI2")
        c2.init_port(s.PORT)

        print()
        c3 = Client("CLI3")
        c3.init_port(s.PORT)

        print()
        c2.action.update("MESSAGE", {"content": "Ah que coucou !"})
        c2.send(s.PORT, c2.action)

        print()
        c1.close_port(s.PORT)
        # c2.close_port(s.PORT)
        # c3.close_port(s.PORT)
        print()

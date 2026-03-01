from __future__ import annotations
from typing import Callable


def definition_types(*params):
    def get_fct(fonction):
        def ctrl_params(*args, **kwargs):
            for index, arg in enumerate(args):
                if not isinstance(arg, params[index]):
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
    data = None

    def __init__(self):
        self.ident = id(self)

    @definition_types(object, str, dict)
    def update(self, code: str, data=None) -> None:
        self.code = code
        self.data = data

    def __str__(self) -> str:
        return f"(id:{self.ident}) {self.code}:{self.data}"


if True:
    a = Action()
    for m in dir(a):
        if m[:2] == "__":
            continue
        if callable(getattr(a, m)):
            print(m)

    exit()


class Communication:
    session: dict[int, dict[int, Callable]] = dict()

    @definition_types(object, Action, int, Callable)
    def init_port(self, action: Action, port: int, callback: Callable) -> None:
        if not Communication.session.get(port):
            Communication.session[port] = dict()
            print("Initialisation du Port:", port)
        
        if action.code != "INIT":
            raise ValueError("L'initialisation d'un port ne peut s'effectuer que par une action INIT")

        client_id: int = action.ident
        Communication.session[port][client_id] = callback

    @definition_types(object, int, int)
    def close_port(self, serveur_id: int, port: int) -> None:
        if not Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'a pas encore été initialisé")

        if not Communication.session.get(port, {}).get(serveur_id):
            raise Exception(f"Le port {port} n'est pas initialisé pour {serveur_id}")

        if len(Communication.session.get(port, {})) > 1:
            raise Exception(f"Il reste des connexions ouvertes sur le port {port}")

        del Communication.session[port]
        print("Fermeture du Port:", port)

    @definition_types(object, int, int)
    def close_communication(self, client_id: int, port: int) -> None:
        if not client_id in Communication.session.get(port, {}):
            raise Exception(f"Le port {port} n'est pas initialisé pour {client_id}")

        del Communication.session[port][client_id]
        if Communication.session[port]:
            return

        del Communication.session[port]
        print("Fermeture du Port:", port)

    @definition_types(object, int, int)
    def get_clients(self, serveur_id: int, port: int) -> list[int]:
        liste = list()
        for instance_id in Communication.session.get(port, {}):
            if instance_id == serveur_id:
                continue

            liste.append(instance_id)

        return liste

    @definition_types(object, int, int, Action)
    def sendTo(self, dest_id: int, port: int, data: Action) -> None:
        if Communication.session.get(port, {}).get(dest_id) is None:
            raise Exception(f"Le port {port} n'est pas initialisé pour {dest_id}")

        fonction = Communication.session.get(port, {}).get(dest_id)
        if fonction:
            fonction(data)

    @definition_types(object, int, int, Action)
    def send(self, client_id: int, port: int, data: Action) -> None:
        if Communication.session.get(port, {}).get(client_id) is None:
            raise Exception(f"Le port {port} n'est pas initialisé pour {client_id}")

        for instance_id in Communication.session.get(port, {}):
            if instance_id == client_id:
                continue

            fonction = Communication.session[port][instance_id]
            fonction(data)


class Server:
    PORT: int = 32165
    communication: Communication
    clients: list = list()
    
    def __init__(self, name: str):
        self.name = name
        self.action = Action()
        self.communication = Communication()
        self.communication.init_port(self.action, Server.PORT, self.receive)

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        for client_id in self.communication.get_clients(self.action.ident, Server.PORT):
            self.action.update("CLOSE")
            self.communication.send(self.action.ident, Server.PORT, self.action)
            self.communication.close_communication(client_id, Server.PORT)

        self.communication.close_port(self.action.ident, Server.PORT)

    @definition_types(object, int, Action)
    def send(self, client_id: int, action: Action): 
        print("  >", self.name,":", "send ...", action)
        self.communication.sendTo(client_id, Server.PORT, action)

    @definition_types(object, Action)
    def receive(self, action: Action):
        match action.code:
            case "INIT":
                pass
            case _:
                return

        client_id = action.ident
        if not client_id:
            return 

        if client_id not in self.clients:
            self.clients.append(client_id)

            print("<", self.name, "New client ...", client_id)
            self.action.update("RESPONSE", {"connected": True})
            self.send(client_id, self.action)


class Client:
    communication: Communication
    
    def __init__(self, name: str):
        self.name = name
        self.communication = Communication()

    @definition_types(object, int)
    def init_port(self, port: int):
        self.action = Action()
        self.communication.init_port(self.action, port, self.receive)

    @definition_types(object, int)
    def close_port(self, port: int):
        self.communication.close_communication(self.action.ident, port)

    @definition_types(object, int, Action)
    def send(self, port: int, action: Action): 
        print(self.name, "send ...", action)
        self.communication.send(self.action.ident, port, action)

    @definition_types(object, Action)
    def receive(self, action: Action):
        match action.code:
            case "RESPONSE":
                pass
            case "CLOSE":
                pass
            case _:
                return

        print("<", self.name, "receive ...", action)


if __name__ == "__main__":
    with Server("SRV") as s:
        c1 = Client("CLI1")
        c1.init_port(s.PORT)
        c1.action.update("INIT", {"id": c1.action.ident})
        c1.send(s.PORT, c1.action)

        print()
        c2 = Client("CLI2")
        c2.init_port(s.PORT)
        c2.action.update("INIT", {"id": c2.action.ident})
        c2.send(s.PORT, c2.action)

        c1.close_port(s.PORT)
        # c2.close_port(s.PORT)

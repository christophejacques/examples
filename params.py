
class SwitchParams:

    def __init__(self):
        self.PARAMS = []

    def add_param(self, fonction, param, nb_params=0):
        self.PARAMS.append([param, fonction, nb_params])

    def check_param(self, param, params):
        for defparam in self.PARAMS:
            if defparam[0] == param:
                if defparam[2] > 0:
                    pos = params.index(param)
                    if len(params) > pos + defparam[2]:
                        return defparam[2] + 1
                    return 0
                return 1
        return 0

    def exec_param(self, param, *params):
        pass


def print1(*args):
    print(args)


sw = SwitchParams()
sw.add_param(print1, "-1")
sw.add_param(print1, "-n", 1)

args = ["-1", "-n", "param", "-1", "b", "c"]

while len(args) > 0:
    nb = sw.check_param(args[0], args)
    if nb == 0:
        print("paramètre:", args[0])
        nb = 1
    else:
        print("Option trouvée:", ", ".join(map(str, args[0:nb])))
    for _ in range(nb):
        args.pop(0)

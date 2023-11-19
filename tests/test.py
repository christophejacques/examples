
class Point:
    def __init__(self, dest: str, dist: int = 0, depuis: str = ""):
        self.dest: str = dest
        self.dist: int = dist
        self.distFromBegin: int = 0
        self.depuis: str = ""
        self.checked: bool = False

    def comeFrom(self, depuis) -> None:
        self.checked = True
        self.distFromBegin = depuis.distFromBegin + self.dist
        self.depuis = depuis.dest

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.dest == other
        elif isinstance(other, Point):
            return self.dest == other.dest
        else:
            raise TypeError(f"Erreur de type: {other.__class__.__name__} au lieu de [str | Point]")

    def __repr__(self) -> str:
        if self.dist == 0:
            return self.dest
        else:
            return f"'{self.depuis} " + ">" * self.dist + f" {self.dest}' ({self.distFromBegin})"


class Liens:
    def __init__(self, liens: list[Point]):
        self.liens = liens
        self.distFromBegin: int = 0
        self.checked = False

    def __repr__(self) -> str:
        res: str = f"{self.liens[0]!r}"

        for p in self.liens[1:]:
            res += f", {p}"
        return res + "\n"


chemin: dict[str, Liens] = {
    'A': Liens([Point('B', 2), Point('D', 1)]),
    'B': Liens([Point('C', 2), Point('A', 1), Point('F', 1)]),
    'C': Liens([Point('B', 3), Point('E', 1), Point('F', 1)]),
    'D': Liens([Point('E', 1), Point('A', 1)]),
    'E': Liens([Point('C', 1), Point('D', 1)]),
    'F': Liens([Point('B', 1), Point('C', 1), Point('G', 1)]),
    'G': Liens([Point('F', 1)])
}

chemin2: dict[str, Liens] = {
    'A': Liens([Point('B', 4), Point('C', 1)]),
    'B': Liens([Point('A', 1), Point('C', 1), Point('D', 1)]),
    'C': Liens([Point('A', 1), Point('B', 1), Point('D', 4)]),
    'D': Liens([Point('B', 1), Point('C', 1)]),
}

DEBUG: bool = True

debut: Point = Point("A")
fin: Point = Point("G")
solution: list[Point] = []
cheminCourt: list[Point] = []
maximum: int = 9 ** 99


def ajoute(destination: Point) -> None:
    solution.append(destination)


def supprime() -> None:
    solution.pop()


def find_next(current: Point) -> list[Point]:
    global maximum
    global cheminCourt

    if current == fin:
        if maximum > current.distFromBegin:
            maximum = current.distFromBegin
        if DEBUG:
            print(f"[>{current.distFromBegin:>3} <]", end=" = ")
            print(solution)
        cheminCourt = solution.copy()
        return []

    for destination in chemin[current.dest].liens:
        if maximum >= current.distFromBegin + destination.dist and \
         (not destination.checked or current.distFromBegin + destination.dist < destination.distFromBegin):
            destination.comeFrom(current)
            ajoute(destination)
            find_next(destination)
            supprime()

    if not solution:
        return cheminCourt

    return []


print(debut, ">", fin, "=", find_next(debut))

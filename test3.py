class Commande_Result:

    def __init__(self) -> None:
        self.CONTENT: list[str] = []

    def clear(self) -> None:
        self.CONTENT.clear()

    def add_line(self, content: str) -> None:
        if isinstance(content, str):
            self.CONTENT.append(content)
        else:
            raise TypeError(f"Le parametre de la methode Commande_Result.add_line est '{content.__class__.__name__}' au lieu de 'str'.")

    def add_lines(self, content: list[str]) -> None:
        if isinstance(content, list):
            self.CONTENT.extend(content)    
        else:
            raise TypeError(f"Le parametre de la methode Commande_Result.add_lines est '{content.__class__.__name__}' au lieu de 'list[str]'.")

    def read_lines(self) -> list[str]:
        return self.CONTENT.copy()

    def pop(self) -> list[str]:
        result = self.read_lines()
        self.clear()
        return result

    def print(self) -> None:
        [print(ligne) for ligne in self.CONTENT]

    def grep(self, pattern: str, **options: bool) -> None:
        my_screen = self.pop()
        if options.get("ignore_case"):
            pattern = pattern.lower()
            self.add_lines([ligne for ligne in my_screen if pattern in ligne.lower()])
            return

        self.add_lines([ligne for ligne in my_screen if pattern in ligne])

    def head(self, nombre: int) -> None:
        self.CONTENT = self.CONTENT[:nombre]

    def tail(self, nombre: int) -> None:
        self.CONTENT = self.CONTENT[-nombre:]


def main():
    cr1 = Commande_Result()
    cr1.clear()
    cr1.add_line("1ere ligne")
    cr1.add_line("test 1")
    cr1.add_line("Test 1")
    cr1.add_line("tesT 1")

    cr2 = Commande_Result()
    cr2.add_lines(cr1.read_lines())
    cr2.add_line("2eme ligne")
    cr2.add_line("test 2")
    cr2.add_line("Test 2")
    cr2.add_line("tesT 2")

    cr2.grep("Test", ignore_case=True)
    cr2.head(4)
    cr2.tail(2)
    cr2.print()


if __name__ == "__main__":
    try:
        main()
    except Exception as erreur:
        print(erreur)

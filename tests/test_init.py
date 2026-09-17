from typing import Type, Any, List, Dict, Optional
from dataclasses import dataclass, field
from typing import LiteralString


@dataclass(frozen=True)
class ClasseMere:
    screen: LiteralString
    window: LiteralString


@dataclass
class UneClasse:
    args: List[Any]
    kwargs: Optional[Dict[str, Any]] = field(default_factory=Dict)

    def __str__(self):
        screen, window, args, kwargs = self.screen, self.window, self.args, self.kwargs
        return f"UneClasse({screen=}, {window=}, {args=}, {kwargs=})"


def initialise_classe(nom_classe: Type[Any], screen: str, window: str, 
        *args, **kwargs) -> Any:

    init_method = nom_classe.__init__
    nom_classe.__init__ = ClasseMere.__init__
    instance = nom_classe(screen, window)

    nom_classe.__init__ = init_method
    nom_classe.__init__(instance, args, kwargs)

    return instance


uc = initialise_classe(UneClasse, "screen", "window", 5, retry=False)
print(uc)

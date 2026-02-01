from __future__ import annotations

import json
from functools import wraps
from typing import Any, Callable, Optional


# ------------------------------------------------------------
# Generic Types
# ------------------------------------------------------------
type PredicateFn[T] = Callable[[T], bool]
type RuleDef = Callable[..., bool]
type PredicateFactory[T] = Callable[..., Predicate[T]]


# ------------------------------------------------------------
# Global Rule Registry
# ------------------------------------------------------------
RULES: dict[str, PredicateFactory[Any]] = {}


# ------------------------------------------------------------
# Predicate
# ------------------------------------------------------------
class Predicate[T]:
    """
    A composable predicate that supports &, |, and ~ operators.
    Wraps a function (T -> bool).
    """

    def __init__(self, fn: PredicateFn[T]):
        self.fn = fn

    def __call__(self, obj: T) -> bool:
        return self.fn(obj)

    def __and__(self, other: Predicate[T]) -> Predicate[T]:
        return Predicate(lambda x: self(x) and other(x))

    def __or__(self, other: Predicate[T]) -> Predicate[T]:
        return Predicate(lambda x: self(x) or other(x))

    def __invert__(self) -> Predicate[T]:
        return Predicate(lambda x: not self(x))

    def __str__(self) -> str:
        return self.fn.__name__


# ------------------------------------------------------------
# Decorators
# ------------------------------------------------------------
def predicate[T](fn: PredicateFn[T]) -> Predicate[T]:
    @wraps(fn)
    def wrapper(obj: T) -> bool:
        return fn(obj)

    return Predicate(wrapper)


def rule[T](fn: RuleDef) -> PredicateFactory[Any]:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Predicate[T]:
        return Predicate(lambda obj: fn(*args, obj, **kwargs))

    RULES[fn.__name__] = wrapper
    return wrapper


def eprint(*args, **kwargs):
    print(*args, **kwargs, end="")


# ------------------------------------------------------------
# Recursive Config Loader
# ------------------------------------------------------------
def decodage_regle(source: dict, operator: Optional[str]=None) -> Predicate[Any]:
    result: Optional[Predicate[Any]] = None
    first: bool = True

    if isinstance(source, dict):
        operator = source.get("operator")
        if operator:
            # gestion des operateurs
            if operator == "NOT":
                if result is None:
                    result = decodage_regle(source.get("components", []), operator)
                else:
                    raise Exception("Erreur", "NOT operateur non utilisable")

            elif operator == "AND":
                decode = decodage_regle(source.get("components", []), operator)
                if result is None:
                    result = decode
                else:
                    result = result & decode

            elif operator == "OR":
                decode = decodage_regle(source.get("components", []), operator)
                if result is None:
                    result = decode
                else:
                    result = result | decode

            else:
                raise Exception("Erreur", f"operateur inconnu {operator}")

        else:
            raise Exception("Erreur", "pas d'operateur")

    elif isinstance(source, list):

        for element in source:
            # gestion des fonctions
            fonc_name = element.get("fonction")
            if first:
                eprint("(")
                eprint("NOT " if operator == "NOT" else "")
                eprint(fonc_name)
            else:
                eprint("", operator, "" if fonc_name is None else fonc_name)

            if fonc_name is None:
                # c'est un operateur NOT, OR ou AND
                if operator == "NOT":
                    if not first:
                        raise Exception("il y a plus d'une expression pour NOT")

                    result = decodage_regle(source.get("components", []), operator)
                    print(result.fn)

                elif operator == "AND":
                    result = result & decodage_regle(element)
                elif operator == "OR":
                    result = result | decodage_regle(element)
                else:
                    raise Exception("Erreur", f"operateur inconnu {operator}")

            else:
                # c'est une fonction
                args = tuple(element.get("args",()))
                eprint(args)

                factory = RULES[fonc_name]
                fonction = factory(*args)

                if first:
                    if operator == "NOT":
                        result = ~ fonction
                    else:
                        result = fonction

                elif operator == "AND":
                    result = result & fonction
                elif operator == "OR":
                    result = result | fonction
                else:
                    raise Exception("Erreur", f"operateur inconnu {operator}")


            first = False

        eprint(")")

    else:
        raise Exception("Erreur", "type source inconnu")

    if result is None:
        raise Exception("Le resultat est None")

    return result


# ------------------------------------------------------------
# Recursive Config Loader
# ------------------------------------------------------------
def load_recursive_rule_from_config(path: str) -> Predicate[Any]:
    with open(path) as f:
        regles = json.load(f)

    return decodage_regle(regles)

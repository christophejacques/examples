from __future__ import annotations

import json
from functools import wraps
from typing import Any, Callable


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


# ------------------------------------------------------------
# Config Loader
# ------------------------------------------------------------
def load_rule_from_config(path: str) -> Predicate[Any]:
    """
    Load a rule from a JSON config file that looks like:
    The returned object is a composed Predicate[Any].
    """

    with open(path) as f:
        regles = json.load(f)

    preds: list[Predicate[Any]] = []
    resultat: Predicate[Any] 
    first_regle: bool = True
    first_cond: bool

    for regle in regles:
        preds.clear()
        first_cond = True

        logic = regle["logic"]
        if first_regle:
            print()
        else:
            print(logic)

        for cond in regle["conditions"]:
            name = cond["name"]
            args = cond.get("args", [])
            if first_cond:
                print("(", name, args)
            else:
                print(" ", logic, name, args)

            if name not in RULES:
                raise ValueError(f"Unknown rule: {name}")

            factory = RULES[name]
            predicate_obj = factory(*args)
            preds.append(predicate_obj)

            first_cond = False

        print(")")

        combined = preds[0]

        for p in preds[1:]:
            combined = (combined & p) if logic == "AND" else (combined | p)

        if first_regle:
            resultat = combined
        else:
            resultat = (resultat & combined) if logic == "AND" else (resultat | combined)

        first_regle = False

    return resultat

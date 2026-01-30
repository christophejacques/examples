from dataclasses import dataclass
from typing import Iterable

from rules import rule, load_recursive_rule_from_config, eprint

DEBUG: bool = False

@dataclass
class User:
    is_admin: bool
    is_active: bool
    account_age: int
    is_banned: bool
    country: str
    credit_score: int
    has_manual_override: bool


# ---------------------------------------------------------------------------
# BUSINESS RULES (SIMPLY USE @predicate)
# ---------------------------------------------------------------------------
@rule
def is_admin(u: User) -> bool:
    if DEBUG:
        eprint("is_admin", u.is_admin, ",")
    return u.is_admin


@rule
def is_active(u: User) -> bool:
    if DEBUG:
        eprint("is_active", u.is_active, ",")
    return u.is_active


@rule
def is_banned(u: User) -> bool:
    if DEBUG:
        eprint("is_banned", u.is_banned, ",")
    return u.is_banned


@rule
def has_override(u: User) -> bool:
    if DEBUG:
        eprint("has_override", u.has_manual_override, ",")
    return u.has_manual_override


@rule
def account_older_than(days: int, u: User) -> bool:
    if DEBUG:
        eprint("account_older_than", u.account_age > days, ",")
    return u.account_age > days


@rule
def from_country(countries: Iterable[str], u: User) -> bool:
    if DEBUG:
        eprint("from_country", u.country in countries, ",")
    return u.country in countries


@rule
def credit_score_above(threshold: int, u: User) -> bool:
    if DEBUG:
        eprint("credit_score_above", u.credit_score > threshold, ",")
    return u.credit_score > threshold


# ---------------------------------------------------------------------------
# BUILD RULE IN PYTHON DSL
# ---------------------------------------------------------------------------
api_check = is_admin() | (
    is_active()
    & account_older_than(30)
    & ~is_banned()
    & from_country(["NL", "BE"])
    & (credit_score_above(650) | has_override())
)

# ---------------------------------------------------------------------------
# EXAMPLE SYSTEM USAGE
# ---------------------------------------------------------------------------
def reporting(users: list[User]) -> list[User]:
    return [u for u in users if api_check(u)]


def cli_export(users: list[User]) -> list[User]:
    return [u for u in users if api_check(u)]


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------
def main() -> None:
    users = [
        User(True, False, 10, True, "US", 100, False),
        User(False, True, 40, False, "NL", 700, False),
        User(False, True, 40, False, "BE", 500, True),
        User(False, True, 10, False, "NL", 900, False),
        User(False, False, 60, False, "NL", 900, False),
        User(False, True, 60, True, "NL", 900, False),
    ]

    if True:
        print("=== Access via Python DSL ===")
        for u in users:
            print(u, "=>", api_check(u))

    # If rule_config.json exists, load dynamic rule:
    try:
        eprint("\n=== Access via Recursive Config Rule ===")
        print("\nrule = ", end="")
        recursive_rule = load_recursive_rule_from_config("rule_test.json")
        print("\n")
        for u in users:
            print(u, "=>", recursive_rule(u))

    except FileNotFoundError:
        print("\n(No rule_config.json found — skipping dynamic demo)")


if __name__ == "__main__":
    main()

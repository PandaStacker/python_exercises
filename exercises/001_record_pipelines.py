"""001 — Record pipelines

Real programs rarely transform one perfect value at a time. They receive a
collection of imperfect records, normalize each record, discard unwanted
ones, and build indexes or summaries from the result.

Work in stages here. A comprehension is useful when it stays readable, but a
plain loop is often clearer when normalization has several steps. Never mutate
caller-owned dictionaries or lists unless the contract explicitly says to.

Implement all three functions. Together they form one small data pipeline; the
output of `normalize_users` is valid input to the other two functions.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any


# There is another way of doing this now, with an @ tag, funny that the AI doesn't
# touch it.
# No there isn't, because ABC and the @abstractmethod tag is only for classes. Well,
# there might be, but this isn't it.

# TODO conceive what a computer which can really embrace its GPU does with this. Because
# all of these are tasks you can run in parallel, none of the data depends on mutations of
# other data. Just give a GPU chunks and it can blast millions of columns in seconds.
def normalize_users(records: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return new, normalized dictionaries for active users.

    Each input has `name` and `email`, and may have `active` and `tags`.
    Ignore a record only when `active` is exactly False. Strip the name; strip
    and lowercase the email. Strip/lowercase tags, remove blanks and duplicates,
    and sort them. Results contain exactly name, email, and tags. Do not mutate.
    """

    r_list = []
    for record in records:
        r_dict = {}
        if "active" in record:
            if record["active"] == False:
                continue
        r_dict["name"] = record["name"].strip()
        r_dict["email"] = record["email"].strip().lower()
        for tag in record["tags"]:
            if not tag:
                continue
            if tag in r_dict["tags"]:
                continue

            r_dict["tags"].append(tag.strip().lower())

        r_list.append(r_dict)

    return r_list


def index_by_email(users: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    """Index original mappings, rejecting duplicates with
    `ValueError("duplicate email: <email>")`.
    """
    # email, info by name?
    r_dict = {}

    # users will have email and other info, which goes into Any
    for user in users:
        email = user["email"]
        if email in r_dict:
            raise ValueError(f"duplicate email: <{email}>")

        r_dict[email] = user # how do we either indicate the rest or...? Just point it to the whole thing? It is the same type

    return r_dict

def count_tags(users: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """Count users per tag and return keys in alphabetical insertion order."""
    raise NotImplementedError


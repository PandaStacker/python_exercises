"""001_RecordPipelines 

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
import traceback


# There is another way of doing this now, with an @ tag, funny that the AI doesn't
# touch it.
# No there isn't, because ABC and the @abstractmethod tag is only for classes. Well,
# there might be, but this isn't it.

# TODO how do we give this to the GPU in Python? Would we have to just write  compute
# shader? A shame, if so, easily chunkable to a GPU.
def normalize_users(records: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Return new, normalized dictionaries for active users.

    Each input has `name` and `email`, and may have `active` and `tags`.
    Ignore a record only when `active` is exactly False. Strip the name; strip
    and lowercase the email. Strip/lowercase tags, remove blanks and duplicates,
    and sort them. Results contain exactly name, email, and tags. Do not mutate.
    """

    r_list = []
    for record in records:
        if not record.get("active", True):
            continue

        r_dict = {
            "name": record["name"].strip(),
            "email": record["email"].strip().lower()
        }

        if "tags" in record:
            r_dict["tags"] = [tag.strip().lower() for tag in record["tags"]]

        """ old way:
        if "tags" in record:
            for tag in record["tags"]:
                if "tags" not in r_dict:
                    r_dict["tags"] = [tag.strip().lower()]
                else:
                    r_dict["tags"].append(tag.strip().lower())
        """

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

        r_dict[email] = user # how do we either indicate the rest or...?
        # Just point it to the whole thing? It is the same type
        # it's supposed to be a mapping, so yes, just the whole thing

    return r_dict

def count_tags(users: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """Count users per tag and return keys in alphabetical insertion order.
    note: how do we return them in alphabetical insertion order in a dict?
    Maybe AI does suck at this."""
    # okay so create the dict of tags and counts, increment each count when we find a tag,
    # that tag finding process is basically automated by the dict
    return_dict = {}
    for user in users:
        for tag in user["tags"]:
            if tag in return_dict:
                return_dict[tag] += 1
            else:
                return_dict[tag] = 1

    return return_dict

if __name__ == "__main__":
    test_records = [
        {"name": " Alice ", "email": "ALICE@example.com", "active": True, "tags": ["admin", " user", ""]},
        {"name": " Bob", "email": "bob@example.com", "active": False, "tags": ["guest"]},
        {"name": "Charlie ", "email": "CHARLIE@example.com", "tags": ["admin", "staff"]}
    ]

    print("--- Testing normalize_users ---")
    try:
        normalized = normalize_users(test_records)
        for u in normalized:
            print(u)
    except Exception as e:
        print(f"normalize_users raised an error: {e!r}")
        traceback.print_exc()

    print("\n--- Testing index_by_email ---")
    try:
        # Using a clean list of dicts that we know works since normalize_users might error out
        clean_records = [
            {"name": "Alice", "email": "alice@example.com", "tags": ["admin"]},
            {"name": "Charlie", "email": "charlie@example.com", "tags": ["admin", "staff"]}
        ]
        indexed = index_by_email(clean_records)
        for email, u in indexed.items():
            print(f"{email}: {u}")
    except Exception as e:
        print(f"index_by_email raised an error: {e!r}")

    print("\n--- Testing count_tags ---")
    try:
        counts = count_tags(clean_records)
        for t, count in counts.items():
            print(f"{t}: {count}")
    except Exception as e:
        print(f"count_tags raised an error: {e!r}")

"""002_loop_toolbox

`for` visits values from any iterable; it is not limited to lists or numeric
indexes. Python supplies tools that keep common loop jobs direct:

    for number, item in enumerate(items, start=1):  # index and value
    for left, right in zip(xs, ys, strict=True):    # aligned iterables
    for key, value in mapping.items():              # mapping pairs
    for start in range(0, len(values), size):       # numeric positions
    # we're going to use this last one all the time in leetcode

Loops compose: a nested loop visits values inside values. `continue` skips to
the next iteration, while `break` ends the nearest loop. A `for` loop's `else`
runs only when iteration finishes without `break`, which helps a search that
found nothing. Use `while` when repetition ends because state changes, such as
following pagination tokens until there is no next token.

Each function deliberately targets one construct. Tests inspect a few bodies
as well as results because the point is to practice the loop forms.

A note on `Callable` (used in type hints below):
`Callable` means "a function" (or any object that can be called). In type hints 
like `Callable[[ArgType], ReturnType]`, the first part in brackets specifies 
the types of arguments the function accepts, and the second part specifies 
what it returns. It simply means you are passing a function as an argument.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any

# you can define the start IN the definition, interesting specificity.
# Does python throw an error if we pass in something else? No, but will
# complain at all?
def numbered_names(users: Iterable[Mapping[str, Any]], start: int = 1) -> list[str]:
    """Use `enumerate(..., start=start)` to return labels like `1. Ada`."""
    return_list = []
    for index, user in enumerate(users, start=1):
        return_list.append(f"{index}. {user}")

    return return_list


def attach_scores(users: Iterable[Mapping[str, Any]], scores: Iterable[int]) -> list[dict[str, Any]]:
    """Pair with `zip(..., strict=True)` and return copied users with scores."""
    return_list = []
    for left, right in zip(users, scores, strict=True):
        return_list.append({left, right})

    return return_list


def first_user_with_tag(users: Iterable[Mapping[str, Any]], tag: str) -> Mapping[str, Any] | None:
    """Find the first matching normalized tag using `break` and `for ... else`."""
    for user in users:
        if tag in user.tags:
            return user

    return None


def process_users_in_chunks(users: Sequence[Mapping[str, Any]], size: int) -> list[list[Mapping[str, Any]]]:
    """Chunk with `range` and slicing; require size > 0 with a clear ValueError.
    
    Elaboration: Breaking a large list into smaller "chunks" is common even without
    multithreading. For example, if you have 10,000 users and need to send them to
    an API that only accepts 100 users per request, you chunk the list into batches
    of 100 before looping through those batches to make the API requests.
    """
    # TODO:
    # 1. Validate input: if size <= 0, raise ValueError.
    # 2. Use a for loop with `range(0, len(users), size)` to get start indices.
    # 3. Use list slicing `users[start:start+size]` to extract each chunk.
    # 4. Return the list of chunks

    raise NotImplementedError


def collect_pages(fetch_page: Callable[[str | None], tuple[Iterable[Mapping[str, Any]], str | None]]) -> list[Mapping[str, Any]]:
    """Use `while` to fetch from token None through a page returning next None.
    
    Elaboration: APIs often return large datasets in "pages" (e.g., 50 records at a time)
    to avoid overwhelming the server or network. Along with the records, the API returns
    a "pagination token" that acts as a bookmark. To get all the data, you must repeatedly
    call the API, passing the previous bookmark each time, until the API returns a None
    token, indicating there are no more pages.
    """
    # TODO:
    # 1. Initialize an empty list for collected users and a token variable (starting as None).
    # 2. Use a while loop that continues as long as you still have a token to fetch (or for the very first fetch).
    # 3. Inside the loop, call fetch_page(token) to get the page's users and the new next token.
    # 4. Add the users to your total list.
    # 5. Update the token variable with the new next token. The loop ends when the returned token is None.
    # 6. Return the total list of users.
    raise NotImplementedError


def active_names(records: Iterable[Mapping[str, Any]]) -> list[str]:
    """Use `continue` to skip only records whose active value is exactly False."""
    return_list = []
    for record in records:
        if record.active is False:
            continue
        else:
            return_list.append(record)

    return return_list



def count_nested_tags(users: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """Count tags with nested loops; rebuild via sorted(counts.items()).
    
    Elaboration: The "nested" part refers to the loops, not the tags themselves. 
    Each user has a single flat list of tags (e.g., {"tags": ["admin", "user"]}). 
    To count all tags across all users, you need a loop to iterate through the users, 
    and a *nested* (inner) loop to iterate through the tags of each user.
    """
    # TODO:
    # 1. Initialize a dictionary to keep tag counts.
    # 2. Outer loop: iterate over each `user` in `users`.
    # 3. Inner loop: iterate over each `tag` in `user["tags"]`.
    # 4. Increment the count for the current tag in your dictionary.
    # 5. Build and return a new dictionary from the alphabetically sorted items: dict(sorted(counts.items())).
    raise NotImplementedError


if __name__ == "__main__":
    sample_users = [
        {"name": "Alice", "active": True, "tags": ["admin", "user"]},
        {"name": "Bob", "active": False, "tags": ["guest"]},
        {"name": "Bob", "active": True, "tags": ["guest"]},
        {"name": "Charlie", "active": True, "tags": ["user"]},
        {"name": "Simon", "active": False, "tags": ["user", "1"]},
        {"name": "Bella", "active": True, "tags": ["user", "2"]},
        {"name": "Catherine", "active": True, "tags": ["user", "3"]},
        {"name": "Cathy", "active": True, "tags": ["user", "2"]},
        {"name": "Bobby", "active": True, "tags": ["guest"]},
    ]

    print("--- Testing numbered_names ---")
    try:
        print(numbered_names(sample_users, start=1))
    except Exception as e:
        print(f"Error: {e!r}")

    print("\n--- Testing attach_scores ---")
    try:
        print(attach_scores(sample_users, [100, 85, 95]))
    except Exception as e:
        print(f"Error: {e!r}")

    print("\n--- Testing first_user_with_tag ---")

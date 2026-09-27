"""022 — Validation and serialization with Pydantic

Pydantic models turn untrusted dictionaries or JSON into typed objects.
Annotations describe output types, `Field` adds constraints, field validators
normalize or reject one field, and model validators enforce relationships
between fields.  Nested models compose validation and produce useful error
locations automatically.

This exercise targets Pydantic 2: use `field_validator`, `model_validator`,
`model_dump`, and `TypeAdapter`.  Validators must return the accepted value (or
the model itself).  Password fields are accepted for validation but excluded
from serialization.
"""
from __future__ import annotations

import re
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, computed_field
from pydantic import field_validator, model_validator


class Address(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str

    @field_validator("postal_code")
    @classmethod
    def normalize_postal_code(cls, value: str) -> str:
        """Accept Canadian `A1A 1A1` with optional middle space.

        Remove spaces, uppercase, validate the alternating letter/digit shape,
        and return it with exactly one middle space.  Raise
        `ValueError("invalid postal code")` for invalid input.
        """
        raise NotImplementedError


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-z0-9_]+$")
    password: str = Field(min_length=8, exclude=True)
    password_repeat: str = Field(min_length=8, exclude=True)
    tags: list[str] = Field(default_factory=list)
    address: Address | None = None

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: Any) -> Any:
        """Strip and lowercase strings; return other values for normal validation."""
        raise NotImplementedError

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, value: Any) -> Any:
        """Allow either a list or one comma-separated string.

        For a string, split on commas.  Normalize list items by stripping and
        lowercasing, remove blanks and duplicates while preserving order.
        Raise `ValueError("tags must be strings")` if any item is not a string.
        """
        raise NotImplementedError

    @model_validator(mode="after")
    def passwords_match(self) -> Self:
        """Raise `ValueError("passwords do not match")` or return self."""
        raise NotImplementedError

    @computed_field
    @property
    def profile_slug(self) -> str:
        """Return `username` followed by the normalized postal code without space.

        When address is absent, use `remote`: for example `ada-a1a1a1` or
        `ada-remote`.
        """
        raise NotImplementedError


REGISTRATION_LIST = TypeAdapter(list[Registration])


def parse_registrations_json(text: str) -> list[Registration]:
    """Validate a JSON array through REGISTRATION_LIST.validate_json."""
    raise NotImplementedError


if __name__ == "__main__":
    print("--- Testing pydantic models ---")
    try:
        reg = Registration(username="user123", password="password1", password_repeat="password1")
        print("Registration dump:", reg.model_dump())
    except Exception as e:
        print(f"Error: {e!r}")

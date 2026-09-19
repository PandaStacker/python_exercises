"""013 — Enums and structural pattern matching

Enums give a closed vocabulary of meaningful values.  Dataclasses give parsed
commands an explicit shape.  Structural `match` then dispatches on those
shapes; guards handle conditions that patterns alone cannot express.

Keep parsing separate from execution.  The parser turns untrusted strings into
validated command objects.  The executor only accepts those objects and can
therefore focus on state transitions.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    @property
    def vector(self) -> tuple[int, int]:
        """Map north/east/south/west to (0,1)/(1,0)/(0,-1)/(-1,0)."""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Move:
    direction: Direction
    distance: int


@dataclass(frozen=True, slots=True)
class Say:
    text: str


@dataclass(frozen=True, slots=True)
class Quit:
    pass


Command = Move | Say | Quit


def parse_command(text: str) -> Command:
    """Parse a case-insensitive command after stripping/splitting whitespace.

    Accepted forms are `move DIRECTION DISTANCE`, `say ANY NON-BLANK TEXT`, and
    `quit`.  A move distance must be an integer greater than zero.  Preserve
    the say text's words joined by single spaces, but not its original spacing.
    Raise `ValueError("invalid command: <original text>")` for everything else.
    Use matching to distinguish token shapes.
    """
    raise NotImplementedError


def execute(position: tuple[int, int], command: Command) -> tuple[tuple[int, int], str | None]:
    """Apply a command using class patterns.

    Move returns the translated position and `None`.  Say keeps the position
    and returns its text.  Quit keeps the position and returns `"quit"`.
    """
    raise NotImplementedError


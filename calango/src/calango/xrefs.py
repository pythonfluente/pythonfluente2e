from enum import Enum, auto
from dataclasses import dataclass


class Kind(Enum):
    PART = auto()
    CHAPTER = auto()
    SECTION = auto()
    EXAMPLE = auto()
    TABLE = auto()


@dataclass
class Target:
    ident: str
    vol: int = 0
    chap: int = 0
    numbers: tuple[int, ...] | None = None
    kind: Kind = Kind.PART

    def __post_init__(self):
        self.kind = self.get_kind()

    def get_kind(self) -> Kind:
        if self.ident.startswith('ch_'):
            return Kind.CHAPTER
        raise ValueError(f'Kind of {self.ident!r} is unknown')


def validate(xref):
    return any([
        xref.startswith('ch_'),
        xref.endswith('_ex'),
        xref.endswith('_sec'),
        xref.endswith('_part'),
        xref.endswith('_tbl'),
    ])
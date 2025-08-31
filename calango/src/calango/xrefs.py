import xml.etree.ElementTree as ET
from enum import Enum, auto
from dataclasses import dataclass
from bs4 import BeautifulSoup


class Kind(Enum):
    PART = auto()
    CHAPTER = auto()
    SECTION = auto()
    EXAMPLE = auto()
    TABLE = auto()


@dataclass
class Target:
    ident: str
    numbers: tuple[int, ...] = ()
    kind: Kind = Kind.PART

    def __post_init__(self):
        self.kind = self.get_kind()
        if self.kind is not Kind.CHAPTER:
            return
        self.numbers = (self.chapter, )

    @property
    def volume(self) -> int:
        return (self.chapter - 1) // 8 + 1

    @property
    def chapter(self) -> int:
        return CHAPTER_NUMBER[self.ident]

    def get_kind(self) -> Kind:
        if self.ident.startswith('ch_'):
            return Kind.CHAPTER
        elif self.ident.endswith('_sec'):
            return Kind.SECTION
        raise ValueError(f'Kind of {self.ident!r} is unknown')

    def get_section_title(self, root: BeautifulSoup) -> str:
        element = root.find(id=self.ident)    
        if element:
            return element.get_text(strip=True)
        raise LookupError(f'element {self.ident} not found')

        


def validate(xref):
    return any([
        xref.startswith('ch_'),
        xref.endswith('_ex'),
        xref.endswith('_sec'),
        xref.endswith('_part'),
        xref.endswith('_tbl'),
    ])

CHAPTER_ID = {
    1 : 'ch_data_model',
    2 : 'ch_sequences',
    3 : 'ch_dicts_sets',
    4 : 'ch_str_bytes',
    5 : 'ch_dataclass',
    6 : 'ch_refs_mut_mem',
    7 : 'ch_func_objects',
    8 : 'ch_type_hints_def',
    9 : 'ch_closure_decorator',
    10 : 'ch_design_patterns',
    11 : 'ch_pythonic_obj',
    12 : 'ch_seq_methods',
    13 : 'ch_ifaces_prot_abc',
    14 : 'ch_inheritance',
    15 : 'ch_more_types',
    16 : 'ch_op_overload',
    17 : 'ch_generators',
    18 : 'ch_with_match',
    19 : 'ch_concurrency_models',
    20 : 'ch_executors',
    21 : 'ch_async',
    22 : 'ch_dynamic_attrs',
    23 : 'ch_descriptors',
    24 : 'ch_class_metaprog',
}

CHAPTER_NUMBER = {i:n for (n, i) in CHAPTER_ID.items()}


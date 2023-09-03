from dataclasses import dataclass
from typing import List


@dataclass
class SrlArgument:
    word: str
    start_idx: int
    end_idx: int
    label: str


@dataclass
class SrlPredicate:
    word: str
    start_idx: int
    end_idx: int


@dataclass
class SrlData:
    sentence: str
    arguments: List[SrlArgument]
    predicate: SrlPredicate
    labels: List[str]


@dataclass
class SrlOutputs:
    data: List[SrlData]
    size: int = 0

    def __post_init__(self):
        self.size = len(self.data)

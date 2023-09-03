from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class NerEntity:
    word: str
    label: str
    start_idx: int
    end_idx: int


@dataclass
class NerData:
    sentence: str
    entities: List[NerEntity]


@dataclass
class NerOutputs:
    data: List[NerData]
    size: int = 0

    def __post_init__(self):
        self.size = len(self.data)

    def __add__(self, others: NerOutputs) -> NerOutputs:
        return NerOutputs(data=self.data + others.data)

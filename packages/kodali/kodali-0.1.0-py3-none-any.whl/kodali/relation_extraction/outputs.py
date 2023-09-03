from dataclasses import dataclass
from typing import List


@dataclass
class ReEntity:
    word: str
    start_idx: int
    end_idx: int
    label: str


@dataclass
class ReData:
    sentence: str
    subject: ReEntity
    object: ReEntity
    label: str


@dataclass
class ReOutputs:
    data: List[ReData]
    size: int = 0

    def __post_init__(self):
        self.size = len(self.data)

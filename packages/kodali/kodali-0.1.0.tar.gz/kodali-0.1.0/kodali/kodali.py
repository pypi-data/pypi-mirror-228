from typing import Union

from kodali.named_entity_recognition.loader import NerLoader
from kodali.named_entity_recognition.outputs import NerOutputs


class Kodali:
    def __new__(cls, path: str, task: str, source: str) -> NerOutputs:
        if task == "ner":
            return NerLoader(path=path, source=source)
        else:
            raise ValueError("Unsupported task. 'ner', 're', 'srl' tasks are currently supported.")

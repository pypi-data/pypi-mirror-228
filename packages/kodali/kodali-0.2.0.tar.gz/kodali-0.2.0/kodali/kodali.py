from typing import Union

from kodali.named_entity_recognition.loader import NerLoader
from kodali.named_entity_recognition.outputs import NerOutputs
from kodali.relation_extraction.loader import ReLoader
from kodali.relation_extraction.outputs import ReOutputs


class Kodali:
    def __new__(cls, path: str, task: str, source: str) -> Union[NerOutputs, ReOutputs]:
        if task == "ner":
            return NerLoader(path=path, source=source)
        elif task == "re":
            return ReLoader(path=path, source=source)
        else:
            raise ValueError("Unsupported task. 'ner', 're' tasks are currently supported.")

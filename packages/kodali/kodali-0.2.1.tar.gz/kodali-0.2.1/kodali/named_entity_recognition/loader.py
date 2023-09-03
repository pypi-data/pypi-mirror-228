from kodali.named_entity_recognition.klue import load_klue_ner
from kodali.named_entity_recognition.korean_corpus import load_korean_corpus_ner
from kodali.named_entity_recognition.outputs import NerOutputs


class NerLoader:
    def __new__(cls, path: str, source: str) -> NerOutputs:
        if source == "korean-corpus":
            dataset = load_korean_corpus_ner(path=path)
        elif source == "klue":
            dataset = load_klue_ner(path=path)
        else:
            raise ValueError("Unsupported data source. 'korean-corpus', 'KLUE' tasks are currently implemented.")

        return dataset

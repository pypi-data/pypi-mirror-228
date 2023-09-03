from typing import List

from kodali.named_entity_recognition.outputs import NerData, NerEntity, NerOutputs
from kodali.named_entity_recognition.scheme import NerTags
from kodali.utils.io import load_txt


def __convert_to_entities(sentence: str, labels: List[str]) -> List[NerEntity]:
    entities = []
    buffer = {}

    for idx, label in enumerate(labels):
        if label.startswith(str(NerTags.BEGIN)):
            buffer = {
                "idx": idx,
                "label": label.replace(f"{str(NerTags.BEGIN)}-", ""),
            }
        elif label == str(NerTags.OUTSIDE):
            if buffer:
                start_idx = buffer["idx"]
                label = buffer["label"]

                # Single
                word = sentence[start_idx] if start_idx + 1 == idx else sentence[start_idx:idx]

                entities.append(
                    NerEntity(
                        word=word,
                        label=label,
                        start_idx=start_idx,
                        end_idx=idx,
                    )
                )
                buffer = {}

    return entities


def load_klue_ner(path: str) -> NerOutputs:
    dataset = []

    buffer = load_txt(path=path)
    char_buffer = []
    label_buffer = []

    for b in buffer:
        if b.startswith("##"):
            continue

        if not b:
            sentence = "".join(char_buffer)

            dataset.append(
                NerData(
                    sentence=sentence,
                    entities=__convert_to_entities(sentence=sentence, labels=label_buffer),
                )
            )

            char_buffer = []
            label_buffer = []
            continue

        char, label = b.split("\t")
        char_buffer.append(char)
        label_buffer.append(label)

    return NerOutputs(data=dataset)

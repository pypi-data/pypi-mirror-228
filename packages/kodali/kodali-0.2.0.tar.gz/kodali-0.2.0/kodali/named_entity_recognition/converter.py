from typing import List

from kodali.named_entity_recognition.outputs import NerData
from kodali.named_entity_recognition.scheme import NerTags


def __format(tag: NerTags, label: str) -> str:
    return f"{str(tag)}-{label}"


def to_bioes_scheme(data: NerData) -> List[str]:
    sentence = data.sentence
    entities = data.entities

    labels = [str(NerTags.OUTSIDE)] * len(sentence)

    for entity in entities:
        label = entity.label
        start_idx = entity.start_idx
        end_idx = entity.end_idx

        # Single Character
        if start_idx == end_idx - 1:
            labels[start_idx] = __format(tag=NerTags.SINGLE, label=label)
        # Multiple Character
        else:
            for idx in range(start_idx, end_idx):
                if idx == start_idx:
                    labels[idx] = __format(tag=NerTags.BEGIN, label=label)
                elif idx + 1 == end_idx:
                    labels[idx] = __format(tag=NerTags.END, label=label)
                else:
                    labels[idx] = __format(tag=NerTags.INSIDE, label=label)

    return labels

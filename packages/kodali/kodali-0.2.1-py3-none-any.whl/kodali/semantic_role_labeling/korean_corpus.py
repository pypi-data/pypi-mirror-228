import json
import os
from typing import List

from tqdm import tqdm

from kodali.semantic_role_labeling.outputs import (
    SrlArgument,
    SrlData,
    SrlOutputs,
    SrlPredicate,
)
from kodali.semantic_role_labeling.scheme import SrlTags


def __convert_to_char_labels(srl_list: list, len_sentence: int) -> List[str]:
    labels = [str(SrlTags.OUTSIDE)] * len_sentence

    for srl in srl_list:
        label = srl["label"]
        begin_idx = srl["begin"]
        end_idx = srl["end"]

        # Single Character
        if begin_idx == end_idx + 1:
            labels[begin_idx] = f"{str(SrlTags.SINGLE)}-{label}"
        # Multiple Character
        else:
            for idx in range(begin_idx, end_idx):
                if idx == begin_idx:
                    labels[idx] = f"{str(SrlTags.BEGIN)}-{label}"
                elif idx + 1 == end_idx:
                    labels[idx] = f"{str(SrlTags.END)}-{label}"
                else:
                    labels[idx] = f"{str(SrlTags.INSIDE)}-{label}"

    return labels


def load_korean_corpus_srl(path: str) -> SrlOutputs:
    dataset = []
    file_list = [file for file in os.listdir(path=path) if file.endswith(".json")]

    progress_bar = tqdm(file_list)
    for file in progress_bar:
        progress_bar.set_description(f"Read {file}")

        with open(os.path.join(path, file), "r", encoding="utf-8") as fp:
            data = json.load(fp)

        # 문장 경로
        # document[list] -> sentence[list] -> form[str]
        # Label 경로
        # document[list] -> sentence[list] -> SRL[list]
        for document in data["document"]:
            for sentence in document["sentence"]:
                form = sentence["form"]
                srl_list = sentence["SRL"]

                if not srl_list:
                    continue

                for srl in srl_list:
                    predicate = srl["predicate"]
                    predicate["label"] = "PREDICATE"

                    arguments = srl["argument"]

                    dataset.append(
                        SrlData(
                            sentence=form,
                            arguments=[
                                SrlArgument(
                                    word=argument["form"],
                                    start_idx=argument["begin"],
                                    end_idx=argument["end"],
                                    label=argument["label"],
                                )
                                for argument in arguments
                            ],
                            predicate=SrlPredicate(
                                word=predicate["form"],
                                start_idx=predicate["begin"],
                                end_idx=predicate["end"],
                            ),
                            labels=__convert_to_char_labels(
                                srl_list=predicate + arguments,
                                len_sentence=len(form),
                            ),
                        )
                    )

    return SrlOutputs(data=dataset)

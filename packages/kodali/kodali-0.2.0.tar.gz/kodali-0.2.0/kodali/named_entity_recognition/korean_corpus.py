import json
import os
from typing import List

from tqdm import tqdm

from kodali.named_entity_recognition.outputs import NerData, NerEntity, NerOutputs


def load_korean_corpus_ner(path: str) -> NerOutputs:
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
        # document[list] -> sentence[list] -> NE[list]
        for document in data["document"]:
            for sentence in document["sentence"]:
                form = sentence["form"]
                ne_list = sentence["NE"]

                if not ne_list:
                    continue

                dataset.append(
                    NerData(
                        sentence=form,
                        entities=[
                            NerEntity(
                                word=ne["form"],
                                label=ne["label"],
                                start_idx=ne["begin"],
                                end_idx=ne["end"],
                            )
                            for ne in ne_list
                        ],
                    )
                )

    return NerOutputs(data=dataset)

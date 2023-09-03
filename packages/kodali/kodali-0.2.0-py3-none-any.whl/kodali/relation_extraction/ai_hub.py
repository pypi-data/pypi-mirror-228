import os
from typing import List

from tqdm import tqdm

from kodali.relation_extraction.outputs import ReData, ReEntity, ReOutputs
from kodali.utils.io import load_json


def load_ai_hub_re(path: str) -> ReOutputs:
    dataset = []
    directories = [d for d in os.listdir(path) if not d.endswith(".zip")]

    for dir in directories:
        dir_path = os.path.join(path, dir)
        file_list = [f for f in os.listdir(dir_path) if f.endswith(".json")]

        progress_bar = tqdm(directories)
        for file in file_list:
            progress_bar.set_description(desc=f"{file}")

            file_path = os.path.join(dir_path, file)

            buffer = load_json(path=file_path)

            for b in buffer:
                dataset.append(
                    ReData(
                        sentence=b["sentence"],
                        subject=ReEntity(
                            word=b["subj_word"],
                            start_idx=b["subj_start"],
                            end_idx=b["subj_end"],
                            label=b["subj_prop"],
                        ),
                        object=ReEntity(
                            word=b["obj_word"],
                            start_idx=b["obj_start"],
                            end_idx=b["obj_end"],
                            label=b["obj_prop"],
                        ),
                        label=b["relation"],
                    )
                )

    return ReOutputs(data=dataset)

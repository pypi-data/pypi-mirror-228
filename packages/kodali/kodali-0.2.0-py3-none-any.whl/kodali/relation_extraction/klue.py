from kodali.relation_extraction.outputs import ReData, ReEntity, ReOutputs
from kodali.utils.io import load_json


def load_klue_re(path: str) -> ReOutputs:
    dataset = []

    buffer = load_json(path=path)

    for b in buffer:
        dataset.append(
            ReData(
                sentence=b["sentence"],
                subject=ReEntity(
                    word=b["subject_entity"]["word"],
                    start_idx=b["subject_entity"]["start_idx"],
                    end_idx=b["subject_entity"]["end_idx"],
                    label=b["subject_entity"]["type"],
                ),
                object=ReEntity(
                    word=b["object_entity"]["word"],
                    start_idx=b["object_entity"]["start_idx"],
                    end_idx=b["object_entity"]["end_idx"],
                    label=b["object_entity"]["type"],
                ),
                label=b["label"],
            )
        )

    return ReOutputs(data=dataset)

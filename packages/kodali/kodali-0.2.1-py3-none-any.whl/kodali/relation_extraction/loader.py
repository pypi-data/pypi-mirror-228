from kodali.relation_extraction.ai_hub import load_ai_hub_re
from kodali.relation_extraction.klue import load_klue_re
from kodali.relation_extraction.outputs import ReOutputs


class ReLoader:
    def __new__(cls, path: str, source: str) -> ReOutputs:
        if source == "ai-hub":
            dataset = load_ai_hub_re(path=path)
        elif source == "klue":
            dataset = load_klue_re(path=path)
        else:
            raise ValueError("Unsupported data source. 'ai-hub', 'KLUE' tasks are currently implemented.")

        return dataset

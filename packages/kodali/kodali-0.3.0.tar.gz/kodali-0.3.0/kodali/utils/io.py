import json
from typing import Any, Dict, List


def load_json(path: str) -> Dict[Any, Any]:
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


def load_txt(path: str) -> List[str]:
    buffer = []
    with open(path, "r", encoding="utf-8") as fp:
        for line in fp.readlines():
            line = line.replace("\n", "")

            buffer.append(line)

    return buffer

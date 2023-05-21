from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AlgorithmState:
    solution: List[int]
    info: str = ""

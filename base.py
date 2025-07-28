from dataclasses import dataclass
from typing import List

@dataclass
class Generator:
    id: int
    pmin: int
    pmax: int

Generators = List[Generator]
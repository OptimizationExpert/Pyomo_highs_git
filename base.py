from dataclasses import dataclass
from typing import List

@dataclass
class Generator:
    id: int
    pmin: int
    pmax: int
    def __hash__(self) -> int:
        return self.id.__hash__()

Generators = List[Generator]
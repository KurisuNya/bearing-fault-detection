from dataclasses import dataclass
from matplotlib.figure import Figure


@dataclass
class AlgorithmData:
    cfg: dict
    data: dict


@dataclass
class AlgorithmResult:
    figure_map: dict[str, Figure]
    text: str

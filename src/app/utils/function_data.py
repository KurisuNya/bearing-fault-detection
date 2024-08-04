from dataclasses import dataclass, field
from typing import Callable


@dataclass
class FuncData:
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

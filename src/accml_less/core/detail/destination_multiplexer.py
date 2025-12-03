from typing import Sequence

from ..interface.combined_views import StandardViews
from ..interface.destination_multiplexer import DestinationMultiplexerBase


class DestinationMultiplexer(DestinationMultiplexerBase):
    def __init__(self, *, target_names: Sequence[str]):
        self.target_names = target_names
        self.target_name = self.target_names[0]

    def __repr__(self):
        return f"{self.__class__.__name__}(target={self.target_name})"

    def set_target(self, target_name: str):
        assert target_name in self.target_names, f"Unknown target_name {target_name}. Known are {self.target_names}"
        self.target_name = StandardViews(target_name).value

    def get_target_name(self) -> str:
        return self.target_name
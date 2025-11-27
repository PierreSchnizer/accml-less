from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Sequence

from .view import View


class StandardViews(Enum):
    design = "design"
    device = "device"


class CombinedViews(metaclass=ABCMeta):
    @abstractmethod
    def get(self, view: str) -> View:
        """get a view.

        Todo:
            analyse if more than the standard views are needed
        """
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def get_view_names(self) -> Sequence[str]:
        raise NotImplementedError("use derived class instead")

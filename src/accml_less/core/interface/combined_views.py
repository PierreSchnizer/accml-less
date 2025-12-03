from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Sequence, Union

from .device_view_facade import DeviceViewRWFacadeBase, DeviceViewRFacadeBase
from .view import ViewR, ViewRW


class StandardViews(Enum):
    design = "design"
    device = "device"


class CombinedViewsBase(metaclass=ABCMeta):
    """
    Todo:
        reduce the number of types get returns or
        make it more Liskov like
    """

    @abstractmethod
    def get(
        self, view: str
    ) -> Union[ViewR, ViewRW, DeviceViewRFacadeBase, DeviceViewRWFacadeBase]:
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

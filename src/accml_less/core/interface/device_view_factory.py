from abc import abstractmethod, ABCMeta
from typing import Union, Sequence

from .device_view_facade import DeviceViewRFacadeBase, DeviceViewRWFacadeBase


class DeviceViewFactoryBase(metaclass=ABCMeta):
    """
    Todo:
      Is the list of known or possible devices necessary?

    Current Idea: show user which ones have been instaniated by
    the factory
    """

    @abstractmethod
    def get(
        self, dev_name: str
    ) -> Union[DeviceViewRFacadeBase, DeviceViewRWFacadeBase]:
        """Returns a  "managed" device view."""
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def get_managed_device_names(self) -> Sequence[str]:
        """Returns the names of the managed devices

        Main intend: provide facility for user to see which
        devices are managed by this object
        """

    @abstractmethod
    def get_known_device_names(self) -> Sequence[str]:
        """Returns the names of the devices that are known to the factory"""

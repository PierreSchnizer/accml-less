from abc import abstractmethod, ABCMeta

from ..interface.view import View


class DeviceViewFactory(metaclass=ABCMeta):
    """
    Todo:
      Is the list of known or possible devices necessary?
    """
    @abstractmethod
    def get(self, dev_name: str) -> View:
        """Returns a  "managed" device view.
        """
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    def get_managed_device_names(self):
        """Returns the names of the managed devices

        Main intend: provide facility for user to see which
        devices are managed by this object
        """


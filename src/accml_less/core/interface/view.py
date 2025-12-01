"""
Todo:
    review if the interface (protocols) of ophyd async or bluesky should
    be used directly?

    in particular:
        * ReadAble
        * Triggerable
        * Settable

"""
from abc import ABCMeta, abstractmethod
from typing import Sequence


class ViewR(metaclass=ABCMeta):
    """provide access to the view similar to ophyd-async Standard Readable and Settable

    Todo:
        improve type annotation
    """

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_properties(self) -> Sequence[str]:
        """get the available properties of this view

        Todo:
            Should it be renamed to id?
        """
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    async def trigger(self, id_: str):
        """get the value associated with a certain property

        Following ophyd async design: separate waiting that
        devices are ready from getting data.

        E.g. you want ot have new data from a device that only
        updates rather slowly. Here one wants to ensure that
        one received new data after e.g. some set before has
        happened.

        Other devices update fast. Then when read one could choose
        to use the new data from the slow device and the last data
        set from the fast device.
        """
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    async def read(self, id_: str) -> object:
        """get the value associated with a certain property"""
        raise NotImplementedError("use derived class instead")


class ViewRW(metaclass=ABCMeta):
    @abstractmethod
    async def set(self, id_: str, value: object) -> None:
        """set the value of the property

        Todo:
            how to deal with timeouts etc.
            Furthermore this method should be rather async
        """

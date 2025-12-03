from abc import ABCMeta, abstractmethod


class SignalProxyRBase(metaclass=ABCMeta):
    """ """

    @abstractmethod
    async def trigger(self):
        """Similar to ophyd async trigger

        Have a look to :meth:`View.trigger` for further details
        """
        raise NotImplementedError("use derived class instead")

    @abstractmethod
    async def read(self) -> object:
        """Similar to ophyd async read

        Have a look to :meth:`View.read` for further details

        Todo:
             improve typing of return object
        """
        raise NotImplementedError("use derived class instead")


class SignalProxyRWBase(SignalProxyRBase, metaclass=ABCMeta):
    @abstractmethod
    async def set(self, value: object):
        """Similar to ophyd async read

        Have a look to :meth:`View.read` for further details
        """
        raise NotImplementedError("use derived class instead")

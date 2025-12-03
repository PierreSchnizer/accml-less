from abc import ABCMeta, abstractmethod
from typing import Sequence, Union

from accml_less.core.interface.view import ViewR
from .signal import SignalProxyRBase, SignalProxyRWBase


class ViewWithAttributesProxyBase(ViewR, metaclass=ABCMeta):
    """
    Todo:
        should it be rather a protocil
    """

    @abstractmethod
    def get_signal_proxy(self, id_: str) -> Union[SignalProxyRBase, SignalProxyRWBase]:
        """ """

    @abstractmethod
    def __dir__(self) -> Sequence[str]:
        """
        Todo:
            appropriate to provide this interface?
        """

    @abstractmethod
    def __getattr__(self, item) -> Union[SignalProxyRBase, SignalProxyRWBase]:
        """
        Todo:
            appropriate to provide this interface?
        """
        raise NotImplementedError("use derived class instead")

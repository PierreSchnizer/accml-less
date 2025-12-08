from abc import ABCMeta, abstractmethod
from typing import Sequence, Union

from accml_less.core.interface.view import ViewR, ViewRW
from .signal import SignalProxyRBase, SignalProxyRWBase


class ViewRWithAttributesProxyBase(ViewR, metaclass=ABCMeta):
    """
    Todo:
        should it be rather a protocil
    """

    @abstractmethod
    def get_signal_proxy(self, id_: str) -> SignalProxyRBase:
        """ """


class ViewRWWithAttributesProxyBase(ViewRW, metaclass=ABCMeta):
    """
    Todo:
        should it be rather a protocil
    """

    @abstractmethod
    def get_signal_proxy(self, id_: str) -> SignalProxyRWBase:
        """ """

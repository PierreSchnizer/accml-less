from abc import ABCMeta, abstractmethod
from typing import Sequence, Union

from .signal import SignalProxyR, SignalProxyRW
from .view import View


class ViewWithAttributesProxy(View, metaclass=ABCMeta):
    """
    Todo:
        should it be rather a protocil
    """

    @abstractmethod
    def get_signal_proxy(self, id_: str) -> Union[SignalProxyR, SignalProxyRW]:
        """

        """

    @abstractmethod
    def __dir__(self) -> Sequence[str]:
        """
        Todo:
            appropriate to provide this interface?
        """

    @abstractmethod
    def __getattr__(self, item) -> Union[SignalProxyR, SignalProxyRW]:
        """
        Todo:
            appropriate to provide this interface?
        """
        raise NotImplementedError("use derived class instead")
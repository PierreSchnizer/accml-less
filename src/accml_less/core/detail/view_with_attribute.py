from typing import Sequence, Union

from ...errors import AttributeUnknownToProxiedObject
from ..interface.signal import SignalProxyR as SignalProxyRInterface
from ..interface.signal import SignalProxyRW as SignalProxyRWInterface
from ..interface.view_with_attributes import (
    ViewWithAttributesProxy as ViewWithAttributesProxyInterface,
)
from ..interface.view import ViewR
from .signal_proxy import SignalProxyR, SignalProxyRW


class ViewWithAttributesProxy(ViewWithAttributesProxyInterface):
    def __init__(self, *, proxid_object: ViewR, name: Union[str, None] = None):
        self._proxied_obj = proxid_object
        self._name = name

    def get_name(self):
        if self._name:
            return self._name
        return f"{self._proxied_obj.get_name()}-attrs-proxy"

    def get_properties(self) -> Sequence[str]:
        return self._proxied_obj.get_properties()

    async def read(self, id_: str) -> object:
        return await self._proxied_obj.read(id_)

    async def trigger(self, id_: str) -> object:
        return await self._proxied_obj.trigger(id_)

    async def set(self, id_: str, value: object) -> None:
        return await self._proxied_obj.set(id_, value)

    def get_signal_proxy(
        self, id_: str
    ) -> Union[SignalProxyRInterface, SignalProxyRWInterface]:
        """
        Todo:
            how can I find out if this object is read only or read write
        """
        attributes = self._proxied_obj.get_properties()
        if id_ not in attributes:
            raise AttributeUnknownToProxiedObject(
                f"{id_} unkown, I only know {attributes}"
            )
        return SignalProxyRW(proxied_object=self._proxied_obj, name=None, id_=id_)

    def __dir__(self):
        """
        Todo:
            do I need to add other names
        """
        return self._proxied_obj.get_properties()

    def __getattr__(self, item):
        return self.get_signal_proxy(item)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            "name={self.get_name()},"
            " properties={self._proxied_obj.get_properties()}"
            ")"
        )

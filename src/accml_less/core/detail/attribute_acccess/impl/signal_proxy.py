from typing import Union

from accml_less.core.interface.view import ViewR
from ..interface.signal import SignalProxyRBase
from ..interface.signal import SignalProxyRWBase


class SignalProxyR(SignalProxyRBase):
    """

    a much ado about closures
    """

    def __init__(self, *, proxied_object: ViewR, name: Union[str, None], id_: str):
        self.name = name
        self.proxied_object = proxied_object
        self.id_ = id_

    def get_name(self):
        if self.name is None:
            return self.proxied_object.get_name()

    async def trigger(self):
        return await self.proxied_object.trigger(self.id_)

    async def read(self) -> object:
        return await self.proxied_object.read(self.id_)

    def __repr__(self):
        return f"{self.__class__.__name__}(" f"name={self.get_name()},"  f"proxied_object={self.proxied_object}" ")"


class SignalProxyRW(SignalProxyR, SignalProxyRWBase):
    async def set(self, value: object):
        return await self.proxied_object.set(self.id_, value)

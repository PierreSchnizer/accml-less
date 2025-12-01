from typing import Union


from ..interface.signal import SignalProxyR as SignalProxyRInterface
from ..interface.signal import SignalProxyRW as SignalProxyRWInterface
from ..interface.view import ViewR


class SignalProxyR(SignalProxyRInterface):
    """

    a much ado about closures
    """

    def __init__(self, *, proxied_object: ViewR, name: Union[str, None], id_: str):
        self.name = name
        self.proxied_object = proxied_object
        self.id_ = id_

    async def trigger(self):
        return await self.proxied_object.trigger(self.id_)

    async def read(self) -> object:
        return await self.proxied_object.read(self.id_)


class SignalProxyRW(SignalProxyR, SignalProxyRWInterface):
    async def set(self, value: object):
        return await self.proxied_object.set(self.id_, value)

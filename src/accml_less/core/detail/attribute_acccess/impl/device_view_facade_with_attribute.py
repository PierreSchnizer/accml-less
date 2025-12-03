from typing import Union, Sequence

from accml_less.core.interface.destination_multiplexer import DestinationMultiplexerBase
from accml_less.core.interface.device_view_facade import DeviceViewRFacadeBase, DeviceViewRWFacadeBase
from accml_less.core.interface.view import ViewR, ViewRW


class DeviceViewRFacadeWithAttributes(DeviceViewRFacadeBase):
    def __init__(self, *, proxid_object: DeviceViewRFacadeBase, name: Union[str, None] = None):
        self._proxied_obj = proxid_object
        self._name = name

    def get_name(self) -> str:
            if self._name:
                return self._name
            return f"{self._proxied_obj.get_name()}-attrs-proxy"

    def get_properties(self) -> Sequence[str]:
        return self._proxied_obj.get_properties()

    def get_switching_object(self) -> DestinationMultiplexerBase:
        return self._proxied_obj.get_switching_object()

    def get_view_implementation(self, view_implementation_name: str) -> Union[ViewR, ViewRW]:
        return self._proxied_obj.get_view_implementation(view_implementation_name)

    def get_view_implementation_names(self) -> Sequence[str]:
        return self._proxied_obj.get_view_implementation_names()

    async def trigger(self, id_: str):
        return await self._proxied_obj.trigger(id_)

    async def read(self, id_: str) -> object:
        return await self._proxied_obj.read(id_)

    def __dir__(self):
        return list(self._proxied_obj.get_view_implementation_names()) + list(super().__dir__())

    def __getattr__(self, item):
        assert item in self.get_view_implementation_names(), f"Request for view implementation {item}, but I only know view implementations {self.get_view_implementation_names()}"
        return self._proxied_obj.get_view_implementation(item)

    def __repr__(self):
        return f"{self.__class__.__name__}(" f"name={self.get_name()},"  f"proxied_object={self._proxied_obj}" ")"

class DeviceViewRWFacadeWithAttributes(DeviceViewRFacadeWithAttributes, DeviceViewRWFacadeBase):


    async def set(self, id_: str, value: object) -> None:
        return await self._proxied_obj.set(id_, value)
from typing import Sequence, Mapping, Union

from ..interface.destination_multiplexer import DestinationMultiplexerBase
from ..interface.device_view_facade import DeviceViewRFacadeBase, DeviceViewRWFacadeBase
from ..interface.view import ViewRW, ViewR


class DeviceViewRFacade(DeviceViewRFacadeBase):
    """

    Todo:
        Does one need to make clear what is read and what is writable
    """

    def __init__(
        self,
        *,
        name: str,
        destination_switching_object: DestinationMultiplexerBase,
        delegates: Mapping[str, Union[ViewR, ViewRW]]
    ):
        self.name = name
        self.dst_switch = destination_switching_object

        # Todo: where to check that a delegate is available
        #       for any required backend
        self.delegates = delegates

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, muxer={self.dst_switch}, delegates={self.delegates})"

    def get_view_implementation(self, view_implementation_mame: str) -> Union[ViewR, ViewRW]:
        return self.delegates[view_implementation_mame]

    def get_view_implementation_names(self) -> Sequence[str]:
        return tuple(self.delegates)

    def get_name(self) -> str:
        return self.name

    def get_properties(self) -> Sequence[str]:
        return self.delegates[self.dst_switch.get_target_name()].get_properties()

    def get_switching_object(self) -> DestinationMultiplexerBase:
        return self.dst_switch

    async def trigger(self, id_):
        return await self.delegates[self.dst_switch.get_target_name()].trigger(id_)

    async def read(self, id_: str) -> object:
        return await self.delegates[self.dst_switch.get_target_name()].read(id_)


class DeviceViewRWFacade(DeviceViewRFacade, DeviceViewRWFacadeBase):
    def __init__(
        self,
        *,
            name: str,
            destination_switching_object: DestinationMultiplexerBase,
            delegates: Mapping[str, Union[ViewRW]]
    ) -> object:
        super().__init__(
            name=name,
            destination_switching_object=destination_switching_object,
            delegates=None,
        )
        self.name = name
        self.dst_switch = destination_switching_object

        # Todo: where to check that a delegate is available
        #       for any required backend
        self.delegates = delegates

    async def set(self, id_: str, value: object) -> None:
        return await self.delegates[self.dst_switch.get_target_name()].set(id_, value)


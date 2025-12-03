from typing import Dict, Sequence, Mapping

from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.translator_service import TranslatorServiceBase

from .combined_views import CombinedViews
from .device_view_facade import DeviceViewRWFacade
from .utils import build_combined_view_for_device, build_view_for_backend_for_entity, create_combined_view
from ..interface.backend import BackendRW
from ..interface.destination_multiplexer import DestinationMultiplexerBase
from ..interface.device_view_factory import (
    DeviceViewFactory as DeviceViewFactoryInterface,
)


class DeviceViewFactory(DeviceViewFactoryInterface):
    def __init__(
        self,
        *,
        backends: Mapping[str, BackendRW],
        views: Sequence[str],
        multiplexer: DestinationMultiplexerBase,
        liaison_manager: LiaisonManagerBase,
        translator_service: TranslatorServiceBase,
    ):
        """
        Todo: should it contain a name
        """
        self.liaison_manager = liaison_manager
        self.translator_service = translator_service
        self.backends = backends
        self.views = views
        #: todo: is a mapping enough ?
        self.managed_devices: Dict[str, CombinedViews] = dict()
        self.multiplexer = multiplexer

    def create_managed_device(self, entity_name: str) -> CombinedViews:
        (t_backend,) = self.backends
        # Todo: did not yet implement nore
        assert (
            t_backend == "simulator"
        ), f"Don't know how to handle backend with name {t_backend}"

        return create_combined_view(
            entity_name=entity_name,
            views=self.views,
            multiplexer=self.multiplexer,
            backends=self.backends,
            liaison_manager=self.liaison_manager,
            translator_service=self.translator_service
        )

    def get(self, dev_name: str) -> CombinedViews:
        """
        Todo:
            Should it always return a new one or keep track which it has already
        """
        cv = self.managed_devices.get(dev_name, None)
        if cv:
            return cv
        cv = self.create_managed_device(dev_name)
        self.managed_devices.update({dev_name: cv})
        return cv

    def get_managed_device_names(self) -> Sequence[str]:
        return tuple(self.managed_devices)

    def get_known_device_names(self) -> Sequence[str]:
        """
        """
        raise NotImplementedError("Should it be implemented?")


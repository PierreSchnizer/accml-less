from typing import Dict, Sequence

from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.translator_service import TranslatorServiceBase

from .combined_views import CombinedViews
from .utils import build_combined_view_for_device
from ..interface.device_view_factory import (
    DeviceViewFactory as DeviceViewFactoryInterface,
)


class DeviceViewFactory(DeviceViewFactoryInterface):
    def __init__(
        self,
        *,
        liaison_manager: LiaisonManagerBase,
        translator_service: TranslatorServiceBase
    ):
        """
        Todo: should it contain a name
        """
        self.lm = liaison_manager
        self.ts = translator_service
        #: todo: is a mapping enough ?
        self.managed_devices: Dict[str, CombinedViews] = dict()

    def create_managed_device(self, dev_name: str) -> CombinedViews:
        return build_combined_view_for_device(
            device_name=dev_name, lm=self.lm, ts=self.ts
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

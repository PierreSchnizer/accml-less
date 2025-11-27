from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.translator_service import TranslatorServiceBase

from ..interface.device_view_factory import DeviceViewFactory as DeviceViewFactoryInterface
from ..interface.view import View


class DeviceViewFactoryImpl(DeviceViewFactoryInterface):
    def __init__(
            self,
            *,
            liaison_manager: LiaisonManagerBase,
            translator_service: TranslatorServiceBase
    ):
        self.lm = liaison_manager
        self.tm = translator_service

    def get(self, dev_name: str) -> View:
        pass

    def get_managed_device_names(self):
        pass


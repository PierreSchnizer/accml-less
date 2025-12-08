from typing import Union, Sequence

from accml.core.interfaces.yellow_pages import YellowPagesBase

from .utils import add_proxies_to_combined_view
from ....interface.device_view_facade import (
    DeviceViewRFacadeBase,
    DeviceViewRWFacadeBase,
)
from ....interface.device_view_factory import DeviceViewFactoryBase


class DeviceViewFactoryWithAttributes(DeviceViewFactoryBase):
    def __init__(self, *, proxied_object: DeviceViewFactoryBase, yp: YellowPagesBase):
        self.proxied_object = proxied_object
        self.yp = yp
        self._families = FamiliesAsAttributes(parent=self, yp=yp)
        self._devices = DevicesAsAttributes(
            parent=self, device_names=self.get_known_device_names()
        )

    def get_managed_device_names(self) -> Sequence[str]:
        return self.proxied_object.get_managed_device_names()

    def get_known_device_names(self) -> Sequence[str]:
        return self.proxied_object.get_known_device_names()

    def get(
        self, dev_name: str
    ) -> Union[DeviceViewRFacadeBase, DeviceViewRWFacadeBase]:
        return add_proxies_to_combined_view(self.proxied_object.get(dev_name))

    @property
    def families(self):
        return self._families

    @property
    def devices(self):
        return self._devices

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"proxied_object={self.proxied_object}"
            f", yp={self.yp}"
            ")"
        )


class DevicesAsAttributes:
    def __init__(self, *, parent: DeviceViewFactoryBase, device_names: Sequence[str]):
        self.parent = parent
        self.device_names = device_names

    def __dir__(self):
        return self.device_names

    def __getattr__(self, item):
        return self.parent.get(item)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"proxied_object={self.parent}"
            f", device_names={self.device_names}"
            ")"
        )


class FamiliesAsAttributes:
    def __init__(self, *, parent: DeviceViewFactoryBase, yp: YellowPagesBase):
        self.parent = parent
        self.yp = yp

    def __dir__(self):
        return self.yp.get_family_names()

    def __getattr__(self, item):
        return DevicesAsAttributes(parent=self.parent, device_names=self.yp.get(item))

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"families={self.yp.get_family_names()}"
            f", proxied_object={self.parent}"
            ")"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"families={self.yp.get_family_names()}"
            f", proxied_object={self.parent}"
            f", yp={self.yp}"
            ")"
        )

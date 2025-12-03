from typing import Union

from accml_less.core.interface.combined_views import CombinedViewsBase
from accml_less.core.interface.device_view_facade import DeviceViewRWFacadeBase, DeviceViewRFacadeBase
from accml_less.core.interface.view import ViewRW
from .combined_views_with_attributes import CombinedViewWithAttributes
from .device_view_facade_with_attribute import DeviceViewRWFacadeWithAttributes
from .view_with_attribute import ViewWithAttributesProxy
from ...combined_views import CombinedViews
from ...device_view_facade import DeviceViewRWFacade, DeviceViewRFacade


def add_proxies_to_combined_view(cv: CombinedViewsBase) -> CombinedViewsBase:
    """
    need to traverse all down the tree
    """

    return CombinedViewWithAttributes(
        proxied_object=CombinedViews(
            name=f"{cv.get_name()}-attr-proxy",
            views={
                view: ViewWithAttributesProxy(
                    proxid_object=add_proxies_to_device_facade(cv.get(view))
                )
                for view in cv.get_view_names()
            },
        )
    )


def add_proxies_to_device_facade(df: Union[DeviceViewRFacadeBase, DeviceViewRWFacadeBase]) ->  DeviceViewRWFacadeBase:
    """
    Todo:
        preserve read only
    """
    return DeviceViewRWFacadeWithAttributes(
        proxid_object=DeviceViewRWFacade(
            name=df.get_name(),
            destination_switching_object=df.get_switching_object(),
            delegates={
                impl: add_proxies_to_view_implementation(df.get_view_implementation(impl))
                for impl in df.get_view_implementation_names()
            }
        )
    )


def add_proxies_to_view_implementation(view_impl: ViewRW)-> ViewRW:
    return ViewWithAttributesProxy(proxid_object=view_impl)

import logging
from typing import Union, Sequence

from accml_less.core.interface.combined_views import CombinedViewsBase
from accml_less.core.interface.device_view_facade import (
    DeviceViewRWFacadeBase,
    DeviceViewRFacadeBase,
)
from accml_less.core.interface.view import ViewRW
from .combined_views_with_attributes import CombinedViewWithAttributes
from .device_view_facade_with_attribute import DeviceViewRWFacadeWithAttributes
from .view_with_attribute import ViewWithAttributesProxy
from ...combined_views import CombinedViews
from ...device_view_facade import DeviceViewRWFacade, DeviceViewRFacade

logger = logging.getLogger("accml-less")


def without_hidden_or_dunder_methods(method_names: Sequence[str]) -> Sequence[str]:
    return [name for name in method_names if name[0] != "_"]


def add_proxies_to_combined_view(cv: CombinedViewsBase) -> CombinedViewsBase:
    """
    need to traverse all down the tree
    """

    r = CombinedViewWithAttributes(
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
    tmp = dir(r)
    tmp = without_hidden_or_dunder_methods(tmp)
    logger.debug("%s: added %s, dir returns %s", cv.get_name(), r, tmp)
    return r


def add_proxies_to_device_facade(
    df: Union[DeviceViewRFacadeBase, DeviceViewRWFacadeBase]
) -> DeviceViewRWFacadeBase:
    """
    Todo:
        preserve read only
    """

    tmp = {
        view: df.get_view_implementation(view)
        for view in df.get_view_implementation_names()
    }
    delegates = {
        view: add_proxies_to_view_implementation(impl)
        for view, impl in tmp.items()
        if impl is not None
    }

    r = DeviceViewRWFacadeWithAttributes(
        proxid_object=DeviceViewRWFacade(
            delegates=delegates,
            name=df.get_name(),
            destination_switching_object=df.get_switching_object(),
        )
    )
    tmp = dir(r)
    tmp = without_hidden_or_dunder_methods(tmp)
    logger.debug("%s: added %s, dir returns %s", df.get_name(), r, tmp)
    return r


def add_proxies_to_view_implementation(view_impl: ViewRW) -> ViewRW:
    assert view_impl is not None
    r = ViewWithAttributesProxy(proxid_object=view_impl)
    tmp = dir(r)
    tmp = without_hidden_or_dunder_methods(tmp)
    logger.debug("%s: added %s, dir returns %s", view_impl.get_name(), r, tmp)
    return r

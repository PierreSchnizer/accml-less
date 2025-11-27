from typing import Sequence

from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.translator_service import TranslatorServiceBase
from accml.core.model.identifiers import LatticeElementPropertyID
from .combined_views import CombinedViews
from .combined_views_with_attributes import CombinedViewWithAttributes
from .view import View
from .view_with_attribute import ViewWithAttributesProxy
from ..interface.combined_views import CombinedViews as CombinedViewsInterface, StandardViews


def add_proxies_to_combined_view(cv: CombinedViewsInterface) -> CombinedViewsInterface:
    return CombinedViewWithAttributes(
        proxied_object=CombinedViews(
            name=f"{cv.get_name()}-attr-proxy",
            views={
                view.value: ViewWithAttributesProxy(proxid_object=cv.get(view.value))
                for view in StandardViews
            },
        )
    )

def devices_corresponding_to_element(*, element_name: str, liaison_manager: LiaisonManagerBase) -> Sequence[str]:
    """
    """
    props = liaison_manager.get_element_properties(element_name)
    lp = [
        LatticeElementPropertyID(element_name=element_name, property=p)
        for p in props
    ]
    return [liaison_manager.forward(id_).device_name for id_ in lp]



def build_combined_view(
        *, element_name: str, lm: LiaisonManagerBase, ts: TranslatorServiceBase
) -> CombinedViewsInterface:
    props = lm.get_element_properties(element_name)

    # only prepared to handle a single device
    (device_name,) = set(
        devices_corresponding_to_element(element_name=element_name, liaison_manager=lm)
    )

    return CombinedViews(
        name=f"{element_name}-combined-views",
        views={
            StandardViews.design.value: View(
                name=f"{element_name}-design-view",
                properties=props
            ),
            StandardViews.device.value: View(
                name=f"{device_name}-device-view",
                properties=lm.get_device_properties(device_name),
            ),
        },
    )

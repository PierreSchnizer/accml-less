"""

Todo:
    rework the whole factory

"""
import itertools
from dataclasses import dataclass
from typing import Sequence

from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.state_conversion import StateConversion
from accml.core.interfaces.translator_service import TranslatorServiceBase
from accml.core.model.identifiers import (
    LatticeElementPropertyID,
    DevicePropertyID,
    ConversionID,
)
from .combined_views import CombinedViews
from .combined_views_with_attributes import CombinedViewWithAttributes
from .conversion_capsule import ConversionCapsule
from .view import View
from .view_with_attribute import ViewWithAttributesProxy
from .view_with_simulator_backend import ViewWithSimulatorBackend
from ..interface.combined_views import (
    CombinedViews as CombinedViewsInterface,
    StandardViews,
)
from ..interface.conversion_capsule import ConversionCapsuleBase
from ..interface.simulator_accelerator.accelerator_simulator import (
    AcceleratorSimulatorInterface,
)


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


def devices_corresponding_to_element(
    *, element_name: str, liaison_manager: LiaisonManagerBase
) -> Sequence[str]:
    """ """
    props = liaison_manager.get_element_properties(element_name)
    lp = [
        LatticeElementPropertyID(element_name=element_name, property=p) for p in props
    ]
    return [liaison_manager.forward(id_).device_name for id_ in lp]


def elements_corresponding_to_device(
    device_name: str, liaison_manager: LiaisonManagerBase
) -> Sequence[str]:
    return list(
        itertools.chain(
            *[
                [
                    elem.element_name
                    for elem in liaison_manager.inverse(
                        DevicePropertyID(device_name=device_name, property=p)
                    )
                ]
                for p in liaison_manager.get_device_properties(device_name)
            ]
        )
    )


def build_combined_view_for_element(
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
                name=f"{element_name}-design-view", properties=props
            ),
            StandardViews.device.value: View(
                name=f"{device_name}-device-view",
                properties=lm.get_device_properties(device_name),
            ),
        },
    )


def build_combined_view_for_device(
    *,
    device_name: str,
    lm: LiaisonManagerBase,
    ts: TranslatorServiceBase,
    backend: AcceleratorSimulatorInterface,
) -> CombinedViewsInterface:
    """

    Todo:
        should it return None on failure or raise an exception ?
    """
    props = lm.get_device_properties(device_name)

    # only prepared to handle a single device
    element_names = set(
        elements_corresponding_to_device(device_name=device_name, liaison_manager=lm)
    )
    if len(element_names) != 1:
        return None

    (element_name,) = element_names

    # now we know that properties exist ... now check that they have corresponding ones
    elem_props = lm.get_element_properties(element_name)
    dev_props = lm.get_device_properties(device_name)

    def capsule_for_elem_prop(id_: str) -> ConversionCapsuleBase:
        elem_id = LatticeElementPropertyID(element_name=element_name, property=id_)
        dev_id = lm.forward(elem_id)
        conv_id = ConversionID(lattice_property_id=elem_id, device_property_id=dev_id)
        return ConversionCapsule(
            conversion_id=conv_id, translation_object=ts.get(conv_id)
        )

    def capsule_for_dev_prop(id_: str):
        dev_id = DevicePropertyID(device_name=device_name, property=id_)
        (elem_id,) = lm.inverse(dev_id)
        conv_id = ConversionID(lattice_property_id=elem_id, device_property_id=dev_id)
        return ConversionCapsule(
            conversion_id=conv_id, translation_object=ts.get(conv_id)
        )
        return ts.get()

    # now we need to handle properly which interface the backend
    # expects ...
    # currently it is only implemented for the accelerator simulator
    # So I don't check yet which natural interface this backend expects
    # but just assume its natural interface is the "desgin" view

    natural_view = StandardViews.design.value

    assert (
        natural_view == StandardViews.design.value
    ), "Currently only implementing it for natural desgin view"

    if natural_view != StandardViews.design.value:
        tos_fwd = [capsule_for_elem_prop(prop) for prop in elem_props]
    else:
        tos_fwd = None

    if natural_view != StandardViews.device.value:
        tos_bwd = [capsule_for_dev_prop(prop) for prop in dev_props]
    else:
        tos_bwd = None

    return CombinedViews(
        name=f"{element_name}-combined-views",
        views={
            StandardViews.design.value: ViewWithSimulatorBackend(
                name=f"{element_name}-design-view",
                element_name=element_name,
                properties=elem_props,
                conversion_capsules=None,
                backend=backend,
            ),
            StandardViews.device.value: ViewWithSimulatorBackend(
                name=f"{device_name}-device-view",
                element_name=element_name,
                properties=list(tos_bwd),
                conversion_capsules=tos_bwd,
                backend=backend,
            ),
        },
    )

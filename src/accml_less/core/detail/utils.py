"""

Todo:
    rework the whole factory
    make it work independent of view

"""
import itertools
from typing import Sequence, Union, Mapping

from accml.core.interfaces.liaison_manager import LiaisonManagerBase
from accml.core.interfaces.translator_service import TranslatorServiceBase
from accml.core.model.identifiers import (
    LatticeElementPropertyID,
    DevicePropertyID,
    ConversionID,
)
from .combined_views import CombinedViews
from .conversion_capsule import ConversionCapsule
from .device_view_facade import DeviceViewRWFacade
from .view import View
from .view_with_backend import ViewRWWithBackend
from .view_with_conversion import ViewRWWithConversion, ViewWithConversionConfiguration
from ..interface.backend import BackendRW
from ..interface.combined_views import (
    CombinedViewsBase as CombinedViewsInterface,
    StandardViews,
)
from ..interface.conversion_capsule import ConversionCapsuleBase
from ..interface.destination_multiplexer import DestinationMultiplexerBase
from ..interface.view import ViewRW


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
    backend: BackendRW,
) -> CombinedViewsInterface:
    """

    Todo:
        should it return None on failure or raise an exception ?
    """

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

    cfg = ViewWithConversionConfiguration(
        name=f"{device_name}-device-view",
        native_view="device",
        target_view="design",
        properties=[
            item.get_conversion_id().device_property_id.property for item in tos_bwd
        ],
    )

    return CombinedViews(
        name=f"{element_name}-combined-views",
        views={
            StandardViews.design.value: ViewRWWithBackend(
                name=f"{element_name}-design-view",
                entity_name=element_name,
                properties=elem_props,
                backend=backend,
            ),
            StandardViews.device.value: ViewRWWithConversion(
                config=cfg,
                conversion_capsules=tos_bwd,
                backend=backend,
            ),
        },
    )


def create_combined_view(
    *,
    entity_name: str,
    views: Sequence[str],
    multiplexer: DestinationMultiplexerBase,
    backends: Mapping[str, BackendRW],
    liaison_manager: LiaisonManagerBase,
    translator_service: TranslatorServiceBase,
) -> CombinedViews:

    return CombinedViews(
        name=f"{entity_name}-combined-view",
        views={
            view: create_facade_view(
                entity_name=entity_name,
                source_view=view,
                backends=backends,
                multiplexer=multiplexer,
                liaison_manager=liaison_manager,
                translator_service=translator_service
            )
            for view in views
        },
    )


def create_facade_view(
    *,
    entity_name: str,
    source_view: str,
    backends: Mapping[str, BackendRW],
    multiplexer: DestinationMultiplexerBase,
    liaison_manager: LiaisonManagerBase,
    translator_service: TranslatorServiceBase
)-> DeviceViewRWFacade:

    delegates = {
        name: build_view_for_backend_for_entity(
            entity_name=entity_name,
            source_view=source_view,
            backend=backend,
            lm=liaison_manager,
            ts=translator_service,
        )
        for name, backend in backends.items()
    }

    return DeviceViewRWFacade(
        name=f"{entity_name}-facade",
        destination_switching_object=multiplexer,
        delegates=delegates,
    )

def build_view_for_backend_for_entity(
    *,
    entity_name: str,
    source_view: str,
    backend: BackendRW,
    lm: LiaisonManagerBase,
    ts: TranslatorServiceBase,
):
    if source_view == backend.get_natural_view_name():
        if source_view == "design":
            props = lm.get_element_properties(entity_name)
        elif source_view == "device":
            props = lm.get_device_properties(entity_name)
        else:
            raise AssertionError(f"Not prepared to handle view {source_view}")
        return _build_view_with_backend_for_entity(
            entity_name=entity_name,
            source_view=source_view,
            entity_props=props,
            backend=backend
        )

    return _build_view_with_backend_for_entity_with_conversion(
        entity_name=entity_name,
        source_view=source_view,
        backend=backend,
        lm=lm,
        ts=ts
    )

def _build_view_with_backend_for_entity(
    *,
    entity_name: str,
    source_view: str,
    entity_props: Sequence[str],
    backend: BackendRW,
) -> ViewRW:
    assert source_view == backend.get_natural_view_name()
    return ViewRWWithBackend(
        name=f"{entity_name}-{source_view}-view",
        entity_name=entity_name,
        properties=entity_props,
        backend=backend,
    )


def _build_view_with_backend_for_entity_with_conversion(
    *,
    entity_name: str,
    source_view: str,
    backend: BackendRW,
    lm: LiaisonManagerBase,
    ts: TranslatorServiceBase,
)-> Union[ViewRW, None]:
    """

    I only need conversion as this view is not in the backend's view
    """

    assert source_view != backend.get_natural_view_name(),\
        f"Why did I end up here given that {source_view} == {backend.get_natural_view_name()}"


    if backend.get_natural_view_name() == "device":
        # Need to convert to device from what ever view is requested
        assert source_view == "design", "Expected that I convert from design to device view"
        element_name = entity_name
        device_names = set(
            devices_corresponding_to_element(
                element_name=element_name, liaison_manager=lm
            )
        )
        if len(device_names) != 1:
            return None
        (device_name,) = device_names
        props = lm.get_element_properties(element_name)
        tos = [capsule_for_elem_prop(element_name=element_name, property=prop, lm=lm, ts=ts) for prop in props]

    elif backend.get_natural_view_name() == "design":
        assert source_view == "device", "Expected that I convert from to device to design view"
        # only prepared to handle a single device
        device_name = entity_name
        element_names = set(
            elements_corresponding_to_device(
                device_name=device_name, liaison_manager=lm
            )
        )
        if len(element_names) != 1:
            return None

        (element_name,) = element_names
        props = lm.get_device_properties(device_name)
        tos = [capsule_for_dev_prop(device_name=device_name, property=prop, lm=lm, ts=ts) for prop in props]

    else:
        raise AssertionError(f"Don't know how to handle natural {backend.get_natural_view_name()}")

    # now we know that properties exist ... now check that they have corresponding ones
    cfg = ViewWithConversionConfiguration(
        name=f"{entity_name}-conf-{source_view}-{backend.get_natural_view_name()}-view",
        native_view=source_view,
        target_view=backend.get_natural_view_name(),
        properties=props,
    )

    return ViewRWWithConversion(
        config=cfg,
        conversion_capsules=tos,
        backend=backend,
    )


def capsule_for_elem_prop(
    *,
    element_name: str,
    property: str,
    lm: LiaisonManagerBase,
    ts: TranslatorServiceBase,
) -> ConversionCapsuleBase:
    elem_id = LatticeElementPropertyID(element_name=element_name, property=property)
    dev_id = lm.forward(elem_id)
    conv_id = ConversionID(lattice_property_id=elem_id, device_property_id=dev_id)
    return ConversionCapsule(conversion_id=conv_id, translation_object=ts.get(conv_id))


def capsule_for_dev_prop(
    *,
    device_name: str,
    property: str,
    lm: LiaisonManagerBase,
    ts: TranslatorServiceBase,
) -> ConversionCapsuleBase:
    dev_id = DevicePropertyID(device_name=device_name, property=property)
    (elem_id,) = lm.inverse(dev_id)
    conv_id = ConversionID(lattice_property_id=elem_id, device_property_id=dev_id)
    return ConversionCapsule(conversion_id=conv_id, translation_object=ts.get(conv_id))

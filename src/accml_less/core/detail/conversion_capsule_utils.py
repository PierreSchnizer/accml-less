from typing import Sequence, Union

from accml.core.model.identifiers import ConversionID

from ..interface.combined_views import StandardViews
from ..interface.conversion_capsule import ConversionCapsuleBase


def get_conversion_capsule(
    *,
    capsules: Sequence[ConversionCapsuleBase],
    entity_property: str,
    native_view: str,
    target_view: str,
) -> Union[ConversionCapsuleBase, None]:
    """

    Currently only prepared for the StandardViews
    """

    # currently only prepared for these views
    # but could be extended
    native_view = StandardViews(native_view)
    target_view = StandardViews(target_view)

    if native_view == StandardViews.design:
        assert (
            target_view == StandardViews.device
        ), f"Native view {native_view}: only prepared to handle a target view of 'device'"

        def check_property(id_: ConversionID) -> str:
            return id_.lattice_property_id.property

    elif native_view == StandardViews.device:
        assert (
            target_view == StandardViews.design
        ), f"Native view {native_view}: only prepared to handle a target view of 'design'"

        def check_property(id_: ConversionID) -> str:
            return id_.device_property_id.property

    else:
        raise AssertionError(
            f"Not prepared to deal with a native view of {native_view}"
        )

    for capsule in capsules:
        #: Be aware: the name of the entity on the other side can be
        #: different
        if check_property(capsule.get_conversion_id()) == entity_property:
            return capsule
    return None


# def get_conversion_capsule_for_device_property(
#     *, capsules: Sequence[ConversionCapsuleBase], device_property: str
# ) -> Union[ConversionCapsuleBase, None]:
#    for capsule in capsules:
#        #: todo yet an other check for the device name
#        conv_id = capsule.get_conversion_id()
#        if conv_id.device_property_id.property == device_property:
#            return capsule
#    return None

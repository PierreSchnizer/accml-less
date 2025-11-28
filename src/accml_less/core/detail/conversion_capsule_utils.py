from typing import Sequence, Union

from accml_less.core.interface.conversion_capsule import ConversionCapsuleBase
from accml_less.core.interface.view import ViewR


def get_conversion_capsule_for_device_property(
    *, capsules: Sequence[ConversionCapsuleBase], device_property: str
) -> Union[ConversionCapsuleBase, None]:
    for capsule in capsules:
        #: todo yet an other check for the device name
        conv_id = capsule.get_conversion_id()
        if conv_id.device_property_id.property == device_property:
            return capsule
    return None

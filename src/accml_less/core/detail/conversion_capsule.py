from accml.core.interfaces.state_conversion import StateConversion
from accml.core.model.identifiers import ConversionID

from ..interface.conversion_capsule import ConversionCapsuleBase


class ConversionCapsule(ConversionCapsuleBase):
    def __init__(
        self, *, conversion_id: ConversionID, translation_object: StateConversion
    ):
        self.conv_id = conversion_id
        self.to = translation_object

    def get_conversion_id(self) -> ConversionID:
        return self.conv_id

    def get_translation_object(self) -> StateConversion:
        return self.to

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            "conversion_id={self.conv_id},"
            " translation_object:{self.to}"
            ")"
        )

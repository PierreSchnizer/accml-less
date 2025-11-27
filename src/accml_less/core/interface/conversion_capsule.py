from abc import ABCMeta

from accml.core.interfaces.state_conversion import StateConversion
from accml.core.model.identifiers import ConversionID


class ConversionCapsuleBase(metaclass=ABCMeta):
    """
    Todo:
        analyse if it shoud be provided by accml.model
    """
    def get_conversion_id(self) -> ConversionID:
        raise NotImplementedError("use derived class instead")

    def get_translation_object(self) -> StateConversion:
        raise NotImplementedError("use derived class instead")

    translation_object: StateConversion

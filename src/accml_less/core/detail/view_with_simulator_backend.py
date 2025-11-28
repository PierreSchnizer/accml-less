"""

Todo:
    Refactor intermixing translation and read / write

    Provide a proxy or delegator for getting info doen
"""
import logging
from typing import Sequence

from .conversion_capsule_utils import get_conversion_capsule_for_device_property
from ..interface.conversion_capsule import ConversionCapsuleBase
from ..interface.simulator_accelerator.accelerator_simulator import (
    AcceleratorSimulatorInterface,
)
from ..interface.view import ViewR as ViewInterface

logger = logging.getLogger("accml")


class ViewWithSimulatorBackend(ViewInterface):
    """

    fine tuned logger

    Todo:
        consider if only one element is supported here
        consider if then directly the element should be
        passed and not the accelerator object
    """

    def __init__(
        self,
        *,
        name: str,
        element_name: str,
        properties: Sequence[str],
        backend: AcceleratorSimulatorInterface,
        backends_view: str = "design",
        conversion_capsules: Sequence[ConversionCapsuleBase],
        logger=logger,
    ):
        self._name = name
        self.element_name = element_name
        self._properties = properties
        self.backend = backend
        self.backends_view = backends_view
        self.conversion_capsules = conversion_capsules
        self.logger = logger

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name}, properties={self._properties})"

    def get_properties(self) -> Sequence[str]:
        return self._properties

    def _get_conversion_capsule(self, id_: str) -> ConversionCapsuleBase:
        """
        Todo:
            rename method
            need to address which direction is searched
        """
        assert self.conversion_capsules is not None
        capsule = get_conversion_capsule_for_device_property(
            capsules=self.conversion_capsules, device_property=id_
        )
        if capsule is None:
            raise AssertionError(f"I expected to find a capsule for {id_}")

        elem_name = capsule.get_conversion_id().lattice_property_id.element_name
        assert (
            elem_name == self.element_name
        ), f"Conversion working on elem {elem_name}, but I am only handling {self.element_name}"

        return capsule

    async def read(self, id_: str) -> object:
        elem_name = self.element_name
        capsule = None
        if self.conversion_capsules:
            capsule = self._get_conversion_capsule(id_)
            lat_id = capsule.get_conversion_id().lattice_property_id
            elem_name = lat_id.element_name
            id_ = lat_id.property

        elem = self.backend.get(elem_name)
        res = elem.peek(id_)
        if capsule:
            res = capsule.get_translation_object().forward(res)

        return res

    async def trigger(self, id_: str):
        logger.info(
            "%s(name=%s).trigger(%s): no action implemented",
            self.__class__.__name__,
            self.get_name(),
            id_,
        )

    async def set(self, id_: str, value: object) -> None:
        elem_name = self.element_name
        capsule = None
        if self.conversion_capsules:
            capsule = self._get_conversion_capsule(id_)
            lat_id = capsule.get_conversion_id().lattice_property_id
            elem_name = lat_id.element_name
            id_ = lat_id.property
            value = capsule.get_translation_object().inverse(value)

        elem = self.backend.get(elem_name)
        # todo: why do I need to pass element_name
        await elem.update(id_, value)

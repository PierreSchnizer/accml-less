import logging
from dataclasses import dataclass
from typing import Sequence, Tuple

from accml.core.model.identifiers import ConversionID

from .conversion_capsule_utils import get_conversion_capsule
from ..interface.backend import BackendR, BackendRW
from ..interface.combined_views import StandardViews
from ..interface.conversion_capsule import ConversionCapsuleBase
from ..interface.view import ViewR, ViewRW

logger = logging.getLogger("accml-less")


@dataclass
class ViewWithConversionConfiguration:
    """
    todo: move it to some model?
    """

    #: name of this conversion ... rather for debugging
    #: chosen well helps user understand who is handling
    #: this step
    name: str
    #: inputs are received in this view.
    native_view: str
    #: inputs received in this view can be directly passed on
    #: to backend
    #: todo use "backend view"?
    target_view: str
    properties: Sequence[str]


class ViewRWithConversion(ViewR):
    """
    **NB**: its users responsibility that the properties of the
    capsule are unique.

    Further note no checks will be made that the entities
    are the same
    * if the native view is design: it will not check that
      the lattice element id is the same for all conversion ids
    * if the native view is device: it will not check that
      the lattice element id is the same for all conversion ids

    """

    def __init__(
        self,
        *,
        backend: BackendR,
        conversion_capsules: Sequence[ConversionCapsuleBase],
        config: ViewWithConversionConfiguration,
        logger=logger,
    ):

        assert (
            config.target_view != config.native_view
        ), f"Why this wrapper if native_view {config.native_view} == target_view {config.target_view}"
        self.backend = backend
        self.conversion_capsules = conversion_capsules
        self.cfg = config
        self.logger = logger

    def get_name(self) -> str:
        return self.cfg.name

    def get_properties(self) -> Sequence[str]:
        return self.cfg.properties

    def _get_conversion_capsule(self, id_: str) -> ConversionCapsuleBase:
        """
        Todo:
            rename method
            need to address which direction is searched
        """
        assert self.conversion_capsules is not None
        capsule = get_conversion_capsule(
            capsules=self.conversion_capsules,
            entity_property=id_,
            native_view=self.cfg.native_view,
            target_view=self.cfg.target_view,
        )
        if capsule is None:
            self.logger.error(
                "%s.%s: Failed to find a capsule for %s",
                __name__,
                self.__class__.__name__,
                id_,
            )
            self.logger.warning(
                "%s:%s Capsules I know have the following ids %s",
                __name__,
                self.__class__.__name__,
                [c.get_conversion_id() for c in self.conversion_capsules],
            )
            raise AssertionError(f"I need a capsule for {id_}")
        return capsule

    def get_target_entity_property_id(self, id_: ConversionID) -> Tuple[str, str]:
        if self.cfg.target_view == StandardViews.design.value:
            return (
                id_.lattice_property_id.element_name,
                id_.lattice_property_id.property,
            )
        elif self.cfg.target_view == StandardViews.device.value:
            return (id_.device_property_id.device_name, id_.device_property_id.property)
        else:
            raise AssertionError(
                f"Only prepared to handle standard views but target view was {self.cfg.target_view}"
            )

    async def trigger(self, id_: str):
        entity_id, prop_id = self.get_target_entity_property_id(
            self._get_conversion_capsule(id_).get_conversion_id()
        )
        return await self.backend.trigger(entity_id, prop_id)

    async def read(self, id_: str) -> object:
        capsule = self._get_conversion_capsule(id_)
        entity_id, prop_id = self.get_target_entity_property_id(
            capsule.get_conversion_id()
        )
        read_value = await self.backend.read(entity_id, prop_id)
        if self.cfg.target_view == StandardViews.device.value:
            value = capsule.get_translation_object().inverse(read_value)
        elif self.cfg.target_view == StandardViews.design.value:
            value = capsule.get_translation_object().forward(read_value)
        else:
            raise AssertionError(
                "Don't know how to convert read value from target view {self.cfg.target_view}"
            )
        return value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"cfg={self.cfg},"
            f" backend={self.backend},"
            f" conversion_capsules={self.conversion_capsules}"
            ")"
        )


class ViewRWWithConversion(ViewRWithConversion, ViewRW):
    def __init__(
        self,
        backend: BackendRW,
        conversion_capsules: Sequence[ConversionCapsuleBase],
        config: ViewWithConversionConfiguration,
        logger=logger,
    ):
        super().__init__(
            conversion_capsules=conversion_capsules,
            backend=backend,
            config=config,
            logger=logger,
        )
        # Just for type checking
        self.backend = backend

    async def set(self, id_: str, value: object) -> None:
        capsule = self._get_conversion_capsule(id_)
        entity_id, prop_id = self.get_target_entity_property_id(
            capsule.get_conversion_id()
        )

        to = capsule.get_translation_object()
        if self.cfg.target_view == StandardViews.device.value:
            set_value = to.forward(value)
        elif self.cfg.target_view == StandardViews.design.value:
            set_value = to.inverse(value)
        else:
            raise AssertionError(
                "Don't know how to convert read value from target view {self.cfg.target_view}"
            )

        return await self.backend.set(entity_id, prop_id, set_value)

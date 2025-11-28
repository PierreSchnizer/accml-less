"""Views directly directing request to back end
"""
import logging
from typing import Sequence

from ..interface.backend import BackendR, BackendRW
from ..interface.view import ViewR, ViewRW

logger = logging.getLogger("accml")


class ViewRWithBackend(ViewR):
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
        entity_name: str,
        properties: Sequence[str],
        backend: BackendR,
        backends_view: str,
        logger=logger,
    ):
        self._name = name
        self.entity_name = entity_name
        self._properties = properties
        self.backend = backend
        self.backends_view = backends_view
        self.logger = logger

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name}, properties={self._properties}, backend={self.backend})"

    def get_properties(self) -> Sequence[str]:
        return self._properties

    async def read(self, id_: str) -> object:
        return await self.backend.read(self.entity_name, id_)

    async def trigger(self, id_: str):
        logger.info(
            "%s(name=%s).trigger(%s): no action implemented",
            self.__class__.__name__,
            self.get_name(),
            id_,
        )


class ViewRWWithBackend(ViewRWithBackend, ViewRW):
    def __init__(
        self,
        *,
        name: str,
        entity_name: str,
        properties: Sequence[str],
        backend: BackendRW,
        backends_view: str,
        logger=logger,
    ):
        super().__init__(
            name=name,
            entity_name=entity_name,
            properties=properties,
            backend=backend,
            backends_view=backends_view,
            logger=logger,
        )
        # for type check
        self.backend = backend

    async def set(self, id_: str, value: object) -> None:
        return await self.backend.set(self.entity_name, value)

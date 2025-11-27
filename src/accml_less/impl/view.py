from typing import Sequence

from ..interface.view import View as ViewInterface


class View(ViewInterface):

    def __init__(self, name: str, properties: Sequence[str]):
        self._name = name
        self._properties = properties

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self._name}, properties={self._properties})"

    def get_properties(self) -> Sequence[str]:
        return  self._properties

    def read(self, id_: str) -> object:
        raise NotImplementedError("need to delegate to mexec")

    def trigger(self, id_: str) -> object:
        raise NotImplementedError("need to delegate to mexec")

    def set(self, id_: str, value: object) -> None:
        raise NotImplementedError("need to delegate to mexec")
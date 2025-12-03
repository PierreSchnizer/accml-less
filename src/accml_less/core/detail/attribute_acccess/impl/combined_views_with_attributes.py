from typing import Sequence, Union

from accml_less.core.interface.combined_views import CombinedViewsBase
from accml_less.core.interface.view import ViewR


class CombinedViewWithAttributes(CombinedViewsBase):
    def __init__(self, *, proxied_object: CombinedViewsBase, name: Union[str, None] = None):
        self._proxied_object = proxied_object
        self._name = name

    def get_name(self) -> str:
        if self._name:
            return self._name
        return f"{self._proxied_object.get_name()}-wth-attrs"

    def get(self, view: str) -> ViewR:
        return self._proxied_object.get(view)

    def get_view_names(self) -> Sequence[str]:
        return self._proxied_object.get_view_names()

    def __getattr__(self, view_name):
        return self._proxied_object.get(view_name)

    def __dir__(self):
        return list(self._proxied_object.views) + super().__dir__()

    def __repr__(self):
        d = {view: self.get(view) for view in self._proxied_object.get_view_names()}
        return f"{self.__class__.__name__}(name={self.get_name()}, views={d})"

from typing import Sequence, Union

from ..interface.combined_views import CombinedViews, StandardViews
from ..interface.view import View


class CombinedViewWithAttributes(CombinedViews):
    def __init__(self, *, proxied_object: CombinedViews, name: Union[str, None]=None):
        self.proxied_object = proxied_object
        self.name = name

    def get_name(self) -> str:
        if self.name:
            return self.name
        return f"{self.proxied_object.get_name()}-wth-attrs"

    def get(self, view: str) -> View:
        return self.proxied_object.get(view)

    def get_view_names(self) -> Sequence[str]:
        return self.proxied_object.get_view_names()

    def __getattr__(self, view_name):
        return self.proxied_object.get(view_name)

    def __dir__(self):
        return tuple(self.proxied_object.views)

    def __repr__(self):
        d = {view: self.get(view) for view in self.proxied_object.get_view_names()}
        return f"{self.__class__.__name__}(name={self.get_name()}, views={d})"
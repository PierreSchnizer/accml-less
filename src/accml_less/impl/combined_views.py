from typing import Dict, Sequence

from ..interface.combined_views import CombinedViews as CombinedViewsInterface
from ..interface.combined_views import StandardViews
from ..interface.view import View


class CombinedViews(CombinedViewsInterface):
    def __init__(self, *, name: str, views: Dict[str, View]):
        self.name = name
        self.views = views

    def get_name(self) -> str:
        return self.name

    def get(self, view: str) -> View:
        return self.views[view]

    def get_view_names(self) -> Sequence[str]:
        return tuple(self.views.keys())

    def __repr__(self):
        d = {key: item  for key, item in self.views.items()}
        return f"{self.__class__.__name__}(name={self.name}, views={d})"
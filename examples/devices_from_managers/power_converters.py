import itertools
import logging

from accml.custom.facility_specific.bessyii.liasion_translator_setup import (
    load_managers,
)

from accml_less.core.detail.device_view_factory import DeviceViewFactory
from accml_less.core.detail.utils import devices_corresponding_to_element

logger = logging.getLogger("accml-mml")


def main():
    yp, lm, ts = load_managers()
    quadrupole_names = yp.get("quadrupoles")

    dvf = DeviceViewFactory(
        liaison_manager=lm,
        translator_service=ts
    )

    # I deliberately work only with power converters now
    dev_names = list(
        itertools.chain(*[
            devices_corresponding_to_element(element_name=quad_name, liaison_manager=lm)
            for quad_name in yp.get("quadrupoles")
        ])
    )
    dev_views = [dvf.get(name) for name in dev_names]
    dev_views = [view for view in dev_views if view is not None]
    dev_views

if __name__ == "__main__":
    main()

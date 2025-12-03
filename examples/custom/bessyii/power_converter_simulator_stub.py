import asyncio
import itertools
import logging

from lat2db.model.accelerator import Accelerator
from accml.custom.facility_specific.bessyii.liasion_translator_setup import (
    load_managers,
)

from accml_less.core.detail.device_view_factory import DeviceViewFactory
from accml_less.core.detail.utils import (
    devices_corresponding_to_element,
    build_combined_view_for_device,
)
from accml_less.core.detail.destination_multiplexer import DestinationMultiplexer
from accml_less.custom.simulators.pyat.accelerator_simulator import (
    PyATAcceleratorSimulator,
)
from accml_less.custom.simulators.pyat.simulator_backend import SimulatorBackend

logger = logging.getLogger("accml-less")


async def main():

    acc = SimulatorBackend(
        name="bessyii-pyat-simulator",
        acc=PyATAcceleratorSimulator(
            at_lattice=Accelerator(
                file_name="bessyii_lattice_json.json", from_json=True
            ).ring
        ),
    )

    yp, lm, ts = load_managers()
    quadrupole_names = yp.get("quadrupoles")

    multiplexer = DestinationMultiplexer(target_names=["simulator"])
    dvf = DeviceViewFactory(
        views=["design"],
        multiplexer=multiplexer,
        backends=dict(simulator=acc),
        liaison_manager=lm,
        translator_service=ts,
    )

    # I deliberately work only with power converters for now
    # here I find out which they are
    dev_names = list(
        itertools.chain(
            *[
                devices_corresponding_to_element(
                    element_name=quad_name, liaison_manager=lm
                )
                for quad_name in yp.get("quadrupoles")
            ]
        )
    )
    # select one for test
    dev_name = dev_names[-1]
    print(f"{dev_name=}")
    cv = dvf.get(dev_name)

    cv = build_combined_view_for_device(device_name=dev_name, lm=lm, ts=ts, backend=acc)
    if cv is None:
        logger.error(f"Could not build a view for device {dev_name}")
        return

    main_strength = await cv.get("design").read("main_strength")
    # There seems to be something really strange with the conversion value
    current = await cv.get("device").read("set_current")

    await cv.get("device").set("set_current", current)
    chk_main_strength = await cv.get("design").read("main_strength")
    # There seems to be something really strange with the conversion value
    chk_current = await cv.get("device").read("set_current")

    txt = f"""Read:
    strength: {main_strength}
    current: {current}

Check after setting current:
    strength: {chk_main_strength}
    current: {chk_current}
"""
    print(txt)


if __name__ == "__main__":
    asyncio.run(main())

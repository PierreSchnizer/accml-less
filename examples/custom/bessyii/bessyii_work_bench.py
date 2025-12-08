import asyncio

from accml.custom.facility_specific.bessyii.liasion_translator_setup import (
    load_managers,
)
from lat2db.model.accelerator import Accelerator

from accml_less.core.detail.attribute_acccess.impl.device_view_factory import (
    DeviceViewFactoryWithAttributes,
)
from accml_less.core.detail.attribute_acccess.impl.utils import (
    add_proxies_to_combined_view,
)
from accml_less.core.detail.destination_multiplexer import DestinationMultiplexer
from accml_less.core.detail.device_view_factory import DeviceViewFactory

from accml_less.custom.simulators.pyat.accelerator_simulator import (
    PyATAcceleratorSimulator,
)
from accml_less.custom.simulators.pyat.simulator_backend import SimulatorBackend


def instaniate_bessyii_device_factory():
    yp, lm, ts = load_managers()
    multiplexer = DestinationMultiplexer(target_names=["simulator"])
    acc = SimulatorBackend(
        name="bessyii-pyat-simulator",
        acc=PyATAcceleratorSimulator(
            at_lattice=Accelerator(
                file_name="bessyii_lattice_json.json", from_json=True
            ).ring
        ),
    )

    dvf = DeviceViewFactory(
        views=["design", "device"],
        multiplexer=multiplexer,
        backends=dict(simulator=acc),
        liaison_manager=lm,
        translator_service=ts,
    )
    dvf.get("PQIPT6R")
    return multiplexer, dvf, yp


async def read_print_signal(signal):
    print(signal)
    print(await signal.read())


async def read(cva):
    await read_print_signal(cva.device.set_current)


if __name__ == "__main__":
    mux, dvf, yp = instaniate_bessyii_device_factory()
    dvfa = DeviceViewFactoryWithAttributes(proxied_object=dvf, yp=yp)
    name = "PQIPT6R"
    print(dvf.get_known_device_names())
    cv = dvf.get(name)
    props = cv.get("device").get_properties()
    print(f"{name}: device properties {props}")
    props = cv.get("design").get_properties()
    print(f"{name}: design properties {props}")

    cva = add_proxies_to_combined_view(cv)

    print(dvfa.families)
    print(repr(dvfa.families))
    print(dvfa.devices)
    print(repr(dvfa.devices))

    cva = dvfa.get(name)
    cva

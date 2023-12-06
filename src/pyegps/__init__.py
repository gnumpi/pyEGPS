"""Controlling Energenie Power Strips."""
from __future__ import annotations
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyegps")
except PackageNotFoundError:
    from ._version import __version__  # noqa

from .device import Device

from .usb.eg_powerstrip import PowerStripUSB
from .dummy.powerstrip import DummyPowerStrip

DEVICE_IMPLEMENTATIONS: list[Device] = [PowerStripUSB]


def search_for_devices() -> list[Device]:
    """Search and return all supported devices."""
    return [dev for impl in DEVICE_IMPLEMENTATIONS for dev in impl.search_for_devices()]


def get_device_types() -> list[str]:
    """Return all supported device types."""
    return [impl.get_device_type() for impl in DEVICE_IMPLEMENTATIONS]


def get_device(device_id: str) -> Device | None:
    """Try to find the device for the given device_id and return it."""
    for impl in DEVICE_IMPLEMENTATIONS:
        dev_or_none = impl.get_device(device_id)
        if dev_or_none is not None:
            return dev_or_none


def use_dummy_devices() -> None:
    """Let dummy devices appear in searches for devices."""
    DEVICE_IMPLEMENTATIONS.clear()
    DEVICE_IMPLEMENTATIONS.append(DummyPowerStrip)

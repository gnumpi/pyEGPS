"""Controlling Energenie Power Strips."""
from .device import Device

from .usb.eg_powerstrip import PowerStripUSB

DEVICE_IMPLEMENTATIONS: list[Device] = [PowerStripUSB]


def get_all_devices() -> list[Device]:
    """Search and return all supported devices."""
    return [dev for impl in DEVICE_IMPLEMENTATIONS for dev in impl.search_for_devices()]


def get_device_types() -> list[str]:
    """Return all supported device types."""
    return [impl.get_device_type() for impl in DEVICE_IMPLEMENTATIONS]

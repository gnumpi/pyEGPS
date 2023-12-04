"""Controlling Energenie PM power strips."""
from .devices import Device

DEVICE_IMPLEMENTATIONS: list[Device] = []


def get_all_devices() -> list[Device]:
    """Search and return all supported devices."""
    return [dev for impl in DEVICE_IMPLEMENTATIONS for dev in impl.search_for_devices()]


def get_device_types() -> list[str]:
    """Return all supported device types."""
    return [impl.get_device_type() for impl in DEVICE_IMPLEMENTATIONS]

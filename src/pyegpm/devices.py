"""Definition of the devices base class."""

from __future__ import annotations

from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod


class Device(ABC):
    """Abstract base class for all devices."""

    @abstractstaticmethod
    def get_device_type() -> str:
        """Return device type."""

    @abstractclassmethod
    def search_for_devices(cls) -> list[Device]:
        """Search for supported devices."""
        pass

    @abstractclassmethod
    def get_device(cls, device_id: str) -> Device | None:
        """Get the device for the given device_id."""
        pass

    @abstractmethod
    def summary(self) -> str:
        """Return summary of device status."""
        pass

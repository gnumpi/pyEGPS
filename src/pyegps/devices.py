"""Definition of the devices base class."""

from __future__ import annotations

import abc


class Device(abc.ABC):
    """Abstract base class for all devices."""

    @staticmethod
    @abc.abstractmethod
    def get_device_type() -> str:
        """Return device type."""

    @classmethod
    @abc.abstractmethod
    def search_for_devices(cls) -> list[Device]:
        """Search for supported devices."""

    @classmethod
    @abc.abstractmethod
    def get_device(cls, device_id: str) -> Device | None:
        """Get the device for the given device_id."""

    @abc.abstractmethod
    def summary(self) -> str:
        """Return summary of device status."""

"""Definition of the base class for alle devices."""
from __future__ import annotations

import abc


class Device(abc.ABC):
    """Abstract base class for all devices."""

    @abc.abstractmethod
    def device_id(self):
        """Return a unique identifier for the device."""

    @abc.abstractmethod
    def manufacturer(self):
        """Return the device manufacturer."""

    @abc.abstractmethod
    def name(self):
        """Return the product name."""

    @staticmethod
    @abc.abstractmethod
    def get_device_type() -> str:
        """Return the device type."""

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
        """Return a summary of the device status."""

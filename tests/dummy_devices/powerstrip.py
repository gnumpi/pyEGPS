"""Dummy implementation of PowerStrip."""
from __future__ import annotations

from pyegpm.powerstrip import PowerStrip


class DummyPowerStrip(PowerStrip):
    """Dummy PowerStrip Device."""

    def __init__(self, devId: str):
        """Initiate new DummyDevice."""
        self._devId = devId

    @property
    def deviceId(self) -> str:
        return self._devId

    @property
    def numberOfSockets(self):
        return 5

    def switch_on(self, socket: int) -> None:
        super().switch_on(socket)

    def switch_off(self, socket: int) -> None:
        super().switch_off(socket)

    def get_status(self, socket: int) -> bool:
        super().get_status(socket)
        return socket < 3

    @classmethod
    def search_for_devices(cls) -> list[DummyPowerStrip]:
        return [cls(devId) for devId in ["AA:BB:CC", "00:11:22"]]

    @classmethod
    def get_device(cls, device_id: str) -> DummyPowerStrip | None:
        devices = cls.search_for_devices()
        for d in devices:
            if d.deviceId == device_id:
                return d
        return None

    def __repr__(self) -> str:
        return f"DummyPowerStrip: {self.deviceId}"

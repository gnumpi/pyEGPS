"""Dummy implementation of PowerStrip."""
from __future__ import annotations

import random

from pyegps.powerstrip import PowerStrip


class DummyPowerStrip(PowerStrip):
    """Dummy PowerStrip Device."""

    DEVICES = []

    def __init__(self, devId: str, number_of_sockets: int):
        """Initiate new DummyDevice."""
        self._devId = devId
        self._numberOfSockets = number_of_sockets
        self._status = [random.randint(0, 1) for _ in range(number_of_sockets)]

    @property
    def deviceId(self) -> str:
        return self._devId

    @property
    def numberOfSockets(self):
        return self._numberOfSockets

    def switch_on(self, socket: int) -> None:
        super().switch_on(socket)
        self._status[socket] = 1

    def switch_off(self, socket: int) -> None:
        super().switch_off(socket)
        self._status[socket] = 0

    def get_status(self, socket: int) -> bool:
        super().get_status(socket)
        return self._status[socket] == 1

    @classmethod
    def search_for_devices(cls) -> list[DummyPowerStrip]:
        if len(cls.DEVICES) == 0:
            cls.DEVICES += [
                cls(devId, sockets)
                for devId, sockets in [("AA:BB:CC", 4), ("00:11:22", 2)]
            ]

        return cls.DEVICES

    @classmethod
    def get_device(cls, device_id: str) -> DummyPowerStrip | None:
        devices = cls.search_for_devices()
        for d in devices:
            if d.deviceId == device_id:
                return d
        return None

    def __repr__(self) -> str:
        return f"DummyPowerStrip: {self.deviceId}"

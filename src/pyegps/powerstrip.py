"""Abstract PowerStrip Class."""

from abc import ABC, abstractproperty
import logging

from .devices import Device
from .exceptions import (
    INVALID_SOCKET_NUMBER,
)

_logger = logging.getLogger(__name__)


class PowerStrip(Device, ABC):
    """Abstract class of a PowerStrip device."""

    @staticmethod
    def get_device_type() -> str:
        return "PowerStrip"

    @abstractproperty
    def deviceId(self) -> str:
        """Return the unique identifier of the power strip."""
        pass

    @abstractproperty
    def numberOfSockets(self) -> int:
        """Return number of controllable sockets."""
        pass

    def get_status(self, socket: int) -> bool:
        """
        Get the status of the socket given by 'socket'.

        @param socket: socket number
        @return: status
        """
        if socket < 0 or socket > self.numberOfSockets - 1:
            raise INVALID_SOCKET_NUMBER

    def switch_off(self, socket: int) -> None:
        """
        Switches the socket with the given id off.

        @param socket: socket number
        """
        if socket < 0 or socket > self.numberOfSockets - 1:
            raise INVALID_SOCKET_NUMBER

        _logger.info(f"Socket {socket} switched off.")

    def switch_on(self, socket: int) -> None:
        """
        Switches the socket with the given id on.

        @param socket: socket number
        """
        if socket < 0 or socket > self.numberOfSockets - 1:
            raise INVALID_SOCKET_NUMBER

        _logger.info(f"Socket {socket} switched on.")

    def __repr__(self) -> str:
        """Override default repr string."""
        return f"Powerstrip: {self.deviceId}\n"

    def summary(self) -> str:
        s = self.__repr__() + "\n"
        for socket in range(self.numberOfSockets):
            s += f"Socket #{socket}: {'on' if self.get_status(socket) else 'off'}\n"
        return s
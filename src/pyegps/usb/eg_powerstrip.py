"""Implementation of USB PowerStrips by Energenie."""
from __future__ import annotations
import logging

import usb.core
from usb.core import Device as UsbDevice
import usb.util

from ..powerstrip import PowerStrip

from ..exceptions import (
    USB_IO_ERROR,
    UNSUPPORTED_PRODUCT_ID,
)

_logger = logging.getLogger(__name__)

USB_VENDOR_ID = 0x04B4
USB_PRODUCT_IDS = [0xFD10, 0xFD11, 0xFD12, 0xFD13, 0xFD15]
PRODUCT_SOCKET_RANGES = [(0, 0), (1, 1), (1, 4), (1, 4), (1, 4)]

USB_CTRL_TRANSFER_TRIES = 5
USB_CTRL_TRANSFER_TIMEOUT = 500


class PowerStripUSB(PowerStrip):
    """Represents an Energenie Power-Strip."""

    def __init__(self, dev: UsbDevice):
        """Initiate PowerStripUSB device.

        :param dev: usb device instance
        :type dev: usb.core.Device
        :raises UNSUPPORTED_PRODUCT_ID: Given usb device has unsupported product id.
        """
        self.productId = dev.idProduct

        if self.productId not in USB_PRODUCT_IDS:
            raise UNSUPPORTED_PRODUCT_ID

        self._dev = dev
        self._device_id = None

        minAddr, maxAddr = PRODUCT_SOCKET_RANGES[USB_PRODUCT_IDS.index(self.productId)]
        self._addrMapping = range(minAddr, maxAddr + 1)

    @property
    def device_id(self):
        """Return unique ID of the device, read from firmware."""
        if self._device_id is None:
            self._read_device_id()
        return self._device_id

    @property
    def numberOfSockets(self):
        """Return number of controllable sockets."""
        return len(self._addrMapping)

    @property
    def manufacturer(self):
        """Return the manufacturer as read from the device."""
        return self._dev.manufacturer

    @property
    def name(self):
        """Return the product name as read from the device."""
        return self._dev.product

    def get_status(self, socket: int) -> bool:
        """
        Get the status of the socket given by 'socket'.

        @param socket: socket number
        @return: status
        """
        super().get_status(socket)

        addr = self._addrMapping[socket]
        buf = bytes([3 * addr, 0x03, 0x00, 0x00, 0x00])
        retbuf = self._ctrl_transfer(0xA1, 0x01, 0x0300 + 3 * addr, 0, buf)
        if retbuf is None:
            return False

        return (1 & retbuf[1]) == 1

    def switch_off(self, socket: int) -> None:
        """
        Switch the socket with the given id off.

        @param socket: socket number
        """
        super().switch_off(socket)

        addr = self._addrMapping[socket]
        buf = bytes([3 * addr, 0x00, 0x00, 0x00, 0x00])
        self._ctrl_transfer(0x21, 0x09, 0x0300 + 3 * addr, 0, buf)

    def switch_on(self, socket: int) -> None:
        """
        Switch the socket with the given id on.

        @param socket: socket number
        """
        super().switch_on(socket)

        addr = self._addrMapping[socket]
        buf = bytes([3 * addr, 0x03, 0x00, 0x00, 0x00])
        self._ctrl_transfer(0x21, 0x09, 0x0300 + 3 * addr, 0, buf)

    def _ctrl_transfer(
        self,
        bmRequestType: int,
        bRequest: int,
        wValue: int,
        wIndex: int,
        data_or_wLength: bytes,
    ) -> bytes | None:
        _logger.debug(
            f"ctrl_transfer: {bmRequestType}, {bRequest}, {wValue}, {data_or_wLength!r}"
        )
        for i in range(USB_CTRL_TRANSFER_TRIES):
            try:
                buf = self._dev.ctrl_transfer(
                    bmRequestType,
                    bRequest,
                    wValue,
                    wIndex,
                    data_or_wLength,
                    USB_CTRL_TRANSFER_TIMEOUT,
                )
                if bmRequestType & usb.util.CTRL_IN and len(buf) == 0:
                    continue
            except usb.core.USBError as e:
                _logger.debug(f"ctrl_transfer: try number {i}, usb error: {e}")
                continue
            return buf

        raise USB_IO_ERROR

    def _read_device_id(self):
        buf = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
        id = self._ctrl_transfer(0xA1, 0x01, 0x0301, 0, buf)
        if id:
            self._device_id = ":".join([format(x, "02x") for x in id])
            _logger.debug(f"The device id is: {self.deviceId}")
        _logger.debug("Couldn't read device id")

    @classmethod
    def search_for_devices(cls) -> list[PowerStripUSB]:
        """List the usb devices which have a known EG-PM product_id."""
        devices = []
        for prodId in USB_PRODUCT_IDS:
            devices += [
                cls(dev)
                for dev in usb.core.find(
                    find_all=True, idVendor=USB_VENDOR_ID, idProduct=prodId
                )
            ]
        return devices

    @classmethod
    def get_device(cls, device_id: str) -> PowerStripUSB | None:
        """Try to locate a specific EG-PM device.

        :param deviceId: The device specific firmware id.
        :type deviceId: str
        :return: _description_
        :rtype: PowerStripUSB | None
        """
        candidates = cls.search_for_devices()
        for dev in candidates:
            if dev.deviceId == device_id:
                return dev
        return None

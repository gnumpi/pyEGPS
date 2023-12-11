"""Main pyEGPS tests."""
from __future__ import annotations
from unittest.mock import patch

from pyegps.usb.eg_powerstrip import PowerStripUSB
from pyegps.exceptions import MaximumConnectionTriesReached, MissingLibrary
import pytest

import usb.core


def test_main(fakeUsbDevice):
    """Dummy Test."""
    # check that all device impl have a unique id
    ps = PowerStripUSB(fakeUsbDevice)
    assert ps.manufacturer == "AllFake"

    with pytest.raises(MaximumConnectionTriesReached):
        _ = ps.device_id

    with patch.object(fakeUsbDevice, "ctrl_transfer", return_value=bytes([1, 2, 3])):
        assert ps.device_id == ":".join(
            [ps.get_implementation_id()] + [format(x, "02x") for x in [1, 2, 3]]
        )


def test_main_error_check(fakeUsbDevice):
    """Dummy Test."""
    # check that all device impl have a unique id
    ps = PowerStripUSB(fakeUsbDevice)

    with patch.object(
        fakeUsbDevice,
        "ctrl_transfer",
        return_value=bytes([1, 2, 3]),
        side_effect=usb.core.USBError("Error"),
    ):
        with pytest.raises(MaximumConnectionTriesReached):
            _ = ps.device_id

    with patch("usb.core.find", side_effect=usb.core.NoBackendError("Error")):
        with pytest.raises(MissingLibrary):
            PowerStripUSB.search_for_devices()

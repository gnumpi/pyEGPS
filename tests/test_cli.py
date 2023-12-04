"""Command line interface (cli) tests for pyEGPM."""

from .dummy_devices.powerstrip import DummyPowerStrip
import pyegpm
from pyegpm import cli

pyegpm.DEVICE_IMPLEMENTATIONS = [DummyPowerStrip]


def test_main():
    """Dummy test."""
    devices = DummyPowerStrip.search_for_devices()
    ps = DummyPowerStrip.get_device(devices[0].deviceId)
    ps.switch_on(1)

    assert len(cli.list_devices()) == 2
    assert len(pyegpm.get_all_devices()) == 2

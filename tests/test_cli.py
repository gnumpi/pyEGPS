"""Command line interface (cli) tests for pyEGPM."""
from .dummy_devices.powerstrip import DummyPowerStrip
import pyegpm
from pyegpm import cli

pyegpm.DEVICE_IMPLEMENTATIONS = [DummyPowerStrip]


def test_exit_codes():
    """Checking error handling via exit codes."""
    # Device has socket 3
    assert cli.cli(["--device", "AA:BB:CC", "set", "--on", "3"]) == 0
    # Device has only sockets 0 and 1
    assert cli.cli(["--device", "00:11:22", "set", "--on", "3"]) == 1


def test_outputs(capsys):
    """Checking consistency of setting and reading socket status."""
    # set status and read if it the same
    cli.cli(["--device", "AA:BB:CC", "set", "--on", "0", "2", "--off", "1", "3"])
    cli.cli(["--device", "AA:BB:CC", "status", "0", "1", "2", "3"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "on off on off"

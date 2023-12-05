"""Command line interface (cli) tests for pyEGPS."""
import pyegps
from pyegps import cli

from .dummy_devices.powerstrip import DummyPowerStrip

pyegps.DEVICE_IMPLEMENTATIONS = [DummyPowerStrip]


def test_exit_codes():
    """Checking error handling via exit codes."""
    # Device not found
    assert cli.cli(["--device", "XX:XX:XX:XX", "set", "--on", "0"]) == 1
    # No socket specified
    assert cli.cli(["--device", "00:11:22", "set", "--on"]) == 1
    # Device has socket 3
    assert cli.cli(["--device", "AA:BB:CC", "set", "--on", "3"]) == 0
    # Device has only sockets 0 and 1
    assert cli.cli(["--device", "00:11:22", "set", "--on", "3"]) == 1
    # Correct status request
    assert cli.cli(["--device", "AA:BB:CC", "status", "0", "1", "2", "3"]) == 0
    # Correct status request (no socket given, prints summary)
    assert cli.cli(["--device", "AA:BB:CC", "status"]) == 0
    # Device has no socket 3
    assert cli.cli(["--device", "00:11:22", "status", "0", "1", "2", "3"]) == 1


def test_outputs(capsys):
    """Checking consistency of setting and reading socket status."""
    # set status and read if it the same
    cli.cli(["--device", "AA:BB:CC", "set", "--on", "0", "2", "--off", "1", "3"])
    cli.cli(["--device", "AA:BB:CC", "status", "0", "1", "2", "3"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "on off on off"

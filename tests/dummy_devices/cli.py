"""Allows direct execution of CLI with dummy devices."""

import os
import sys


this_path = os.path.dirname(__file__)
sys.path.append(os.path.join(this_path, "..", "..", "src"))

import pyegps  # noqa
from pyegps import cli  # noqa

from .powerstrip import DummyPowerStrip  # noqa

pyegps.DEVICE_IMPLEMENTATIONS = [DummyPowerStrip]


if __name__ == "__main__":
    sys.exit(cli.cli(sys.argv[1:]))

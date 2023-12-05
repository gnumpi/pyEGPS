"""Using CLI as main entry point."""
from .cli import cli
import sys

sys.exit(cli(sys.argv[1:]))

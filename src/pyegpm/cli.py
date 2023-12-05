"""Simple command line interface for pyEGPM."""
from __future__ import annotations

import argparse

from . import get_all_devices, get_device_types
from .devices import Device
from .exceptions import INVALID_SOCKET_NUMBER


def print_status(dev: Device):
    """Print summary of given device."""
    print(dev.summary())


def list_devices(device_type: str = "all") -> int:
    """Print __repr__() for all devices."""
    for dev in get_all_devices():
        if device_type == "all" or dev.get_device_type() == device_type:
            print(dev)
    return 0


def cli(argList: list[str]) -> int:
    """Command Line Interface (CLI)."""
    parser = argparse.ArgumentParser(
        description="Simple command line interface for controlling Energenie-Power-Strips"
    )

    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument(
        "--device",
        metavar="DEVICE_ID",
        nargs="?",
        help="Specify device[s] to use. Can be omitted if only one device is present.",
    )
    parser.add_argument("--debug", action="store_true", help="Print debug information.")

    # List devices
    list_cmd = subparsers.add_parser("list", help="Search for supported devices.")

    # If several device types are defined, allow filtering by device type
    device_types = get_device_types()
    if len(device_types) > 1:
        list_cmd.add_argument(
            "--type", type=str, choices=["all"] + device_types, default="all"
        )

    set_cmd = subparsers.add_parser("set", help="Set status of sockets.")
    set_cmd.add_argument(
        "--on",
        type=int,
        nargs="*",
        action="append",
        metavar="SOCKET_NR",
        default=[],
        help="Turn SOCKET_NR on.",
    )
    set_cmd.add_argument(
        "--off",
        type=int,
        nargs="*",
        action="append",
        metavar="SOCKET_NR",
        default=[],
        help="Turn SOCKET_NR off.",
    )

    status_cmd = subparsers.add_parser("status", help="Get current device status.")
    status_cmd.add_argument(
        "SOCKET_NR",
        nargs="*",
        type=int,
        help="Status of SOCKET_NR, print summary if no SOCKET_NR is given.",
    )

    args = parser.parse_args(argList)

    if args.command == "list":
        dev_type = args.type if len(device_types) > 1 else "all"
        return list_devices(dev_type)

    devices = get_all_devices()
    # filter devices if requested
    if args.device is not None:
        devices = [d for d in devices if d.deviceId == args.device]

    if len(devices) == 0:
        print(
            "Couldn't find any devices{}.".format(
                f" with ids in {args.device}" if args.device is not None else "!"
            )
        )
        return 1

    if args.command == "set":
        on_sockets = [item for sublist in args.on for item in sublist]
        off_sockets = [item for sublist in args.off for item in sublist]
        if len(on_sockets) + len(off_sockets) == 0:
            print("Please specify at least one --on or --off argument")
            return 1
        for device in devices:
            for socket in on_sockets:
                try:
                    device.switch_on(socket)
                except INVALID_SOCKET_NUMBER:
                    print(
                        f"Device {device} has no socket {socket}. Known sockets: {list(range(device.numberOfSockets))}."
                    )
                    return 1
            for socket in off_sockets:
                try:
                    device.switch_off(socket)
                except INVALID_SOCKET_NUMBER:
                    print(
                        f"Device {device} has no socket {socket}. Known sockets: {list(range(device.numberOfSockets))}."
                    )
                    return 1
        return 0

    elif args.command == "status":
        for device in devices:
            if len(args.SOCKET_NR) == 0:
                print_status(device)
            else:
                status = []
                for socket in args.SOCKET_NR:
                    try:
                        status.append(device.get_status(socket))
                    except INVALID_SOCKET_NUMBER:
                        print(
                            f"Device {device} has no socket {socket}. Known sockets: {list(range(device.numberOfSockets))}."
                        )
                        return 1
                print(" ".join(map(lambda s: "on" if s else "off", status)))
        return 0
    else:
        parser.print_usage()
        return 1

    return 1

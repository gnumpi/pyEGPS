"""Custom Exceptions of pyEGPM."""


class INVALID_SOCKET_NUMBER(Exception):
    """Device has no such socket."""


class USB_IO_ERROR(Exception):
    """Can't access the usb device."""


class UNSUPPORTED_PRODUCT_ID(Exception):
    """Device has an unsupported product id."""

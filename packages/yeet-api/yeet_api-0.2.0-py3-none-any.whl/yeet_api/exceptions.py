# SPDX-License-Identifier: MIT


class InvalidConfigError(Exception):
    """Exception class for a device config that is invalid."""

    pass


class NoSuchDevice(Exception):
    """Exception class for a non-existing device."""

    pass

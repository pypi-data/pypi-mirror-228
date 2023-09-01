# SPDX-License-Identifier: MIT

import os
import json
import logging

from pathlib import Path
from . import CONFIG_DIR

log: logging.Logger = logging.getLogger(__name__)


class _Config:
    """Internal class meant to only be used by yeet-api."""

    def __init__(self):
        self.name: str = os.path.join(CONFIG_DIR, "config.json")
        self._data: dict = {}

        if not Path(self.name).exists():
            with open(self.name, "w") as file:
                json.dump({}, file)

        log.debug(f"Config file path: {self.name}")
        self.read_config()

    def read_config(self) -> None:
        """Update data object by reading from config."""
        log.debug("Reading log file")
        with open(self.name, "r") as file:
            self._data = json.load(file)

    def write_config(self) -> None:
        """Write data object to config file."""
        log.debug("Writing log file")
        with open(self.name, "w") as file:
            json.dump(self._data, file)

    @property
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, data: dict) -> None:
        if isinstance(data, dict):
            self._data = data
        else:
            raise ValueError(f"Expecting dict, got {type(data)} instead")

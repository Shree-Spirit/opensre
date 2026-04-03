"""Analytics event definitions."""

from __future__ import annotations

from enum import StrEnum


class Event(StrEnum):
    COMMAND_COMPLETED = "command_completed"
    INSTALL_DETECTED = "install_detected"

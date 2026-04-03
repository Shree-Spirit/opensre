"""Install analytics entrypoint."""

from __future__ import annotations

from app.analytics.events import Event
from app.analytics.provider import Properties, capture, mark_install_detected

_INSTALL_PROPERTIES: Properties = {
    "install_source": "make_install",
    "entrypoint": "make install",
}


def main() -> int:
    mark_install_detected()
    capture(Event.INSTALL_DETECTED, _INSTALL_PROPERTIES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

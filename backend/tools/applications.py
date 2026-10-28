from __future__ import annotations

from devices.base import Application
from devices.manager import DeviceManager


_device_manager: DeviceManager | None = None


def _get_device_manager() -> DeviceManager:
    global _device_manager

    if _device_manager is None:
        _device_manager = DeviceManager()

    return _device_manager


def open_application(name: str) -> str:
    """
    Open an installed application on the device running the local JARVIS agent.
    """
    try:
        return _get_device_manager().open_application(name)
    except RuntimeError as exc:
        return str(exc)


def refresh_applications() -> str:
    try:
        count = _get_device_manager().refresh_applications()
        return f"Application catalogue refreshed. I found {count} launchable entries, Sir."
    except RuntimeError as exc:
        return str(exc)


def list_applications() -> list[Application]:
    try:
        return _get_device_manager().get_applications()
    except Exception:
        return []

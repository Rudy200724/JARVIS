from __future__ import annotations

import platform

from devices.base import Device
from devices.windows import WindowsDevice


class DeviceManager:
    """
    Chooses the device adapter for the machine JARVIS is currently running on.

    Later, this same manager can route to registered remote device agents:
      - Windows laptop
      - Android phone
      - iPhone companion
    """

    def __init__(self) -> None:
        self.local_device = self._create_local_device()

    @staticmethod
    def _create_local_device() -> Device:
        system = platform.system().lower()

        if system == "windows":
            return WindowsDevice()

        raise RuntimeError(
            f"Local device control is not implemented for {platform.system()} yet."
        )

    def open_application(self, app_name: str) -> str:
        return self.local_device.open_application(app_name)

    def refresh_applications(self) -> int:
        return self.local_device.refresh_applications()

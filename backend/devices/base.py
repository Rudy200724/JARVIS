from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class Application:
    name: str
    launch_target: str
    launch_type: str
    source: str


class Device(ABC):
    """Platform-independent interface for a device JARVIS can control."""

    @abstractmethod
    def find_application(self, query: str) -> Application | None:
        raise NotImplementedError

    @abstractmethod
    def open_application(self, query: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def refresh_applications(self) -> int:
        raise NotImplementedError

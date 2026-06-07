"""
Reality Provider

Defines the normalized runtime reality model used by evidence providers.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class RuntimeReality:
    services: list[dict]
    hosts: list[dict]
    containers: list[dict]
    dependencies: list[dict]
    problems: list[dict] | None = None

    def to_dict(self) -> dict:
        return {
            "services": self.services,
            "hosts": self.hosts,
            "containers": self.containers,
            "dependencies": self.dependencies,
            "problems": self.problems or [],
        }


class RealityProvider(ABC):
    """Base class for runtime reality providers."""

    @abstractmethod
    def get_runtime_reality(self) -> RuntimeReality:
        pass

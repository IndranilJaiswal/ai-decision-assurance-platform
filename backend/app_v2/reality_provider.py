"""
Reality Provider

Provides normalized runtime reality
for evidence collection.

Phase 1 source:
Dynatrace
"""


class RuntimeReality:
    """
    Normalized runtime reality model.

    All external systems should be normalized
    into this structure.
    """

    def __init__(
        self,
        services=None,
        hosts=None,
        dependencies=None,
        containers=None,
    ):
        self.services = services or []
        self.hosts = hosts or []
        self.dependencies = dependencies or []
        self.containers = containers or []


class RealityProvider:
    """
    Base reality provider interface.
    """

    def get_runtime_reality(self):
        raise NotImplementedError

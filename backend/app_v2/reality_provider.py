"""
Reality Provider

Provides normalized runtime reality for evidence collection.

The Evidence Engine should not depend directly on Dynatrace,
AWS, Azure, Kubernetes, or any other vendor API.

External systems should be normalized into RuntimeReality first.
"""


class RuntimeReality:
    """
    Normalized representation of observed operational reality.

    Phase 1 examples:
    - services
    - hosts
    - containers
    - dependencies
    """

    def __init__(
        self,
        services=None,
        hosts=None,
        containers=None,
        dependencies=None,
    ):
        self.services = services or []
        self.hosts = hosts or []
        self.containers = containers or []
        self.dependencies = dependencies or []

    def to_dict(self):
        """Convert RuntimeReality into a dictionary."""

        return {
            "services": self.services,
            "hosts": self.hosts,
            "containers": self.containers,
            "dependencies": self.dependencies,
        }


class RealityProvider:
    """
    Base interface for all reality providers.

    Future providers:
    - DynatraceProvider
    - KubernetesProvider
    - AWSProvider
    - AzureProvider
    - ServiceNowProvider
    """

    def get_runtime_reality(self) -> RuntimeReality:
        """Return normalized runtime reality."""

        raise NotImplementedError(
            "Reality providers must implement get_runtime_reality()."
        )

"""
Mock Dynatrace Provider

Temporary provider used before direct Dynatrace API integration.

It simulates normalized Dynatrace runtime reality.
"""

from reality_provider import RealityProvider, RuntimeReality


class MockDynatraceProvider(RealityProvider):
    """
    Mock provider for local testing.

    This allows us to test the claim → evidence flow
    without calling the Dynatrace API yet.
    """

    def get_runtime_reality(self) -> RuntimeReality:
        """Return sample runtime reality similar to easyTravel."""

        return RuntimeReality(
            services=[
                {
                    "name": "easyTravel Customer Frontend",
                    "entity_type": "SERVICE",
                },
                {
                    "name": "easyTravel Business Backend",
                    "entity_type": "SERVICE",
                },
                {
                    "name": "EasytravelService",
                    "entity_type": "SERVICE",
                },
            ],
            hosts=[
                {
                    "name": "ai-assurance-engine",
                    "entity_type": "HOST",
                }
            ],
            containers=[
                {
                    "name": "easytravel-frontend",
                    "entity_type": "CONTAINER",
                },
                {
                    "name": "easytravel-backend",
                    "entity_type": "CONTAINER",
                },
                {
                    "name": "easytravel-mongodb",
                    "entity_type": "CONTAINER",
                },
            ],
            dependencies=[],
        )

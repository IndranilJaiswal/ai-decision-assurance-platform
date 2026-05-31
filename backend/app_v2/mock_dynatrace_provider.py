"""
Mock Dynatrace Provider

Temporary provider until direct
Dynatrace API integration is added.
"""

from reality_provider import RuntimeReality


class MockDynatraceProvider:
    """
    Provides sample runtime reality.
    """

    def get_runtime_reality(self):

        return RuntimeReality(
            services=[
                {
                    "name": "easyTravel Customer Frontend"
                },
                {
                    "name": "easyTravel Business Backend"
                }
            ],
            dependencies=[],
            hosts=[],
            containers=[]
        )

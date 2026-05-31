"""
Dynatrace Provider

Converts live Dynatrace API data into normalized RuntimeReality.
"""

from dynatrace_client import DynatraceClient
from reality_provider import RealityProvider, RuntimeReality


class DynatraceProvider(RealityProvider):
    """Runtime reality provider backed by Dynatrace."""

    def __init__(self):
        self.client = DynatraceClient()

    def get_runtime_reality(self) -> RuntimeReality:
        """Collect and normalize runtime reality from Dynatrace."""

        services = self._get_services()

        return RuntimeReality(
            services=services,
            hosts=[],
            containers=[],
            dependencies=[],
        )

    def _get_services(self) -> list[dict]:
        """Fetch service entities from Dynatrace."""

        response = self.client.get_entities(
            entity_selector='type("SERVICE")',
            page_size=100,
        )

        services = []

        for entity in response.get("entities", []):

            service_name = entity.get("displayName", "")

            # Ignore Dynatrace-generated technical services.
            if service_name.startswith("Netty on localhost"):
                continue

            if service_name.startswith("Requests on localhost"):
                continue

            # Ignore port-only service names.
            if service_name in [":80", ":8080", ":9079"]:
                continue

            services.append(
                {
                    "id": entity.get("entityId"),
                    "name": service_name,
                    "entity_type": "SERVICE",
                    "raw": entity,
                }
            )

        return services

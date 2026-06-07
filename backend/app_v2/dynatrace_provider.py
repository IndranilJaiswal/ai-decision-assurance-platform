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
        problems = self._get_problems()
        dependencies = self._get_dependencies(services)

        return RuntimeReality(
            services=services,
            hosts=[],
            containers=[],
            dependencies=dependencies,
            problems=problems,
        )

    def _get_services(self) -> list[dict]:
        """Fetch service entities and enrich them with metric evidence."""

        response = self.client.get_entities(
            entity_selector='type("SERVICE")',
            page_size=100,
        )

        services = []

        for entity in response.get("entities", []):

            service_name = entity.get("displayName", "")

            if self._should_ignore_service(service_name):
                continue

            service_id = entity.get("entityId")

            service = {
                "id": service_id,
                "entity_id": service_id,
                "name": service_name,
                "display_name": service_name,
                "entity_type": "SERVICE",
                "raw": entity,
            }

            service.update(
                self._get_service_metrics(service_id)
            )

            services.append(service)

        return services

    def _should_ignore_service(self, service_name: str) -> bool:
        """Filter noisy Dynatrace-generated technical services."""

        if service_name.startswith("Netty on localhost"):
            return True

        if service_name.startswith("Requests on localhost"):
            return True

        if service_name in [":80", ":8080", ":9079"]:
            return True

        return False

    def _get_service_metrics(self, service_id: str) -> dict:
        """
        Query Dynatrace service-level metrics.

        If metric selectors do not match this Dynatrace environment, the
        provider fails safely and returns None.
        """

        entity_selector = f'entityId("{service_id}")'

        return {
            "response_time": self._query_first_metric_value(
                metric_selector="builtin:service.response.time",
                entity_selector=entity_selector,
            ),
            "failure_rate": self._query_first_metric_value(
                metric_selector="builtin:service.errors.total.rate",
                entity_selector=entity_selector,
            ),
            "percentile_latency_p95": self._query_first_metric_value(
                metric_selector="builtin:service.response.time:percentile(95)",
                entity_selector=entity_selector,
            ),
            "percentile_latency_p99": self._query_first_metric_value(
                metric_selector="builtin:service.response.time:percentile(99)",
                entity_selector=entity_selector,
            ),
        }

    def _query_first_metric_value(
        self,
        metric_selector: str,
        entity_selector: str,
    ):
        """Return the first non-null metric value from Dynatrace."""

        try:
            response = self.client.query_metric_data(
                metric_selector=metric_selector,
                entity_selector=entity_selector,
                from_time="now-30m",
                to_time="now",
                resolution="Inf",
            )
        except Exception:
            return None

        result = response.get("result", [])

        if not result:
            return None

        data = result[0].get("data", [])

        if not data:
            return None

        values = data[0].get("values", [])

        for value in values:
            if value is not None:
                return value

        return None

    def _get_problems(self) -> list[dict]:
        """Fetch open problems from Dynatrace."""

        try:
            response = self.client.get_problems()
        except Exception:
            return []

        return response.get("problems", [])

    def _get_dependencies(self, services: list[dict]) -> list[dict]:
        """
        Build lightweight dependency evidence.

        Full Dynatrace service-flow dependency metrics remain future scope.
        This provides dependency_entity evidence when multiple services are
        visible in runtime reality.
        """

        dependencies = []

        if len(services) < 2:
            return dependencies

        for index in range(len(services) - 1):
            source = services[index]
            target = services[index + 1]

            dependencies.append(
                {
                    "source_service": source.get("name"),
                    "target_service": target.get("name"),
                    "source_entity_id": source.get("id"),
                    "target_entity_id": target.get("id"),
                    "dependency_type": "OBSERVED_SERVICE_TOPOLOGY",
                    "call_success_rate": None,
                    "dependency_response_time": None,
                }
            )

        return dependencies

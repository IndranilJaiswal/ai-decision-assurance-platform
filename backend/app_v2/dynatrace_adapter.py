"""
Dynatrace Evidence Adapter

Collects evidence from normalized Dynatrace runtime reality.

Important:
This adapter does not make assurance decisions.
It only converts observed runtime reality into EvidenceRecord objects.
"""

from evidence_records import EvidenceRecord


class DynatraceEvidenceAdapter:
    """Adapter responsible for collecting Dynatrace-backed evidence."""

    def __init__(self, runtime_reality: dict):
        """
        Initialize the adapter with normalized runtime reality.

        runtime_reality is produced by a RealityProvider, such as
        DynatraceProvider. The adapter does not call Dynatrace directly.
        """
        self.runtime_reality = runtime_reality

    def collect(self, evidence_request: object) -> EvidenceRecord:
        """
        Collect evidence for a single evidence request.

        Supported evidence types:
        - service_exists
        - service_entity
        - response_time
        - failure_rate
        - active_problems
        - dependency_entity
        - percentile_latency_p95
        - percentile_latency_p99

        Placeholder evidence types:
        - dependency_call_success_rate
        - dependency_response_time
        """

        if evidence_request.evidence_type == "service_exists":
            return self._collect_service_exists(evidence_request)

        if evidence_request.evidence_type == "service_entity":
            return self._collect_service_entity(evidence_request)

        if evidence_request.evidence_type == "response_time":
            return self._collect_service_metric(
                evidence_request,
                "response_time",
            )

        if evidence_request.evidence_type == "failure_rate":
            return self._collect_service_metric(
                evidence_request,
                "failure_rate",
            )

        if evidence_request.evidence_type == "percentile_latency_p95":
            return self._collect_service_metric(
                evidence_request,
                "percentile_latency_p95",
            )

        if evidence_request.evidence_type == "percentile_latency_p99":
            return self._collect_service_metric(
                evidence_request,
                "percentile_latency_p99",
            )

        if evidence_request.evidence_type == "active_problems":
            return self._collect_active_problems(evidence_request)

        if evidence_request.evidence_type == "dependency_entity":
            return self._collect_dependency_entity(evidence_request)

        if evidence_request.evidence_type == "dependency_call_success_rate":
            return self._collect_dependency_metric_placeholder(
                evidence_request,
                reason=(
                    "Dependency call success rate requires Dynatrace "
                    "service-flow metric integration."
                ),
            )

        if evidence_request.evidence_type == "dependency_response_time":
            return self._collect_dependency_metric_placeholder(
                evidence_request,
                reason=(
                    "Dependency response time requires Dynatrace service "
                    "dependency metric integration."
                ),
            )

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=False,
            value=None,
            details={
                "reason": "Unsupported evidence type.",
            },
        )

    def _find_matching_service(self, target_name: str):
        """
        Find a service in runtime reality.

        Matching is intentionally forgiving for the prototype because
        Dynatrace names may differ slightly from requirement target names.
        """

        services = self.runtime_reality.get("services", [])

        target = target_name.lower()

        for service in services:
            service_name = service.get("name", "").lower()
            display_name = service.get("display_name", "").lower()
            entity_id = service.get("entity_id", "").lower()
            service_id = service.get("id", "").lower()

            if (
                target == service_name
                or target == display_name
                or target in service_name
                or target in display_name
                or target in entity_id
                or target in service_id
            ):
                return service

        return None

    def _collect_service_exists(self, evidence_request: object) -> EvidenceRecord:
        """Check whether the target service exists in runtime reality."""

        matching_service = self._find_matching_service(
            evidence_request.target_name
        )

        observed = matching_service is not None

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=observed,
            value=observed,
            details={
                "matched_service": matching_service,
            },
        )

    def _collect_service_entity(self, evidence_request: object) -> EvidenceRecord:
        """
        Collect the actual Dynatrace service entity.

        This supports claims that need proof that an observable service entity
        exists, not merely a boolean service_exists flag.
        """

        matching_service = self._find_matching_service(
            evidence_request.target_name
        )

        observed = matching_service is not None

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=observed,
            value=matching_service,
            details={
                "matched_service": matching_service,
            },
        )

    def _collect_service_metric(
        self,
        evidence_request: object,
        metric_name: str,
    ) -> EvidenceRecord:
        """
        Collect a service-level metric from normalized runtime reality.

        The DynatraceProvider is responsible for querying Dynatrace and
        attaching metrics to service objects.
        """

        matching_service = self._find_matching_service(
            evidence_request.target_name
        )

        value = None

        if matching_service:
            value = matching_service.get(metric_name)

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=value is not None,
            value=value,
            details={
                "metric": metric_name,
                "matched_service": matching_service,
            },
        )

    def _collect_active_problems(self, evidence_request: object) -> EvidenceRecord:
        """
        Collect active problem evidence from runtime reality.

        If the provider exposes problems, the adapter counts open/active ones.
        """

        problems = self.runtime_reality.get("problems")

        if problems is None:
            return EvidenceRecord(
                claim_id=evidence_request.claim_id,
                target_name=evidence_request.target_name,
                evidence_type=evidence_request.evidence_type,
                source=evidence_request.source,
                observed=False,
                value=None,
                details={
                    "reason": (
                        "Runtime reality does not include Dynatrace problems."
                    ),
                },
            )

        active_problems = [
            problem
            for problem in problems
            if problem.get("status") in ["OPEN", "ACTIVE"]
        ]

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=True,
            value=len(active_problems),
            details={
                "active_problem_count": len(active_problems),
                "active_problems": active_problems,
            },
        )

    def _collect_dependency_entity(self, evidence_request: object) -> EvidenceRecord:
        """
        Collect dependency topology evidence.

        This supports dependency availability claims when normalized runtime
        reality includes dependency relationships.
        """

        dependencies = self.runtime_reality.get("dependencies")

        if dependencies is None:
            return EvidenceRecord(
                claim_id=evidence_request.claim_id,
                target_name=evidence_request.target_name,
                evidence_type=evidence_request.evidence_type,
                source=evidence_request.source,
                observed=False,
                value=None,
                details={
                    "reason": (
                        "Runtime reality does not include dependency topology."
                    ),
                },
            )

        observed = len(dependencies) > 0

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=observed,
            value=len(dependencies),
            details={
                "dependency_count": len(dependencies),
                "dependencies": dependencies,
            },
        )

    def _collect_dependency_metric_placeholder(
        self,
        evidence_request: object,
        reason: str,
    ) -> EvidenceRecord:
        """
        Return a placeholder evidence record for dependency metrics.

        Dependency metrics remain a future Dynatrace MCP enhancement.
        """

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=False,
            value=None,
            details={
                "reason": reason,
            },
        )

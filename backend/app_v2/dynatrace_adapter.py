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

        runtime_reality is produced by a RealityProvider, such as DynatraceProvider.
        The adapter does not call Dynatrace directly.
        """
        self.runtime_reality = runtime_reality

    def collect(self, evidence_request: object) -> EvidenceRecord:
        """
        Collect evidence for a single evidence request.

        Supported evidence types:
        - service_exists

        Placeholder evidence types:
        - response_time
        - failure_rate

        The placeholders intentionally return observed=False until
        live Dynatrace metrics are implemented.
        """

        if evidence_request.evidence_type == "service_exists":
            return self._collect_service_exists(evidence_request)

        if evidence_request.evidence_type == "response_time":
            return self._collect_metric_placeholder(
                evidence_request,
                reason="Response time metric collection is not implemented yet.",
            )

        if evidence_request.evidence_type == "failure_rate":
            return self._collect_metric_placeholder(
                evidence_request,
                reason="Failure rate metric collection is not implemented yet.",
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

    def _collect_service_exists(self, evidence_request: object) -> EvidenceRecord:
        """Check whether the target service exists in runtime reality."""

        services = self.runtime_reality.get("services", [])

        matching_service = next(
            (
                service
                for service in services
                if service["name"].lower() == evidence_request.target_name.lower()
            ),
            None,
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

    def _collect_metric_placeholder(
        self,
        evidence_request: object,
        reason: str,
    ) -> EvidenceRecord:
        """
        Return a placeholder evidence record for metrics not yet collected.

        This is deliberate.

        It allows the Assurance Engine to demonstrate that a claim
        cannot be justified when required evidence is missing.
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

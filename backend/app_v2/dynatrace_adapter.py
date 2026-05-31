"""
Dynatrace Evidence Adapter

Collects evidence from Dynatrace for evidence requests.
"""

from evidence_records import EvidenceRecord


class DynatraceEvidenceAdapter:
    """Adapter responsible for collecting Dynatrace-backed evidence."""

    def __init__(self, runtime_reality: dict):
        """
        For Phase 1B, we start with normalized runtime reality.

        Later, this will call the Dynatrace API directly.
        """
        self.runtime_reality = runtime_reality

    def collect(self, evidence_request: object) -> EvidenceRecord:
        """Collect evidence for a single evidence request."""

        if evidence_request.evidence_type == "service_exists":
            return self._collect_service_exists(evidence_request)

        return EvidenceRecord(
            claim_id=evidence_request.claim_id,
            target_name=evidence_request.target_name,
            evidence_type=evidence_request.evidence_type,
            source=evidence_request.source,
            observed=False,
            value=None,
            details={
                "reason": "Unsupported evidence type"
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
                "matched_service": matching_service
            },
        )

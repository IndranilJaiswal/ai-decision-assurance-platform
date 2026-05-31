"""
Evidence Collection Engine

Coordinates evidence collection for approved claims.

Responsibilities:

1. Generate evidence requests.
2. Collect evidence.
3. Return evidence records.

The engine does not make assurance decisions.
"""

from evidence_request_builder import EvidenceRequestBuilder


class EvidenceCollectionEngine:
    """
    Coordinates evidence collection.
    """

    def __init__(self, evidence_adapter):
        self.evidence_adapter = evidence_adapter
        self.request_builder = EvidenceRequestBuilder()

    def collect_evidence(self, approved_claim):
        """
        Collect all evidence required for an approved claim.
        """

        requests = self.request_builder.build_requests(
            approved_claim
        )

        evidence_records = []

        for request in requests:

            evidence_record = self.evidence_adapter.collect(
                request
            )

            evidence_records.append(
                evidence_record
            )

        return evidence_records

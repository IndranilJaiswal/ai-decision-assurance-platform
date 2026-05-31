"""
Evidence Request Builder

Converts an approved claim into
specific evidence requests.
"""

from evidence_models import EvidenceRequest


class EvidenceRequestBuilder:
    """Builds evidence requests from approved claims."""

    def build_requests(self, approved_claim):
        requests = []

        for evidence_type in approved_claim.claim.evidence_required:

            requests.append(
                EvidenceRequest(
                    claim_id=approved_claim.claim.claim_id,
                    target_name=approved_claim.target_name,
                    evidence_type=evidence_type,
                    source="dynatrace"
                )
            )

        return requests

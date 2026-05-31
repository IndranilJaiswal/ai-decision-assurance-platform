"""
Claim Assurance Engine

Evaluates whether collected evidence supports an approved claim.

Phase 1C supports SERVICE_EXISTS first.
"""


from assurance_models import AssuranceResult


class ClaimAssuranceEngine:
    """Evaluates evidence records against approved claims."""

    def evaluate(self, approved_claim, evidence_records) -> AssuranceResult:
        """Evaluate an approved claim using collected evidence records."""

        required_evidence = approved_claim.claim.evidence_required

        collected_types = [
            evidence.evidence_type
            for evidence in evidence_records
        ]

        missing_evidence = [
            evidence_type
            for evidence_type in required_evidence
            if evidence_type not in collected_types
        ]

        if missing_evidence:
            return AssuranceResult(
                claim_id=approved_claim.claim.claim_id,
                target_name=approved_claim.target_name,
                status="INSUFFICIENT_EVIDENCE",
                confidence=0.0,
                evidence_gaps=missing_evidence,
                explanation="Required evidence is missing.",
            )

        if approved_claim.claim.claim_id == "SERVICE_EXISTS":
            return self._evaluate_service_exists(
                approved_claim,
                evidence_records
            )

        return AssuranceResult(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            status="INSUFFICIENT_EVIDENCE",
            confidence=0.0,
            evidence_gaps=[],
            explanation="No assurance rule is implemented for this claim.",
        )

    def _evaluate_service_exists(self, approved_claim, evidence_records):
        """Evaluate SERVICE_EXISTS using service_exists evidence."""

        service_exists_record = next(
            evidence
            for evidence in evidence_records
            if evidence.evidence_type == "service_exists"
        )

        if service_exists_record.observed is True:
            return AssuranceResult(
                claim_id=approved_claim.claim.claim_id,
                target_name=approved_claim.target_name,
                status="VERIFIED",
                confidence=1.0,
                evidence_gaps=[],
                explanation="Service was observed in runtime reality.",
            )

        return AssuranceResult(
            claim_id=approved_claim.claim.claim_id,
            target_name=approved_claim.target_name,
            status="FAILED",
            confidence=1.0,
            evidence_gaps=[],
            explanation="Service was not observed in runtime reality.",
        )

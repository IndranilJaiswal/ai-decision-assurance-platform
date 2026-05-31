"""
Test Assurance Explanation Engine

Purpose:
Validate deterministic explanation generation from requirement assurance.
"""

from assurance_explanation_engine import AssuranceExplanationEngine
from requirement_assurance_models import RequirementAssuranceResult


class MockClaimResult:
    """Lightweight mock claim result for explanation testing."""

    def __init__(self, claim_id, status, evidence_gaps):
        self.claim_id = claim_id
        self.status = status
        self.evidence_gaps = evidence_gaps


def main():
    """Run explanation test."""

    requirement_result = RequirementAssuranceResult(
        requirement_id="REQ-002",
        title="Customer booking service must remain healthy",
        status="PARTIALLY_ASSURED",
        verified_claims=1,
        insufficient_claims=1,
        failed_claims=0,
        claim_results=[
            MockClaimResult(
                claim_id="SERVICE_EXISTS",
                status="VERIFIED",
                evidence_gaps=[],
            ),
            MockClaimResult(
                claim_id="SERVICE_HEALTHY",
                status="INSUFFICIENT_EVIDENCE",
                evidence_gaps=[
                    "response_time",
                    "failure_rate",
                ],
            ),
        ],
        explanation=(
            "One or more supporting claims have insufficient evidence."
        ),
    )

    engine = AssuranceExplanationEngine()
    explanation = engine.explain(requirement_result)

    print("\nAI Assurance Explanation")
    print("=" * 80)
    print("Title:", explanation.title)
    print("Summary:", explanation.summary)

    print("\nDetails")
    for detail in explanation.details:
        print("-", detail)

    print("\nRecommendations")
    for recommendation in explanation.recommendations:
        print("-", recommendation)


if __name__ == "__main__":
    main()

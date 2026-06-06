"""
Claim Review Package Builder

Purpose:
Builds explainable claim review packages for PML approval.

Inputs:
- ClaimSuggestion
- CoverageGapDetector
- MongoDB knowledge sources

Output:
- ClaimReviewPackage

This module does not approve claims.
It only prepares decision context.
"""

from claim_review_models import ClaimReviewPackage
from coverage_gap_detector import CoverageGapDetector


class ClaimReviewPackageBuilder:
    """Build PML review packages for suggested claims."""

    def __init__(self):
        self.coverage_gap_detector = CoverageGapDetector()

    def build(self, suggestion) -> ClaimReviewPackage:
        """Build a review package for one claim suggestion."""

        gap = self.coverage_gap_detector.detect(
            suggestion.claim_id
        )

        coverage_status = (
            "COVERAGE_GAP"
            if gap
            else "SUPPORTED"
        )

        return ClaimReviewPackage(
            claim_id=suggestion.claim_id,
            requirement=suggestion.requirement,
            category=self._infer_category(suggestion.claim_id),
            rationale=self._build_rationale(suggestion.claim_id),
            business_impact=self._build_business_impact(suggestion.claim_id),
            relevant_policies=[
                suggestion.policy_name,
            ],
            relevant_standards=[
                "Internal Secure Development Lifecycle Guidance",
            ],
            coverage_status=coverage_status,
            coverage_gap_reason=gap.reason if gap else None,
        )

    def _infer_category(self, claim_id: str) -> str:
        """Infer simple assurance category from claim name."""

        if "SERVICE" in claim_id:
            return "Availability"

        if "DEPENDENC" in claim_id:
            return "Architecture Dependency"

        if "LATENCY" in claim_id:
            return "Performance"

        if "RECOVERY" in claim_id:
            return "Resilience"

        return "General Assurance"

    def _build_rationale(self, claim_id: str) -> str:
        """Create a human-readable rationale."""

        return (
            f"{claim_id} was suggested because it may be required "
            "to assure the stated requirement."
        )

    def _build_business_impact(self, claim_id: str) -> str:
        """Create a simple business impact explanation."""

        return (
            f"If {claim_id} is not assured, the requirement may not be "
            "fully supported by observable evidence."
        )

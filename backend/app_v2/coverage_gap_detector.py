"""
Coverage Gap Detector

Purpose:
---------
Determines whether a suggested claim
exists in the executable claim library.

If not, a CoverageGap is generated.

Author:
-------
Indranil Jaiswal
AI Assurance Platform
"""

from coverage_gap_models import CoverageGap
from claim_library import load_claim_library


class CoverageGapDetector:
    """
    Detects claims not currently supported
    by the Assurance Engine.
    """

    def __init__(self):

        self.claims = load_claim_library()

        self.claim_ids = {
            claim.claim_id
            for claim in self.claims
        }

    def detect(self, claim_id: str):

        if claim_id in self.claim_ids:
            return None

        return CoverageGap(
            claim_id=claim_id,
            reason=(
                "No executable claim definition "
                "exists in the claim library."
            ),
        )

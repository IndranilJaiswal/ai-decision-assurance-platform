"""
test_claim_discovery_agent.py

Purpose:
---------
Validate requirement-to-claim discovery and coverage gap detection.

Workflow:
---------
Requirement
↓
Gemini Claim Discovery Agent
↓
ClaimSuggestion
↓
CoverageGapDetector
↓
Supported Claim or Coverage Gap
"""

from claim_discovery_agent import ClaimDiscoveryAgent
from coverage_gap_detector import CoverageGapDetector


agent = ClaimDiscoveryAgent()
gap_detector = CoverageGapDetector()

suggestions = agent.discover(
    "Booking service must remain available."
)

print("\n==============================")
print("CLAIM DISCOVERY + COVERAGE GAP TEST")
print("==============================")

for suggestion in suggestions:

    gap = gap_detector.detect(
        suggestion.claim_id
    )

    if gap:
        print(
            f"{suggestion.claim_id} -> COVERAGE GAP"
        )
        print(
            f"Reason: {gap.reason}"
        )
    else:
        print(
            f"{suggestion.claim_id} -> SUPPORTED"
        )

    print()

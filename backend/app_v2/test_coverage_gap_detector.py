"""
Coverage Gap Detector Tests

Purpose:
---------
Validate detection of unsupported claims.

Expected Results:
-----------------

SERVICE_EXISTS
→ No Coverage Gap

SERVICE_HEALTHY
→ No Coverage Gap

REDIS_AVAILABLE
→ Coverage Gap

POSTGRESQL_AVAILABLE
→ Coverage Gap
"""

from coverage_gap_detector import CoverageGapDetector

detector = CoverageGapDetector()

test_claims = [
    "SERVICE_EXISTS",
    "SERVICE_HEALTHY",
    "REDIS_AVAILABLE",
    "POSTGRESQL_AVAILABLE",
]

print("\n==============================")
print("COVERAGE GAP TEST")
print("==============================")

for claim in test_claims:

    gap = detector.detect(claim)

    if gap:
        print(
            f"{claim} -> COVERAGE GAP"
        )
    else:
        print(
            f"{claim} -> SUPPORTED"
        )

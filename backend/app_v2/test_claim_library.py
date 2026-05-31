"""
Test Claim Library

Temporary test script to verify that claims load correctly.
"""

from claim_library import load_claim_library


claims = load_claim_library()

for claim in claims:
    print(
        f"{claim.claim_id} | "
        f"{claim.name} | "
        f"{claim.entity_type} | "
        f"{claim.evidence_required}"
    )

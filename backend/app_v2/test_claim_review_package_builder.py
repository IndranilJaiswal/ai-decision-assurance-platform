"""
Test Claim Review Package Builder

Purpose:
Validate that discovered claims can be converted into
PML-reviewable packages.
"""

from claim_discovery_agent import ClaimDiscoveryAgent
from claim_review_package_builder import ClaimReviewPackageBuilder


agent = ClaimDiscoveryAgent()
builder = ClaimReviewPackageBuilder()

suggestions = agent.discover(
    "Booking service must remain available."
)

print("\n==============================")
print("PML CLAIM REVIEW PACKAGES")
print("==============================")

for suggestion in suggestions:

    package = builder.build(suggestion)

    print()
    print("Claim:", package.claim_id)
    print("Category:", package.category)
    print("Coverage:", package.coverage_status)
    print("Rationale:", package.rationale)
    print("Business Impact:", package.business_impact)
    print("Policies:", package.relevant_policies)
    print("Standards:", package.relevant_standards)

    if package.coverage_gap_reason:
        print("Coverage Gap Reason:", package.coverage_gap_reason)

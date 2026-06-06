"""
Test script for PML governance routing.

This validates that:
- Supported claims go toward PML approval and then SDL execution.
- Coverage gaps go toward PML governance classification.
"""

from dataclasses import dataclass

from pml_governance_router import route_claim_review_package


@dataclass
class MockClaimReviewPackage:
    claim_id: str
    category: str
    coverage_status: str


def main():
    packages = [
        MockClaimReviewPackage(
            claim_id="DEPENDENCY_AVAILABLE",
            category="Architecture Dependency",
            coverage_status="SUPPORTED",
        ),
        MockClaimReviewPackage(
            claim_id="CAPACITY_SUFFICIENT",
            category="Capacity Management",
            coverage_status="SUPPORTED",
        ),
        MockClaimReviewPackage(
            claim_id="NETWORK_REACHABLE",
            category="General Assurance",
            coverage_status="COVERAGE_GAP",
        ),
        MockClaimReviewPackage(
            claim_id="DATABASE_ACCESSIBLE",
            category="General Assurance",
            coverage_status="COVERAGE_GAP",
        ),
    ]

    print("\n==============================")
    print("PML GOVERNANCE ROUTING")
    print("==============================\n")

    for package in packages:
        route = route_claim_review_package(package)

        print(f"Claim: {package.claim_id}")
        print(f"Category: {package.category}")
        print(f"Coverage: {package.coverage_status}")
        print(f"Governance Route: {route}")
        print("")


if __name__ == "__main__":
    main()

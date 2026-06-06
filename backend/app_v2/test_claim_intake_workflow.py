"""
Test script for Claim Intake Workflow.
"""

from dataclasses import dataclass

from claim_intake_workflow import ClaimIntakeWorkflow
from claim_registry import InMemoryClaimRegistry


@dataclass
class MockClaimReviewPackage:
    claim_id: str
    category: str
    coverage_status: str


def main():
    registry = InMemoryClaimRegistry()
    workflow = ClaimIntakeWorkflow(registry)

    packages = [
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
    ]

    print("\n==============================")
    print("CLAIM INTAKE WORKFLOW")
    print("==============================\n")

    for package in packages:
        result = workflow.intake_claim(
            package=package,
            requirement_id="REQ-001",
        )

        print(f"Claim: {result.claim_id}")
        print(f"Coverage: {result.coverage_status}")
        print(f"Governance Route: {result.governance_route}")
        print(f"Lifecycle State: {result.lifecycle_state.value}")
        print(f"Registry Status: CREATED")
        print("")


if __name__ == "__main__":
    main()

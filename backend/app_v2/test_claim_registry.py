"""
Test script for Claim Registry.
"""

from claim_lifecycle_state_machine import ClaimLifecycleState
from claim_registry import InMemoryClaimRegistry


def main():
    registry = InMemoryClaimRegistry()

    claim = registry.create_claim_instance(
        claim_id="CAPACITY_SUFFICIENT",
        requirement_id="REQ-001",
    )

    registry.update_claim_state(
        claim_instance_id=claim.claim_instance_id,
        new_state=ClaimLifecycleState.PML_REVIEW_REQUIRED,
    )

    pml_claims = registry.list_by_state(
        ClaimLifecycleState.PML_REVIEW_REQUIRED
    )

    print("\n==============================")
    print("CLAIM REGISTRY")
    print("==============================\n")

    print("Created Claim Instance:")
    print(registry.to_dict(claim))

    print("\nClaims Waiting for PML Review:")
    for item in pml_claims:
        print(registry.to_dict(item))


if __name__ == "__main__":
    main()

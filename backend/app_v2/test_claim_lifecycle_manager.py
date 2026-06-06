from datetime import datetime

from claim_lifecycle_manager import (
    ClaimInstance,
    ClaimLifecycleManager,
)

from claim_lifecycle_state_machine import (
    ClaimLifecycleState,
)


def main():

    claim = ClaimInstance(
        claim_id="CAPACITY_SUFFICIENT",
        requirement_id="REQ-001",
        state=ClaimLifecycleState.DISCOVERED,
        created_at=datetime.utcnow(),
    )

    manager = ClaimLifecycleManager()

    print("\n==============================")
    print("CLAIM LIFECYCLE MANAGER")
    print("==============================\n")

    print("Initial State:")
    print(claim.state.value)

    claim = manager.transition(
        claim,
        ClaimLifecycleState.PML_REVIEW_REQUIRED,
    )

    print("\nAfter Transition:")
    print(claim.state.value)

    try:
        manager.transition(
            claim,
            ClaimLifecycleState.VERIFIED,
        )

    except ValueError as ex:
        print("\nExpected Validation:")
        print(ex)


if __name__ == "__main__":
    main()

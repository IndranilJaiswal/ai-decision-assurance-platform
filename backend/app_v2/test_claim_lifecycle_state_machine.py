"""
Test script for Claim Lifecycle State Machine.
"""

from claim_lifecycle_state_machine import ClaimLifecycleState, can_transition


def main():
    test_cases = [
        (
            ClaimLifecycleState.DISCOVERED,
            ClaimLifecycleState.PML_REVIEW_REQUIRED,
        ),
        (
            ClaimLifecycleState.PML_REVIEW_REQUIRED,
            ClaimLifecycleState.PML_APPROVED,
        ),
        (
            ClaimLifecycleState.PML_APPROVED,
            ClaimLifecycleState.SDL_REVIEW_REQUIRED,
        ),
        (
            ClaimLifecycleState.SDL_APPROVED,
            ClaimLifecycleState.APPROVED_FOR_ASSURANCE,
        ),
        (
            ClaimLifecycleState.DISCOVERED,
            ClaimLifecycleState.SDL_APPROVED,
        ),
    ]

    print("\n==============================")
    print("CLAIM LIFECYCLE STATE MACHINE")
    print("==============================\n")

    for current_state, next_state in test_cases:
        allowed = can_transition(current_state, next_state)

        print(f"{current_state.value} -> {next_state.value}")
        print(f"Allowed: {allowed}")
        print("")


if __name__ == "__main__":
    main()

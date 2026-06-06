"""
Claim Lifecycle Manager

Owns lifecycle state transitions for claim instances.

The lifecycle manager is the only component allowed to
change claim state.
"""

from dataclasses import dataclass
from datetime import datetime

from claim_lifecycle_state_machine import (
    ClaimLifecycleState,
    can_transition,
)


@dataclass
class ClaimInstance:
    """
    Runtime instance of a claim.

    A claim definition may exist once in the library,
    but many claim instances may be created over time.
    """

    claim_id: str
    requirement_id: str
    state: ClaimLifecycleState
    created_at: datetime


class ClaimLifecycleManager:
    """
    Manages lifecycle transitions.
    """

    def transition(
        self,
        claim: ClaimInstance,
        new_state: ClaimLifecycleState,
    ):
        """
        Move a claim to a new lifecycle state.

        Raises:
            ValueError if transition is invalid.
        """

        if not can_transition(claim.state, new_state):
            raise ValueError(
                f"Invalid transition: "
                f"{claim.state.value} -> {new_state.value}"
            )

        claim.state = new_state

        return claim

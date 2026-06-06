"""
Claim Lifecycle State Machine

Defines allowed lifecycle states and transitions for assurance claims.

This prevents claims from jumping directly from AI discovery into execution
or assurance without governance approval.
"""

from enum import Enum


class ClaimLifecycleState(str, Enum):
    DISCOVERED = "DISCOVERED"
    PML_REVIEW_REQUIRED = "PML_REVIEW_REQUIRED"
    PML_APPROVED = "PML_APPROVED"
    PML_CLASSIFIED_NEW_GOVERNANCE_CLAIM = "PML_CLASSIFIED_NEW_GOVERNANCE_CLAIM"
    PML_REJECTED = "PML_REJECTED"
    PML_DEFERRED = "PML_DEFERRED"
    SDL_REVIEW_REQUIRED = "SDL_REVIEW_REQUIRED"
    SDL_APPROVED = "SDL_APPROVED"
    APPROVED_FOR_ASSURANCE = "APPROVED_FOR_ASSURANCE"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


ALLOWED_TRANSITIONS = {
    ClaimLifecycleState.DISCOVERED: [
        ClaimLifecycleState.PML_REVIEW_REQUIRED,
    ],
    ClaimLifecycleState.PML_REVIEW_REQUIRED: [
        ClaimLifecycleState.PML_APPROVED,
        ClaimLifecycleState.PML_CLASSIFIED_NEW_GOVERNANCE_CLAIM,
        ClaimLifecycleState.PML_REJECTED,
        ClaimLifecycleState.PML_DEFERRED,
    ],
    ClaimLifecycleState.PML_APPROVED: [
        ClaimLifecycleState.SDL_REVIEW_REQUIRED,
    ],
    ClaimLifecycleState.SDL_REVIEW_REQUIRED: [
        ClaimLifecycleState.SDL_APPROVED,
    ],
    ClaimLifecycleState.SDL_APPROVED: [
        ClaimLifecycleState.APPROVED_FOR_ASSURANCE,
    ],
    ClaimLifecycleState.APPROVED_FOR_ASSURANCE: [
        ClaimLifecycleState.VERIFIED,
        ClaimLifecycleState.FAILED,
        ClaimLifecycleState.INSUFFICIENT_EVIDENCE,
    ],
}


def can_transition(
    current_state: ClaimLifecycleState,
    next_state: ClaimLifecycleState,
) -> bool:
    """
    Returns True if a claim is allowed to move from current_state
    to next_state.
    """

    return next_state in ALLOWED_TRANSITIONS.get(current_state, [])

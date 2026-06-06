"""
Governance Decision Model

This module defines the formal decision states used by the AI Decision
Assurance Platform.

Key principle:
- PML owns assurance intent.
- SDL owns execution/remediation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PMLDecision(str, Enum):
    """
    Product / Portfolio / Platform Management decision.

    PML decides whether a discovered claim is valid from a governance
    and assurance-intent perspective.
    """

    APPROVE_EXISTING_CLAIM = "APPROVE_EXISTING_CLAIM"
    CLASSIFY_NEW_GOVERNANCE_CLAIM = "CLASSIFY_NEW_GOVERNANCE_CLAIM"
    REJECT_CLAIM = "REJECT_CLAIM"
    DEFER_CLAIM = "DEFER_CLAIM"


class SDLDecision(str, Enum):
    """
    Software Design Leader decision.

    SDL only acts on claims that are already approved by PML and are
    ready for execution, remediation, or implementation workflow.
    """

    APPROVE_EXECUTION = "APPROVE_EXECUTION"
    REJECT_EXECUTION = "REJECT_EXECUTION"
    REQUEST_CHANGES = "REQUEST_CHANGES"


@dataclass
class GovernanceDecision:
    """
    Captures the governance decision state for a discovered claim.

    A claim may first require PML governance classification before it
    can ever reach SDL execution.
    """

    claim_id: str
    claim_category: str
    coverage_status: str
    pml_decision: Optional[PMLDecision] = None
    sdl_decision: Optional[SDLDecision] = None
    rationale: Optional[str] = None

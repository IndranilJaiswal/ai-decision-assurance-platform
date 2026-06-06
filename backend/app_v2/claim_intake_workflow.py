"""
Claim Intake Workflow

Turns claim review packages into governed claim instances.

This is the first orchestration layer in the Governance Plane.
It connects:
- Coverage assessment
- PML governance routing
- Claim lifecycle state
- Claim registry persistence
"""

from dataclasses import dataclass

from claim_lifecycle_state_machine import ClaimLifecycleState
from claim_registry import InMemoryClaimRegistry
from pml_governance_router import route_claim_review_package


@dataclass
class ClaimIntakeResult:
    """
    Result produced after a claim review package enters intake.
    """

    claim_instance_id: str
    claim_id: str
    requirement_id: str
    coverage_status: str
    governance_route: str
    lifecycle_state: ClaimLifecycleState


class ClaimIntakeWorkflow:
    """
    Orchestrates initial claim intake.

    Every discovered claim enters PML review first.
    The governance route determines whether the claim is:
    - an existing supported claim requiring PML approval
    - a coverage gap requiring PML governance classification
    """

    def __init__(self, registry: InMemoryClaimRegistry):
        self.registry = registry

    def intake_claim(
        self,
        package,
        requirement_id: str,
    ) -> ClaimIntakeResult:
        """
        Convert a claim review package into a claim registry instance.
        """

        governance_route = route_claim_review_package(package)

        claim_instance = self.registry.create_claim_instance(
            claim_id=package.claim_id,
            requirement_id=requirement_id,
            initial_state=ClaimLifecycleState.PML_REVIEW_REQUIRED,
        )

        return ClaimIntakeResult(
            claim_instance_id=claim_instance.claim_instance_id,
            claim_id=claim_instance.claim_id,
            requirement_id=claim_instance.requirement_id,
            coverage_status=package.coverage_status,
            governance_route=governance_route,
            lifecycle_state=claim_instance.state,
        )

"""
Test Human Approval Workflow

Purpose:
Validate Requirement → Policy Agent → Suggested Claims → Human Approval.

This test does not run evidence collection yet.
It only verifies that suggested claims can be approved into assurance scope.
"""

from availability_policy_agent import AvailabilityPolicyAgent
from claim_approval_engine import ClaimApprovalEngine


def main():

    requirement = "Customer booking service must remain available."

    agent = AvailabilityPolicyAgent()
    suggestions = agent.suggest_claims(requirement)

    approval_engine = ClaimApprovalEngine()

    approved_claims = approval_engine.approve_claims(
        suggestions=suggestions,
        approved_claim_ids=[
            "SERVICE_EXISTS",
            "SERVICE_HEALTHY",
        ],
    )

    print("\nSuggested Claims")
    print("=" * 80)

    for suggestion in suggestions:

        approval_status = "APPROVED" if suggestion.approved else "NOT APPROVED"

        print()
        print(f"Claim: {suggestion.claim_id}")
        print(f"Status: {approval_status}")
        print(f"Policy: {suggestion.policy_name}")
        print(f"Objective: {suggestion.objective_id}")
        print(f"Reason: {suggestion.objective_description}")

    print("\nApproved Claims")
    print("=" * 80)

    for claim in approved_claims:
        print(f"- {claim.claim_id}")


if __name__ == "__main__":
    main()

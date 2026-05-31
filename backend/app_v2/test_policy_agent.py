"""
Policy Agent Test

Purpose:
Validate policy-based claim discovery.
"""

from availability_policy_agent import AvailabilityPolicyAgent


def main():

    agent = AvailabilityPolicyAgent()

    claims = agent.suggest_claims(
        "Customer booking service must remain available."
    )

    print("\nSuggested Claims")
    print("=" * 80)

    for claim in claims:

        print(f"\nClaim ID: {claim['claim_id']}")
        print(f"Policy: {claim['policy_name']}")
        print(f"Objective: {claim['objective_id']}")
        print(f"Reason: {claim['objective_description']}")


if __name__ == "__main__":
    main()

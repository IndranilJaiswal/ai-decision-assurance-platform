"""
Test script for PML Claim Mapping Agent.
"""

from claim_library import load_claim_library
from pml_claim_mapping_agent import PMLClaimMappingAgent


def main():
    claims = load_claim_library()

    governed_claims = [
        claim.claim_id
        for claim in claims
    ]

    agent = PMLClaimMappingAgent()

    result = agent.recommend_mapping(
        discovered_claim="LATENCY_WITHIN_THRESHOLD",
        governed_claims=governed_claims,
    )

    print("\n==============================")
    print("PML CLAIM MAPPING AGENT")
    print("==============================\n")

    print("Discovered Claim:")
    print("LATENCY_WITHIN_THRESHOLD")

    print("\nMapping Recommendation:")
    print(result)


if __name__ == "__main__":
    main()

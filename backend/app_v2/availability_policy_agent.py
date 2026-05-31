"""
Availability Policy Agent

Purpose:
Translate approved policy objectives into candidate assurance claims.

Responsibilities:
- Read approved organizational policies
- Generate candidate claims
- Attach policy traceability

Important:
The agent does NOT approve claims.
The agent does NOT collect evidence.
The agent does NOT perform assurance.

Future Evolution:
Replace deterministic claim discovery with LLM-assisted
policy interpretation while preserving the same output schema.
"""

from claim_suggestion_models import ClaimSuggestion
from policy_loader import load_policy


class AvailabilityPolicyAgent:
    """
    Policy-bound claim discovery agent.
    """

    POLICY_PATH = (
        "backend/app_v2/config/policies/"
        "service_availability_policy.yaml"
    )

    def suggest_claims(self, requirement_text: str) -> list[ClaimSuggestion]:
        """
        Suggest claims for a requirement.

        Current Behavior:
        Returns all claims associated with the policy.

        Future Behavior:
        Use an LLM to match the requirement text to the most relevant
        policy objectives while keeping the output model unchanged.
        """

        policy = load_policy(self.POLICY_PATH)

        suggestions = []

        for objective in policy.objectives:

            for claim_id in objective.suggested_claims:

                suggestions.append(
                    ClaimSuggestion(
                        claim_id=claim_id,
                        policy_id=policy.policy_id,
                        policy_name=policy.name,
                        objective_id=objective.objective_id,
                        objective_description=objective.description,
                        requirement=requirement_text,
                        approved=False,
                    )
                )

        return suggestions

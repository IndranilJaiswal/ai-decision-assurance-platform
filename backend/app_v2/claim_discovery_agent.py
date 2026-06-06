"""
claim_discovery_agent.py

Purpose:
---------
Convert requirements into ClaimSuggestion
objects using Gemini reasoning.

Workflow:
----------
Requirement
↓
Knowledge Retrieval
↓
Gemini
↓
ClaimSuggestion

Author:
-------
Indranil Jaiswal
AI Assurance Platform
"""

from gemini_client import GeminiClient
from knowledge_retriever import KnowledgeRetriever
from claim_suggestion_models import ClaimSuggestion


class ClaimDiscoveryAgent:

    def __init__(self):

        self.gemini = GeminiClient()
        self.retriever = KnowledgeRetriever()

    def discover(self, requirement: str):

        claim_patterns = (
            self.retriever.get_claim_patterns()
        )

        known_claims = [
            pattern["claim_name"]
            for pattern in claim_patterns
        ]

        prompt = f"""
You are an assurance architect.

Requirement:
{requirement}

Known Claims:
{", ".join(known_claims)}

Task:
Suggest claims needed to assure the requirement.

Rules:
- Return one claim ID per line.
- Use uppercase claim naming.
- Do not explain.
"""

        response = self.gemini.generate(prompt)

        suggestions = []

        for line in response.splitlines():

            claim_id = line.strip()

            if not claim_id:
                continue

            suggestions.append(
                ClaimSuggestion(
                    claim_id=claim_id,
                    policy_id="AI_DISCOVERY",
                    policy_name="Gemini Discovery Agent",
                    objective_id="REQ_DISCOVERY",
                    objective_description=(
                        "Requirement decomposition"
                    ),
                    requirement=requirement,
                )
            )

        return suggestions

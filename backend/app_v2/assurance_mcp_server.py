"""
assurance_mcp_server.py

MCP server for the AI Decision Assurance Platform.

Purpose:
Expose the core Reason → Plan → Act workflow as agent-callable MCP tools.

Tools:
- discover_claims: Gemini reasoning layer
- map_claim: Gemini/PML planning layer
- request_dynatrace_evidence: Observability action layer

This server does not bypass PML governance.
It exposes agent tools that support the governed assurance workflow.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP


APP_DIR = Path(__file__).resolve().parent
sys.path.append(str(APP_DIR))


from claim_discovery_agent import ClaimDiscoveryAgent
from claim_library import load_claim_library
from dynatrace_provider import DynatraceProvider
from pml_claim_mapping_agent import PMLClaimMappingAgent


mcp = FastMCP("AI Decision Assurance MCP Server")


def _governed_claim_ids() -> List[str]:
    claims = load_claim_library()
    return [claim.claim_id for claim in claims]


@mcp.tool()
def discover_claims(requirement: str) -> Dict[str, Any]:
    """
    Reasoning tool.

    Uses Gemini to discover assurance claims from a requirement.
    """

    agent = ClaimDiscoveryAgent()
    suggestions = agent.discover(requirement)

    return {
        "tool": "discover_claims",
        "agent_layer": "reason",
        "requirement": requirement,
        "claims": [
            {
                "claim_id": suggestion.claim_id,
                "rationale": getattr(
                    suggestion,
                    "rationale",
                    suggestion.objective_description,
                ),
                "business_impact": getattr(
                    suggestion,
                    "business_impact",
                    "Business impact not provided.",
                ),
                "governance_need": getattr(
                    suggestion,
                    "governance_need",
                    "PML review required.",
                ),
                "source": suggestion.policy_name,
            }
            for suggestion in suggestions
        ],
    }


@mcp.tool()
def map_claim(discovered_claim: str) -> Dict[str, Any]:
    """
    Planning tool.

    Uses the PML Claim Mapping Agent to recommend whether a discovered claim
    maps to an existing governed executable claim.
    """

    governed_claims = _governed_claim_ids()

    agent = PMLClaimMappingAgent()

    recommendation = agent.recommend_mapping(
        discovered_claim=discovered_claim,
        governed_claims=governed_claims,
    )

    mapped_claim = recommendation.get("mapped_claim")
    confidence = recommendation.get("confidence", 0.0)

    mapping_supported = (
        mapped_claim in governed_claims
        and confidence >= 0.7
    )

    return {
        "tool": "map_claim",
        "agent_layer": "plan",
        "discovered_claim": discovered_claim,
        "mapped_claim": mapped_claim,
        "confidence": confidence,
        "rationale": recommendation.get("rationale"),
        "mapping_status": (
            "PML_APPROVAL_REQUIRED"
            if mapping_supported
            else "NO_SUPPORTED_MAPPING_FOUND"
        ),
        "governance_note": (
            "This is a recommendation only. PML approval is required before "
            "the mapped claim can enter the assurance scope."
        ),
    }


@mcp.tool()
def request_dynatrace_evidence(
    target_name: str = "easyTravel-Business",
) -> Dict[str, Any]:
    """
    Action tool.

    Requests runtime evidence from Dynatrace.

    This tool provides observability evidence only.
    It does not make assurance decisions.
    """

    runtime_reality = DynatraceProvider().get_runtime_reality().to_dict()

    return {
        "tool": "request_dynatrace_evidence",
        "agent_layer": "act",
        "source": "Dynatrace",
        "target_name": target_name,
        "runtime_reality": runtime_reality,
        "governance_note": (
            "Runtime evidence is not assurance by itself. Evidence must be "
            "evaluated against PML-approved governed claims."
        ),
    }


if __name__ == "__main__":
    mcp.run()

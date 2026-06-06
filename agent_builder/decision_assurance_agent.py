"""
decision_assurance_agent.py

Google ADK agent wrapper for the AI Decision Assurance Platform.

This file demonstrates how the platform can be orchestrated by a Gemini agent
using MCP tools.

Agent flow:
1. discover_claims
2. map_claim
3. request_dynatrace_evidence

PML approval remains visible in the Streamlit dashboard.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters


assurance_mcp_tools = McpToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=[
            "backend/app_v2/assurance_mcp_server.py",
        ],
    )
)


root_agent = LlmAgent(
    name="ai_decision_assurance_agent",
    model="gemini-3.1-flash-lite",
    description=(
        "An AI Decision Assurance Agent that reasons over requirements, "
        "plans governed assurance scope, and requests Dynatrace evidence "
        "through MCP tools."
    ),
    instruction="""
You are an AI Decision Assurance Agent.

Your job is to assure requirements safely.

Workflow:
1. Use discover_claims to reason over the requirement.
2. Use map_claim to map discovered claims to governed executable claims.
3. Explain that PML approval is required before claims enter assurance scope.
4. Use request_dynatrace_evidence to collect runtime evidence.
5. Do not claim assurance unless evidence has been evaluated by the assurance engine.
6. Never bypass PML governance.
7. Never directly modify production systems.

Output:
- Discovered claims
- Mapping recommendations
- Required PML approvals
- Runtime evidence summary
- Remaining assurance gaps
""",
    tools=[
        assurance_mcp_tools,
    ],
)

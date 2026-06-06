"""
dynatrace_mcp_server.py

Dynatrace Observability MCP Server

Purpose:
Expose Dynatrace runtime evidence capabilities as MCP tools.

This represents the partner observability MCP domain used by the
AI Decision Assurance Agent.

Tools:
- get_runtime_reality
- query_service_entity
- query_service_health_evidence
- query_active_problems
- query_dependency_topology

Important:
This MCP server does not make assurance decisions.
It only exposes runtime evidence capabilities.
"""

import sys
from pathlib import Path
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP


APP_DIR = Path(__file__).resolve().parent
sys.path.append(str(APP_DIR))

from dynatrace_provider import DynatraceProvider


mcp = FastMCP("Dynatrace Observability MCP Server")


def _runtime_reality() -> Dict[str, Any]:
    provider = DynatraceProvider()
    return provider.get_runtime_reality().to_dict()


def _find_service(runtime_reality: dict, target_name: str):
    services = runtime_reality.get("services", [])
    target = target_name.lower()

    for service in services:
        name = service.get("name", "").lower()
        display_name = service.get("display_name", "").lower()
        entity_id = service.get("entity_id", "").lower()

        if (
            target == name
            or target == display_name
            or target in name
            or target in display_name
            or target in entity_id
        ):
            return service

    return None


@mcp.tool()
def get_runtime_reality() -> Dict[str, Any]:
    """
    Return normalized Dynatrace runtime reality.
    """

    return {
        "source": "Dynatrace",
        "runtime_reality": _runtime_reality(),
    }


@mcp.tool()
def query_service_entity(target_name: str) -> Dict[str, Any]:
    """
    Query whether a service entity exists in Dynatrace runtime reality.
    """

    runtime_reality = _runtime_reality()
    service = _find_service(runtime_reality, target_name)

    return {
        "source": "Dynatrace",
        "tool": "query_service_entity",
        "target_name": target_name,
        "observed": service is not None,
        "service_entity": service,
    }


@mcp.tool()
def query_active_problems() -> Dict[str, Any]:
    """
    Query active/open Dynatrace problems.
    """

    runtime_reality = _runtime_reality()
    problems = runtime_reality.get("problems")

    if problems is None:
        return {
            "source": "Dynatrace",
            "tool": "query_active_problems",
            "observed": False,
            "reason": "Runtime reality does not include problems.",
            "active_problem_count": None,
            "active_problems": [],
        }

    active_problems = [
        problem
        for problem in problems
        if problem.get("status") in ["OPEN", "ACTIVE"]
    ]

    return {
        "source": "Dynatrace",
        "tool": "query_active_problems",
        "observed": True,
        "active_problem_count": len(active_problems),
        "active_problems": active_problems,
    }


@mcp.tool()
def query_dependency_topology() -> Dict[str, Any]:
    """
    Query dependency topology from Dynatrace runtime reality.
    """

    runtime_reality = _runtime_reality()
    dependencies = runtime_reality.get("dependencies")

    if dependencies is None:
        return {
            "source": "Dynatrace",
            "tool": "query_dependency_topology",
            "observed": False,
            "reason": "Runtime reality does not include dependency topology.",
            "dependencies": [],
        }

    return {
        "source": "Dynatrace",
        "tool": "query_dependency_topology",
        "observed": len(dependencies) > 0,
        "dependency_count": len(dependencies),
        "dependencies": dependencies,
    }


@mcp.tool()
def query_service_health_evidence(
    target_name: str,
) -> Dict[str, Any]:
    """
    Query service health evidence for an assurance target.

    Returns currently available health-related evidence and explicitly lists
    missing capabilities when metrics are not available.
    """

    runtime_reality = _runtime_reality()
    service = _find_service(runtime_reality, target_name)
    problems = runtime_reality.get("problems")

    response_time = None
    failure_rate = None

    missing_capabilities = []

    if service:
        response_time = (
            service.get("response_time")
            or service.get("avg_response_time")
            or service.get("responseTime")
        )

        failure_rate = (
            service.get("failure_rate")
            or service.get("error_rate")
            or service.get("failureRate")
        )
    else:
        missing_capabilities.append("service_entity")

    if response_time is None:
        missing_capabilities.append("response_time")

    if failure_rate is None:
        missing_capabilities.append("failure_rate")

    if problems is None:
        missing_capabilities.append("active_problems")

    return {
        "source": "Dynatrace",
        "tool": "query_service_health_evidence",
        "target_name": target_name,
        "service_observed": service is not None,
        "service_entity": service,
        "response_time": response_time,
        "failure_rate": failure_rate,
        "problems_available": problems is not None,
        "missing_capabilities": missing_capabilities,
    }


if __name__ == "__main__":
    mcp.run()

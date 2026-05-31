"""
Reality Engine

Compares declared architecture against observed Dynatrace runtime reality.

Core principle:
If Dynatrace cannot observe something, the platform should not treat it
as verified truth.
"""


def normalize_name(name: str) -> str:
    """
    Normalize component names so comparison is less brittle.
    Example: 'PostgreSQL' and 'postgresql' should match.
    """
    return name.strip().lower()


def detect_component_gaps(declared_architecture: dict, dynatrace_snapshot: dict) -> list:
    """
    Detect components declared in architecture but not observed by Dynatrace.
    """

    declared_components = declared_architecture.get("components", [])
    observed_components = dynatrace_snapshot.get("observed_components", [])

    observed_names = {
        normalize_name(component["name"])
        for component in observed_components
    }

    gaps = []

    for component in declared_components:
        component_name = normalize_name(component["name"])

        if component_name not in observed_names:
            gaps.append({
                "gap_type": "missing_component",
                "component": component["name"],
                "declared": True,
                "observed_in_dynatrace": False,
                "status": "not_verified",
                "reason": "Component is declared in architecture but not observed by Dynatrace."
            })

    return gaps


def detect_dependency_gaps(declared_architecture: dict, dynatrace_snapshot: dict) -> list:
    """
    Detect dependencies declared in architecture but not observed by Dynatrace.
    """

    declared_dependencies = declared_architecture.get("dependencies", [])
    observed_dependencies = dynatrace_snapshot.get("observed_dependencies", [])

    observed_pairs = {
        (
            normalize_name(dep["from"]),
            normalize_name(dep["to"])
        )
        for dep in observed_dependencies
    }

    gaps = []

    for dep in declared_dependencies:
        declared_pair = (
            normalize_name(dep["from"]),
            normalize_name(dep["to"])
        )

        if declared_pair not in observed_pairs:
            gaps.append({
                "gap_type": "missing_dependency",
                "from": dep["from"],
                "to": dep["to"],
                "declared": True,
                "observed_in_dynatrace": False,
                "status": "not_verified",
                "reason": "Dependency is declared in architecture but not observed by Dynatrace."
            })

    return gaps


def generate_truth_gap_report(declared_architecture: dict, dynatrace_snapshot: dict) -> dict:
    """
    Generate full truth gap report.
    """

    component_gaps = detect_component_gaps(
        declared_architecture,
        dynatrace_snapshot
    )

    dependency_gaps = detect_dependency_gaps(
        declared_architecture,
        dynatrace_snapshot
    )

    return {
        "summary": {
            "component_gaps": len(component_gaps),
            "dependency_gaps": len(dependency_gaps),
            "total_gaps": len(component_gaps) + len(dependency_gaps)
        },
        "gaps": component_gaps + dependency_gaps
    }

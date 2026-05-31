"""
Assurance Explanation Models

Purpose:
Represent human-readable explanations generated from assurance results.

Important:
Explanations do not determine assurance status.
They only explain assurance status.

Future:
This model can support LLM-generated explanations while preserving
a structured output contract.
"""

from dataclasses import dataclass


@dataclass
class AssuranceExplanation:
    """
    Represents an explanation of an assurance result.

    title:
        Short explanation title.

    summary:
        Human-readable summary.

    details:
        Supporting explanation points.

    recommendations:
        Suggested investigation or improvement actions.
    """

    title: str
    summary: str
    details: list[str]
    recommendations: list[str]

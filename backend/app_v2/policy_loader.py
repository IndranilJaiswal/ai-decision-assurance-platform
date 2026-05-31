"""
Policy Loader

Purpose:
Load policy definitions from YAML files.

Responsibilities:
- Parse policy YAML
- Create Policy models
- Create PolicyObjective models

Future Evolution:
Load multiple policies from a policy repository.
"""

import yaml

from policy_models import Policy
from policy_models import PolicyObjective


def load_policy(path: str) -> Policy:
    """
    Load a policy from YAML.

    Parameters
    ----------
    path:
        YAML file path.

    Returns
    -------
    Policy
    """

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    objectives = []

    for objective in data["objectives"]:

        objectives.append(
            PolicyObjective(
                objective_id=objective["objective_id"],
                description=objective["description"],
                suggested_claims=objective["suggested_claims"],
            )
        )

    return Policy(
        policy_id=data["policy_id"],
        name=data["name"],
        description=data["description"],
        objectives=objectives,
    )

"""
Claim Registry

Stores and retrieves claim instances.

Architectural distinction:
- Claim Library = governed claim definitions
- Claim Registry = runtime/governance instances of claims

The registry is the foundation for tracking claims through the full
governance lifecycle.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from claim_lifecycle_state_machine import ClaimLifecycleState


@dataclass
class ClaimRegistryRecord:
    """
    Persistent record for a claim instance.

    One claim definition can have many claim instances across
    requirements, reviews, approvals, and assurance runs.
    """

    claim_instance_id: str
    claim_id: str
    requirement_id: str
    state: ClaimLifecycleState
    created_at: datetime
    updated_at: datetime


class InMemoryClaimRegistry:
    """
    In-memory claim registry.

    This is the MVP implementation. It can later be replaced with
    MongoDB without changing the lifecycle architecture.
    """

    def __init__(self):
        self.records: Dict[str, ClaimRegistryRecord] = {}

    def create_claim_instance(
        self,
        claim_id: str,
        requirement_id: str,
        initial_state: ClaimLifecycleState = ClaimLifecycleState.DISCOVERED,
    ) -> ClaimRegistryRecord:
        """
        Create a new claim instance and store it in the registry.
        """

        now = datetime.utcnow()

        record = ClaimRegistryRecord(
            claim_instance_id=str(uuid4()),
            claim_id=claim_id,
            requirement_id=requirement_id,
            state=initial_state,
            created_at=now,
            updated_at=now,
        )

        self.records[record.claim_instance_id] = record

        return record

    def get_claim_instance(
        self,
        claim_instance_id: str,
    ) -> Optional[ClaimRegistryRecord]:
        """
        Retrieve a claim instance by ID.
        """

        return self.records.get(claim_instance_id)

    def update_claim_state(
        self,
        claim_instance_id: str,
        new_state: ClaimLifecycleState,
    ) -> ClaimRegistryRecord:
        """
        Update the lifecycle state of a claim instance.

        Note:
        This method only updates storage. Lifecycle transition validation
        should be handled by ClaimLifecycleManager.
        """

        record = self.records.get(claim_instance_id)

        if record is None:
            raise ValueError(
                f"Claim instance not found: {claim_instance_id}"
            )

        record.state = new_state
        record.updated_at = datetime.utcnow()

        return record

    def list_by_state(
        self,
        state: ClaimLifecycleState,
    ) -> List[ClaimRegistryRecord]:
        """
        List claim instances currently in a given lifecycle state.
        """

        return [
            record
            for record in self.records.values()
            if record.state == state
        ]

    def to_dict(
        self,
        record: ClaimRegistryRecord,
    ) -> dict:
        """
        Convert a registry record into a serializable dictionary.
        """

        data = asdict(record)
        data["state"] = record.state.value
        data["created_at"] = record.created_at.isoformat()
        data["updated_at"] = record.updated_at.isoformat()

        return data

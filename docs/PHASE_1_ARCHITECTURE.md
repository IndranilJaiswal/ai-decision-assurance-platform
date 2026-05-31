# AI Decision Assurance Platform

## Phase 1 Architecture

### Objective

Determine whether approved observable claims are supported by operational reality.

The platform does not assure requirements directly.

The platform assures approved claims using collected evidence.

---

# Core Flow

Requirement
↓
Claim Selection
↓
Evidence Collection
↓
Assurance Evaluation
↓
Decision Assurance Report

---

# Component Overview

## claim_models.py

Defines the core domain objects.

Responsibilities:

* Claim definition
* Approved claim definition

Purpose:

Provides the foundational data structures used throughout the platform.

---

## claim_library.yaml

Contains reusable claim templates.

Examples:

* Service Exists
* Service Healthy
* Dependency Exists

Purpose:

Provides a catalog of approved observable claims.

---

## capability_matrix.yaml

Maps claims to evidence requirements.

Purpose:

Defines what evidence is required to verify a claim and whether Dynatrace can provide it.

Example:

SERVICE_HEALTHY
↓
service_exists
failure_rate
response_time

---

## claim_library.py

Loads claim definitions and enriches them using capability metadata.

Purpose:

Creates executable claim objects from YAML configuration.

---

## evidence_models.py

Defines evidence request objects.

Purpose:

Represents the facts required to evaluate a claim.

---

## evidence_request_builder.py

Converts approved claims into evidence requests.

Purpose:

Separates claim definition from evidence collection.

Example:

SERVICE_HEALTHY
↓
service_exists
failure_rate
response_time

---

## evidence_engine.py

Collects evidence from reality sources.

Phase 1 Source:

Dynatrace

Future Sources:

* AWS
* Azure
* Kubernetes
* ServiceNow

---

## assurance_engine.py

Evaluates collected evidence against claim rules.

Outputs:

* VERIFIED
* PARTIALLY VERIFIED
* FAILED
* INSUFFICIENT_EVIDENCE

---

## reality_engine.py

Interfaces with external systems to collect operational reality.

Phase 1:

Dynatrace

---

## main.py

Platform orchestration entry point.

Coordinates:

Claims
↓
Evidence
↓
Assurance

---

# Design Principles

1. Requirements are not directly evaluated.

2. Only approved observable claims can be assured.

3. Evidence collection is separated from claim definition.

4. AI assists interpretation but does not determine truth.

5. Every assurance decision must be traceable to evidence.

---

# Current Milestone

Phase 1A - Claim Assurance Core

Completed:

✓ Claim Library

✓ Capability Matrix

✓ Claim Models

In Progress:

□ Evidence Request Builder

□ Evidence Collection

□ Assurance Evaluation

Future:

□ Standards-Based Claims

□ Dynatrace Evidence Adapters

□ Decision Assurance Dashboard
## evidence_models.py

Defines evidence request objects.

Purpose:

Represents the observable facts required
to evaluate a claim.

---

## evidence_request_builder.py

Converts approved claims into evidence requests.

Purpose:

Creates the bridge between:

Claim
↓
Evidence

Example:

SERVICE_HEALTHY

↓

service_exists
failure_rate
response_time
## evidence_records.py

Defines evidence records collected from reality sources.

Purpose:

Represents observable facts collected from external systems.

Example:

Service Exists
↓
Observed = True

Evidence records do not make assurance decisions.

They only record reality.

---

## dynatrace_adapter.py

Collects evidence from Dynatrace.

Purpose:

Transforms evidence requests into evidence records.

Example:

Evidence Request:
service_exists

↓

Dynatrace Service Lookup

↓

Evidence Record

Observed = True

---

Current Evidence Sources

Phase 1:

- Dynatrace

Future:

- AWS
- Azure
- Kubernetes
- ServiceNow
## Legacy MVP Components

### reality_engine.py

Phase 0 MVP component.

Purpose:

Compare declared architecture against observed runtime topology.

Produces:

Truth Gap Report

This component will remain supported for backward compatibility.

Future versions will introduce dedicated reality providers.

---

### evidence_engine.py

Phase 0 MVP component.

Purpose:

Convert truth gaps into evidence records.

Future versions will introduce evidence collection directly from runtime sources.
## reality_provider.py

Provides normalized runtime reality.

Purpose:

Decouples evidence collection from external systems.

Phase 1 Source:

Dynatrace

Future Sources:

- AWS
- Azure
- Kubernetes
- ServiceNow
## Runtime Reality Layer

Purpose:

Provide a normalized representation of observed operational reality.

The platform should not depend directly on vendor APIs.

Instead, external systems are normalized into RuntimeReality.

Benefits:

- Decouples assurance logic from vendor implementations.
- Supports multiple evidence sources.
- Enables consistent evidence collection.

Examples:

- Dynatrace
- AWS
- Azure
- Kubernetes
- ServiceNow
## Runtime Reality Layer

Purpose:

Provide a normalized representation of observed operational reality.

The platform should not depend directly on vendor APIs.

Instead, external systems are normalized into RuntimeReality.

Benefits:

- Decouples assurance logic from vendor implementations.
- Supports multiple evidence sources.
- Enables consistent evidence collection.

Examples:

- Dynatrace
- AWS
- Azure
- Kubernetes
- ServiceNow

---

## reality_provider.py

Defines the RuntimeReality model and provider interface.

Purpose:

Create a standard representation of operational reality regardless of source.

---

## mock_dynatrace_provider.py

Temporary Dynatrace implementation.

Purpose:

Allow development and testing of the Claim → Evidence flow before live Dynatrace API integration.
## dynatrace_client.py

Low-level Dynatrace API client.

Purpose:

Handles authenticated calls to Dynatrace APIs.

Does not contain assurance logic.

---

## dynatrace_provider.py

Live Dynatrace runtime reality provider.

Purpose:

Converts Dynatrace entities into normalized RuntimeReality.

Current support:

- SERVICE entities
## test_dynatrace_adapter.py

Purpose:

Validate the complete Claim → Evidence flow using
live Dynatrace runtime reality.

Current Validation:

SERVICE_EXISTS

Future Validation:

- SERVICE_HEALTHY
- NO_ACTIVE_PROBLEMS
- DEPENDENCY_EXISTS
## Live Dynatrace Validation

Current Supported Validation:

SERVICE_EXISTS

Flow:

Approved Claim
↓
Evidence Request Builder
↓
Dynatrace Provider
↓
Runtime Reality
↓
Evidence Adapter
↓
Evidence Record

Current Runtime Reality Source:

Dynatrace SaaS Tenant

Current Validated Service:

easyTravel-Business

## evidence_collection_engine.py

Purpose:

Coordinates evidence collection for approved claims.

Responsibilities:

- Generate evidence requests
- Collect evidence
- Return evidence records

The engine does not perform assurance evaluation.
\

Approved Claim
↓
Evidence Requests
↓
Evidence Adapter
↓
Evidence Records

## Requirement Layer

Requirements express human intent.

Claims make requirements observable.

Architecture:

Requirement
↓
Approved Claims
↓
Evidence
↓
Assurance

---

## requirement_models.py

Defines requirement domain objects.

---

## requirement_library.py

Loads requirements from configuration.

---

## claim_assurance_engine.py

Evaluates evidence records against approved claims.

Phase 1C currently supports SERVICE_EXISTS.

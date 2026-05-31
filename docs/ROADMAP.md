# Roadmap

## Phase 1A - Claim Assurance Core

Status: Complete

### Completed

- Claim Library
- Claim Models
- Capability Matrix
- Approved Claims
- Evidence Request Model
- Evidence Request Builder

### Outcome

The platform can transform approved claims into observable evidence requirements.

---

## Phase 1B - Evidence Collection

Status: In Progress

### Goal

Collect real evidence from Dynatrace.

### Deliverables

- Dynatrace Evidence Adapter
- Evidence Record Model
- Evidence Collection Engine

### First Supported Evidence Type

SERVICE_EXISTS

### Example Flow

Approved Claim:
SERVICE_EXISTS

Evidence Request:
service_exists

Reality Source:
Dynatrace

Evidence Record:
Service observed or not observed

## Phase 1B - Evidence Collection

Status: In Progress

### Completed

- Evidence Record Model
- Dynatrace Evidence Adapter
- Service Existence Evidence Collection

### In Progress

- Failure Rate Evidence
- Response Time Evidence
- Problem Evidence

### Remaining

- Evidence Collection Engine
- Assurance Integration
### Completed

- Runtime Reality Model
- Reality Provider Abstraction
Completed:

✓ RuntimeReality model

✓ RealityProvider abstraction

✓ Mock Dynatrace Provider

In Progress:

□ Real Dynatrace Provider

□ Evidence Collection Engine

□ Assurance Integration
### Completed

- RuntimeReality model
- RealityProvider abstraction
- MockDynatraceProvider

### In Progress

- Live Dynatrace Provider
- Evidence Collection Engine
- Assurance Integration
### Completed

- Live Dynatrace Client
- Live Dynatrace Provider
- SERVICE entity ingestion

### Remaining

- Container ingestion
- Host ingestion
- Dependency ingestion
- Metrics ingestion
### Completed

- Live Dynatrace Provider
- SERVICE entity ingestion
- Runtime Reality normalization
- Live SERVICE_EXISTS evidence test
### Completed

✓ Live Dynatrace Client

✓ Live Dynatrace Provider

✓ Runtime Reality Normalization

✓ SERVICE Entity Ingestion

✓ Live SERVICE_EXISTS Validation

### Next

□ SERVICE_HEALTHY

□ NO_ACTIVE_PROBLEMS

□ DEPENDENCY_EXISTS

□ Assurance Engine Integration
### Completed

✓ Evidence Collection Engine

✓ End-to-End Evidence Collection Flow

### Completed

✓ RuntimeReality model

✓ RealityProvider abstraction

✓ Live Dynatrace Provider

✓ SERVICE entity ingestion

✓ Runtime Reality normalization

✓ Live SERVICE_EXISTS validation

✓ Evidence Collection Engine

✓ End-to-End Evidence Collection Flow

### Remaining

□ Assurance Engine Integration

□ SERVICE_HEALTHY

□ NO_ACTIVE_PROBLEMS

□ DEPENDENCY_EXISTS


## Phase 1C - Requirement Assurance

Status: In Progress

### Completed

- Requirement model
- Requirement configuration
- Requirement loader
- Assurance result model
- Claim Assurance Engine v1
- SERVICE_EXISTS assurance evaluation

### Next

- Requirement assurance rollup
- SERVICE_HEALTHY assurance
- Dashboard v1

### Completed

- Requirement assurance rollup model
- Requirement assurance engine
- Multi-claim requirement evaluation

### Next

- Dashboard v1
- SERVICE_HEALTHY evidence expansion

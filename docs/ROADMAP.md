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

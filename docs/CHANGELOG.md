## 2026-05-31

### Added

- EvidenceRequest model
- EvidenceRequestBuilder
- Evidence Request Builder test

### Purpose

Introduced the Evidence Request layer.

Claims can now be transformed into
observable evidence requirements.

### Architecture Impact

Approved Claim
↓
Evidence Requests
↓
Evidence Engine
## 2026-05-31

### Added

- EvidenceRecord model
- DynatraceEvidenceAdapter
- Service existence evidence collection
- Dynatrace adapter test

### Purpose

Introduced the first operational evidence collection capability.

The platform can now collect evidence from runtime reality.

### Architecture Impact

Approved Claim
↓
Evidence Request
↓
Dynatrace Adapter
↓
Evidence Record

### Supported Evidence Types

- service_exists

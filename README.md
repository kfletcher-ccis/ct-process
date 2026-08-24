# CT Process ETL

## Overview

CT Process ETL transforms RE NXT exports into a canonical constituent model and produces operational outputs for review, import, diagnostics, and future API-driven integrations.

The project has evolved from a CSV transformation utility into a canonical constituent processing platform.

## Core Capabilities

### Constituent Matching

Supports:

- NEW records
- EXISTING records

Matching methods:

- Lookup ID
- SKY ID
- ConsImportID

---

### Canonical Constituent Model

Each constituent is assembled into a structured object model:

```text
Constituent
├── core
├── phones[]
├── employment[]
├── education[]
├── military[]
└── relationships[]
```

This canonical representation becomes the system of record for all downstream outputs.

---

### Employment Processing

Employment records are generated from pipe-delimited source fields:

```text
ORPos
ORProf
ORFromDate
ORToDate
ORIndustry
```

Features:

- Positional alignment preservation
- Multiple employment records supported
- Null/N/A normalization
- Recent employment detection

---

### Education Processing

Education records are transformed into structured degree objects.

Features:

- Degree support
- Major support
- Minor support
- Graduation date filtering

---

### Recent Activity Filtering

Employment and education records are evaluated against a:

```text
120-day activity window
```

Used to identify actionable updates for EXISTING records.

---

### Existing Record Update Detection

Existing constituents are evaluated for:

```text
EMPLOYMENT updates
EDUCATION updates
```

The resulting metadata is exposed through:

```json
{
  "update_flags": {
    "needs_employment_update": true,
    "needs_education_update": false,
    "needs_update": true
  },

  "update_actions": [
    "EMPLOYMENT"
  ]
}
```

---

## Outputs

Each run generates:

```text
constituents_*.json
diagnostics_*.json
schema_analysis_*.json

process_summary_*.json
process_summary_*.txt

ct_process_review_*.xlsx
ct_process_import_*.csv
```

---

## Output Folder Structure

```text
output\
└── YYYY-MM-DD\
    ├── source files
    ├── CT_Process__Existing_IDs_*.xlsx
    ├── constituents_*.json
    ├── diagnostics_*.json
    ├── schema_analysis_*.json
    ├── process_summary_*.json
    ├── process_summary_*.txt
    ├── ct_process_review_*.xlsx
    └── ct_process_import_*.csv
```

Each folder is a complete historical processing run.

---

## Architecture

```text
RE NXT Exports
        ↓
Loaders
        ↓
Transformers
        ↓
Canonical Constituent Model
        ↓
Filters
        ↓
Update Detection
        ↓
Outputs
```

Produced outputs:

```text
JSON
XLSX Review Workbook
CT Process CSV
Diagnostics
Process Summary
```

---

## Future Direction

Designed to support:

```text
Canonical JSON
        ↓
Power Automate
        ↓
SKY API
```

without requiring additional business-rule evaluation downstream.

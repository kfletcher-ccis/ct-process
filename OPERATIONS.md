# OPERATIONS GUIDE

## Running the Process

Execute:

```powershell
python C:\Users\kfletcher\CTinput\run_ct_process.py
```

The process is location-independent and uses:

```python
SCRIPT_DIR
```

for file resolution.

---

## Required Inputs

Drop the following files into the CTinput root folder:

```text
RENXT-EXPORT_*.csv
RENXT-EXPORT_Activities_File_*.csv
RENXT-EXPORT_Education_File_*.csv
RENXT-EXPORT_Military_File_*.csv
RENXT-EXPORT_Relationships_File_*.csv

CT_Process__Existing_IDs.xlsx
```

---

## File Selection

When multiple export files match:

```text
Newest modified file wins
```

This prevents stale runs from being selected.

---

## Runtime Flow

```text
1. Locate Source Files
2. Load Exports
3. Build Canonical Model
4. Generate Constituents JSON
5. Generate Diagnostics JSON
6. Generate Schema Analysis JSON
7. Generate Review Workbook
8. Generate Import CSV
9. Generate Process Summary Files
10. Archive Run Artifacts
```

---

## Generated Outputs

### JSON

```text
constituents_*.json
diagnostics_*.json
schema_analysis_*.json
process_summary_*.json
```

### Text

```text
process_summary_*.txt
```

### User Review

```text
ct_process_review_*.xlsx
```

### CT Process Import

```text
ct_process_import_*.csv
```

---

## Archival Structure

Successful runs are archived into:

```text
output\
└── YYYY-MM-DD\
```

Each folder contains:

```text
Source files
Existing IDs workbook
JSON outputs
Summary outputs
Review workbook
Import CSV
```

---

## Diagnostics

The following files support troubleshooting:

### diagnostics.json

Contains:

```text
total_constituents
new_records
existing_records
phone_records
employment_records
degree_records
military_records
relationship_records
warnings
relationship_warnings
```

### schema_analysis.json

Contains:

```text
max_phone_records
max_employment_records
max_degree_records
max_major_records
max_minor_records
max_military_records
max_relationship_records
```

---

## Process Summary

### process_summary.txt

Human-readable run summary.

### process_summary.json

Machine-readable run summary.

Intended for:

```text
Power Automate
SharePoint
Email notifications
Monitoring
```

---

## Existing Record Update Evaluation

Update eligibility is calculated after filtering.

Supported update actions:

```text
EMPLOYMENT
EDUCATION
```

These appear in:

```json
update_flags
update_actions
```

within the canonical constituent JSON.

---

## Future Integrations

Planned integration path:

```text
Constituents JSON
        ↓
SharePoint
        ↓
Power Automate
        ↓
SKY API Operations
```

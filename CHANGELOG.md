# CHANGELOG

All notable changes to the CT Process ETL project are documented in this file.

---

# v1.6.0 - PAD Automation and Repeated-Field Compatibility

Date: November 18, 2026

## Added

- `run_ct_process.bat` as an unattended Windows entry point for the existing CT Process File Transfer PAD flow.
- Python launcher detection:
  - Prefers `py -3`.
  - Falls back to `python`.
- Exit-code propagation from `run_ct_process.py` to PAD.
- Explicit batch error codes for a missing Python script and an unavailable Python installation.
- PAD execution, success, failure, and post-run verification guidance.

## Fixed

### `helpers/common.py`

- Updated `repeated_values()` to support both repeated-column naming conventions used by CT Process sources:
  - Pandas duplicate-header suffixes: `Field`, `Field.1`, `Field.2`, ...
  - Explicit numbered suffixes: `Field`, `Field_2`, `Field_3`, ...
- Restored extraction of all populated phone and email records rather than only the unsuffixed first record.
- Preserved compatibility with callers that use explicit underscore-numbered fields.
- Retained compact output behavior by omitting blank repeated values.

## Changed

### `README.md`

- Updated the production project root from `C:\Users\kfletcher\CTinput` to `C:\PAD\CTinput`.
- Added the PAD/batch quick-start procedure.
- Documented required inputs, generated outputs, success criteria, and repeated-field compatibility.
- Added a file-by-file summary of the v1.6.0 repository changes.

### `OPERATIONS.md`

- Updated all production commands and paths to `C:\PAD\CTinput`.
- Made `run_ct_process.bat` the recommended production entry point.
- Added the CT Process File Transfer PAD handoff sequence.
- Added recommended PAD run settings, exit-code handling, post-run verification, and troubleshooting.
- Added regression checks for aliases, phones/emails, majors, minors, and education attributes after shared helper changes.

### `CHANGELOG.md`

- Added this v1.6.0 release entry covering every repository file changed for the repeated-field fix, working-directory move, documentation refresh, and PAD launcher.

## Changed Files

| File | Change |
|---|---|
| `helpers/common.py` | Supports dot-suffixed and underscore-suffixed repeated fields. |
| `run_ct_process.bat` | New unattended launcher for PAD and manual execution. |
| `README.md` | Updated path and end-to-end operating guidance. |
| `OPERATIONS.md` | Updated runbook and PAD integration contract. |
| `CHANGELOG.md` | Added the v1.6.0 release record. |

## Compatibility Notes

- No changes are required in `transformers/core_transformer.py` or `transformers/education_transformer.py`; their existing calls to `repeated_values()` use the expanded helper behavior.
- The batch launcher does not pause, so the current PAD flow can wait for completion without keyboard interaction.
- The batch launcher resolves `run_ct_process.py` relative to the batch file, while the production PAD configuration continues to call it at `C:\PAD\CTinput\run_ct_process.bat`.

---

# v1.5.0 - Automated Reporting Foundation
Date: August 2026

## Added

- Process summary generation:
  - process_summary.json
  - process_summary.txt

- Enhanced runtime reporting.

- Structured machine-readable summary output.

- Foundation for:
  - Power Automate notifications
  - SharePoint-based automation
  - Email notifications
  - Operational monitoring

## Generated Artifacts

- constituents_*.json
- diagnostics_*.json
- schema_analysis_*.json
- process_summary_*.json
- process_summary_*.txt
- ct_process_review_*.xlsx
- ct_process_import_*.csv

---

# v1.4.0 - Review Workbook Improvements

Date: August 2026

## Changed

- Review workbook now operates against the canonical transformed constituent model.

## Benefits

- Workbook reflects actual import behavior.
- Improves validation accuracy.
- Reduces discrepancies between review and import outputs.

---

# v1.3.0 - Existing Record Update Framework

Date: August 2026

## Added

Constituent-level update tracking.

### New Metadata

- update_flags
- update_actions

### Supported Actions

- EMPLOYMENT
- EDUCATION

## Benefits

- Identifies actionable updates for EXISTING records.
- Simplifies future SKY API integration.
- Eliminates downstream re-evaluation of update eligibility.

---

# v1.2.0 - Recent Activity Window Expansion

Date: August 2026

## Changed

- Recent activity window increased from:
  - 90 days
  - to 120 days

## Impact

- Employment records qualifying after April 21, 2026 remain actionable.
- Education records qualifying after April 21, 2026 remain actionable.

---

# v1.1.0 - Employment Date Normalization

Date: August 2026

## Fixed

Employment date handling.

### Normalized Values

The following values now normalize to blank:

- N/A
- NA
- NULL
- NONE

## Benefits

- Prevents positional alignment failures.
- Prevents incorrect date assignment.

---

# v1.0.0 - Employment Processing Rewrite

Date: August 2026

## Fixed

Pipe-delimited employment processing.

### Fields

- ORPos
- ORProf
- ORFromDate
- ORToDate
- ORIndustry

### Improvements

- Preserves positional alignment.
- Correctly generates multiple employment records.
- Prevents dates from shifting to adjacent positions.

## Added

- split_preserving_positions()

---

# v0.9.0 - Newest File Resolution

Date: August 2026

## Changed

File discovery now automatically selects the newest matching file.

### Previous Behavior

- First file returned by filesystem.

### New Behavior

- Most recently modified file.

## Benefits

- Eliminates stale input selection.
- Supports multiple export sets.

---

# v0.8.0 - Working Directory Independence

Date: August 2026

## Changed

Introduced SCRIPT_DIR-based path resolution.

### Previous Behavior

- Depended on current PowerShell directory.

### New Behavior

- Uses script location.

## Benefits

- Reliable execution from any location.
- Improved compatibility with automation tools.

---

# v0.7.0 - Run Folder Architecture

Date: August 2026

## Changed

Removed:

- OLD\ archive structure

Added:

- output\YYYY-MM-DD\

## Benefits

- Self-contained run folders.
- Simpler artifact management.
- Easier SharePoint synchronization.

---

# v0.6.0 - Transformation Diagnostics

Date: August 2026

## Added

Diagnostics generation.

### Metrics

- total_constituents
- new_records
- existing_records
- phone_records
- employment_records
- degree_records
- military_records
- relationship_records

### Validation

- warnings
- relationship_warnings

---

# v0.5.0 - JSON Serialization Framework

Date: August 2026

## Added

Canonical JSON outputs:

- constituents.json
- diagnostics.json
- schema_analysis.json

## Benefits

- Full model visibility.
- Improved troubleshooting.
- Future API readiness.

---

# v0.4.0 - Dynamic Schema Analysis

Date: August 2026

## Added

Automatic schema discovery.

### Metrics

- max_phone_records
- max_employment_records
- max_degree_records
- max_major_records
- max_minor_records
- max_military_records
- max_relationship_records

---

# v0.3.0 - Canonical Object Model Expansion

Date: July-August 2026

## Added

Structured constituent collections:

- phones[]
- employment[]
- education[]
- military[]
- relationships[]

## Benefits

- Single source of truth.
- Easier exporters.
- API-ready architecture.

---

# v0.2.0 - ETL Framework Expansion

Date: July 2026

## Added

Support for:

- Core Export
- Activities Export
- Education Export
- Military Export
- Relationships Export

## Added

Existing/New constituent detection.

### Matching Methods

- Lookup ID
- SKY ID
- ConsImportID

---

# v0.1.0 - Initial Release

Date: July 15, 2026

## Added

Initial CT Process ETL framework.

### Core Capabilities

- Constituent transformation pipeline.
- Dynamic CSV export.
- Review workbook generation.
- ConsCode evaluation.

### Business Rules

- Employment qualification window.
- Education qualification window.
- Existing vs New record handling.

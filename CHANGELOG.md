# CHANGELOG

All notable changes to the CT Process ETL project are documented in this file.

---

# v1.7.0 - Timestamp Standardization and Runtime Hardening

Date: October 21, 2026

## Changed

- Standardized CT Process internal run timestamps on the sortable format:
  - `yyyy-MM-dd_HH-mm-ss`
- Preserved the source RENXT export filename convention while normalizing the parsed timestamp used by CT Process.
- Updated `get_processing_timestamp()` so `timestamp["raw"]` is assembled as:
  - `year-month-day_time`
- Standardized generated JSON, workbook, CSV, and process-summary filenames on the normalized run timestamp.
- Retained date-only local output folders in `yyyy-MM-dd` format.
- Restricted the `GENERATED FILES` report to the successful execution path so failed runs are not presented as completed runs.

## Added

- Added resilient CSV decoding to the shared CSV loader:
  - UTF-8 is attempted first.
  - If UTF-8 decoding fails, loading automatically retries with Windows-1252 (`cp1252`).
- Added a clear console message when the loader falls back from UTF-8 to Windows-1252.

## Fixed

- Prevented RENXT CSV exports containing Windows-encoded characters, including non-breaking spaces, from failing during `pandas.read_csv()` decoding.
- Eliminated inconsistent `dd-MM-yyyy_HH-mm-ss` values in generated filenames and `process_summary.json`.
- Improved chronological sorting and cross-system run correlation among CT Process, Power Automate Desktop, SharePoint archives, and cloud-flow logs.
- Corrected exception handling so failures occurring before output paths are initialized do not raise a secondary `NameError` for variables such as `review_file`.
- Preserved the original processing exception and traceback instead of masking it with output-reporting errors.
- Prevented unsuccessful runs from printing misleading generated-file paths.

---

# v1.6.0 - SharePoint Archiving and Power Automate Integration

Date: September 2026

## Added

- Added Power Automate Desktop processing to upload CT Process JSON artifacts to SharePoint.
- Added replaceable root working copies for downstream automation:
  - `constituents.json`
  - `diagnostics.json`
  - `process_summary.json`
  - `schema_analysis.json`
- Added timestamped SharePoint archive folders containing forensic copies of each run's JSON artifacts.
- Added the SharePoint `CT Process Run Log` list for run-level status, counts, timestamps, source-file references, and error summaries.
- Added the SharePoint `CT Process Change Log` list for atomic comparisons and changes, including before/after values, proposed values, payloads, outcomes, and error details.
- Added run-level and change-level forensic references to archived constituent JSON files.
- Added Central Time formatting for timestamps embedded in human-readable text while retaining UTC for SharePoint Date/Time columns and calculations.

## Changed

- Revised the Power Automate Desktop upload order so archived JSON copies are created before root working files are overwritten.
- Adopted `process_summary.json` as the cloud-flow orchestration trigger and run manifest.
- Adopted `run_timestamp` as the shared run identifier across Python output, Power Automate Desktop, SharePoint archive folders, the Run Log, and the Change Log.
- Revised constituent-processing logic so the archived `constituents` file can provide both processing content and forensic source metadata.
- Converted `constituents.json` from a lookup-ID-keyed JSON object to a root JSON array for direct use by Power Automate `Filter array` and `Apply to each` actions.

## Power Automate Processor Architecture

- Added or designed scopes for:
  - Retrieving current RENXT constituent data
  - Comparing Employment records
  - Comparing Education records
  - Comparing Names and Aliases
  - Executing approved changes
  - Constituent-level exception handling
- Added run and change counters for attempted, successful, failed, skipped, Employment, Education, Name, and Alias operations.
- Established sequential constituent processing to protect shared counters and preserve deterministic logging.
- Defined Pending, Succeeded, Failed, Skipped, No Change, and Needs Review outcomes for change operations.

## Name and Demographic Review Design

- Defined a review-only rule for Last Name discrepancies so incoming data does not automatically overwrite a potentially newer RENXT value.
- Defined Birth Date handling:
  - Populate RENXT when the incoming value exists and RENXT is blank.
  - Take no action when the values match.
  - Log and flag the difference for review when both values exist but differ.
- Reserved selected Alias comparison and update logic for a later implementation phase.

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
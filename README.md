# CT Process ETL

The CT Process ETL converts the monthly Colleague/CT Process export set into a canonical constituent model and produces review, diagnostics, import, and process-summary artifacts for downstream review and automation.

## Current project location

The production working directory is:

```text
C:\PAD\CTinput
```

All source files, the Python entry point, the batch launcher, and generated `output` folders are resolved from this project directory. The Python process uses script-relative path resolution, so it does not depend on the shell's starting directory.

## Quick start

### From the CT Process File Transfer PAD flow

1. Complete the existing file-transfer steps so the required exports and workbook are present in `C:\PAD\CTinput`.
2. Run:

   ```text
   C:\PAD\CTinput\run_ct_process.bat
   ```

3. Configure PAD to wait for the batch file to finish.
4. Treat exit code `0` as success and any nonzero exit code as failure.
5. On success, review the newest date-stamped folder beneath `C:\PAD\CTinput\output`.

See [OPERATIONS.md](OPERATIONS.md) for the recommended PAD configuration, verification steps, and troubleshooting guidance.

### From Command Prompt or PowerShell

Run the batch launcher:

```bat
C:\PAD\CTinput\run_ct_process.bat
```

Or invoke Python directly:

```powershell
python C:\PAD\CTinput\run_ct_process.py
```

The batch launcher is preferred because it:

- resolves the project directory from its own location;
- changes to that directory before execution;
- prefers the Windows `py -3` launcher and falls back to `python`;
- returns the Python process's exit code to PAD;
- does not pause for keyboard input.

## Requirements

- Windows
- Python 3 available through either `py -3` or `python`
- The Python environment and project dependencies already used by `run_ct_process.py`
- Read/write access to `C:\PAD\CTinput`

## Required inputs

Place the newest matching files in `C:\PAD\CTinput` before starting the process:

```text
RENXT-EXPORT_*.csv
RENXT-EXPORT_Activities_File_*.csv
RENXT-EXPORT_Education_File_*.csv
RENXT-EXPORT_Military_File_*.csv
RENXT-EXPORT_Relationships_File_*.csv
CT_Process__Existing_IDs.xlsx
```

When multiple files match a source pattern, the process selects the most recently modified file.

## Processing sequence

```text
1. Locate source files
2. Load exports
3. Build the canonical constituent model
4. Generate constituents JSON
5. Generate diagnostics JSON
6. Generate schema-analysis JSON
7. Generate the review workbook
8. Generate the import CSV
9. Generate process-summary files
10. Archive run artifacts in a date-stamped output folder
```

## Generated artifacts

Successful runs create artifacts beneath:

```text
C:\PAD\CTinput\output\YYYY-MM-DD\
```

The run folder includes files matching:

```text
constituents_*.json
diagnostics_*.json
schema_analysis_*.json
process_summary_*.json
process_summary_*.txt
ct_process_review_*.xlsx
ct_process_import_*.csv
```

The run folder also retains the source files and existing-IDs workbook used for the run.

## Canonical update metadata

Existing-record update eligibility is represented in the constituent JSON through:

```text
update_flags
update_actions
```

Current supported update-action categories are:

```text
EMPLOYMENT
EDUCATION
```

## Repeated-field compatibility

The shared `repeated_values()` helper supports both repeated-column conventions used by the source data:

```text
Pandas duplicate headers:  Field, Field.1, Field.2, ...
Explicit numbered fields:  Field, Field_2, Field_3, ...
```

This preserves compatibility across core aliases, phone/email records, education majors, education minors, and education attributes. Blank repeated values are omitted from the compact canonical collections.

## Operational success criteria

A run is complete only when:

- the batch/Python exit code is `0`;
- a new date-stamped output folder exists;
- `process_summary_*.json` and `process_summary_*.txt` exist;
- the review workbook and import CSV exist;
- warnings and diagnostics have been reviewed before downstream use.

## Repository files changed in v1.6.0

- `helpers/common.py` — repeated-field parsing supports both dot-suffixed and underscore-suffixed source columns.
- `run_ct_process.bat` — unattended entry point for the CT Process File Transfer PAD flow.
- `README.md` — current path, batch/PAD quick start, inputs, outputs, and validation.
- `OPERATIONS.md` — production runbook and PAD integration steps.
- `CHANGELOG.md` — v1.6.0 release record.

See [CHANGELOG.md](CHANGELOG.md) for the full project history.

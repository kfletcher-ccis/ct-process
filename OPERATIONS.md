# OPERATIONS GUIDE

## Production location

The CT Process ETL production working directory is:

```text
C:\PAD\CTinput
```

Expected entry points:

```text
C:\PAD\CTinput\run_ct_process.bat
C:\PAD\CTinput\run_ct_process.py
```

`run_ct_process.py` resolves project files from its script directory. `run_ct_process.bat` also resolves its own folder and changes to that folder before starting Python. The process therefore does not depend on PAD's or the user's current shell directory.

---

## Recommended production run

Use the batch launcher for manual and PAD-initiated production runs:

```bat
C:\PAD\CTinput\run_ct_process.bat
```

The launcher:

1. Locates `run_ct_process.py` beside the batch file.
2. Changes the working directory to `C:\PAD\CTinput`.
3. Uses `py -3` when the Windows Python launcher is available.
4. Falls back to `python` when necessary.
5. Runs the complete Python process.
6. Returns the Python exit code unchanged to the calling PAD flow.
7. Exits without pausing for user input.

Direct execution remains available for troubleshooting:

```powershell
python C:\PAD\CTinput\run_ct_process.py
```

---

## CT Process File Transfer PAD integration

Keep the existing CT Process File Transfer desktop flow responsible for obtaining and copying the source files. Add the batch execution as the final processing step after all copies have completed successfully.

### Recommended PAD sequence

```text
1. Run the existing Colleague/CT Process export and file-transfer steps.
2. Copy all required source files into C:\PAD\CTinput.
3. Copy CT_Process__Existing_IDs.xlsx into C:\PAD\CTinput.
4. Run C:\PAD\CTinput\run_ct_process.bat.
5. Wait for the batch process to finish.
6. If the exit code is 0, continue to success/reporting steps.
7. If the exit code is nonzero, stop the flow and route to failure handling.
```

### PAD run settings

Configure the PAD action that launches the batch file with these values or their equivalent:

| Setting | Value |
|---|---|
| Program / command | `C:\PAD\CTinput\run_ct_process.bat` |
| Working folder | `C:\PAD\CTinput` |
| Wait for completion | Yes |
| Window | Hidden or normal; either is supported |
| Continue after command failure | No |

If the PAD action cannot execute a `.bat` file directly, use:

```text
cmd.exe /d /c ""C:\PAD\CTinput\run_ct_process.bat""
```

The doubled outer quotes are intentional and protect a quoted batch-file path.

### Exit-code contract

| Exit code | Meaning |
|---:|---|
| `0` | The Python process completed successfully. |
| `2` | `run_ct_process.py` was not found beside the batch file. |
| `3` | The batch launcher could not use its project directory. |
| `9009` | Neither `py` nor `python` was available on `PATH`. |
| Other nonzero value | The Python process failed; the original Python exit code was returned. |

PAD should use only `0` as its success condition.

---

## Required inputs

Before launching the process, confirm the newest source set is present in `C:\PAD\CTinput`:

```text
RENXT-EXPORT_*.csv
RENXT-EXPORT_Activities_File_*.csv
RENXT-EXPORT_Education_File_*.csv
RENXT-EXPORT_Military_File_*.csv
RENXT-EXPORT_Relationships_File_*.csv
CT_Process__Existing_IDs.xlsx
```

### File-selection rule

When multiple files match a source pattern:

```text
Newest modified file wins
```

Do not rely on filename sorting alone. Remove unintended newer copies before a production run.

---

## Runtime flow

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

## Generated outputs

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

### User review

```text
ct_process_review_*.xlsx
```

### CT Process import

```text
ct_process_import_*.csv
```

---

## Archival structure

Successful runs are archived beneath:

```text
C:\PAD\CTinput\output\YYYY-MM-DD\
```

Each run folder contains the source files, existing-IDs workbook, JSON outputs, process summaries, review workbook, and import CSV associated with that run.

---

## Post-run verification

After PAD receives exit code `0`:

1. Open the newest folder under `C:\PAD\CTinput\output`.
2. Confirm that `process_summary_*.json` and `process_summary_*.txt` exist.
3. Confirm that `ct_process_review_*.xlsx` exists.
4. Confirm that `ct_process_import_*.csv` exists.
5. Review diagnostics and warnings.
6. Compare the summary's constituent and record counts with the expected source volume.
7. Do not send artifacts to a downstream import or API process until the review is complete.

### `diagnostics_*.json`

Use the diagnostics output to review:

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

### `schema_analysis_*.json`

Use the schema-analysis output to review:

```text
max_phone_records
max_employment_records
max_degree_records
max_major_records
max_minor_records
max_military_records
max_relationship_records
```

### Process summaries

- `process_summary_*.txt` is the human-readable run summary.
- `process_summary_*.json` is the machine-readable summary intended for PAD, Power Automate, SharePoint, email notification, or monitoring integrations.

---

## Repeated-field parsing

`helpers\common.py` supports both repeated-column conventions found in CT Process data:

```text
Field, Field.1, Field.2, ...
Field, Field_2, Field_3, ...
```

The helper is shared by:

- core aliases;
- core phone and email records;
- education majors;
- education minors;
- education attributes.

After a helper change, validate at least one constituent with multiple phones/emails, one with aliases, and one with repeated education values. Confirm that populated records remain paired and that no expected repeated values are dropped.

---

## Existing-record update evaluation

Update eligibility is calculated after filtering.

Current supported update actions:

```text
EMPLOYMENT
EDUCATION
```

These appear in the canonical constituent JSON as:

```text
update_flags
update_actions
```

---

## Failure handling

### Batch reports that the Python script is missing

Confirm that both files are in the same folder:

```text
C:\PAD\CTinput\run_ct_process.bat
C:\PAD\CTinput\run_ct_process.py
```

### Batch reports that Python is unavailable

From Command Prompt, test:

```bat
py -3 --version
python --version
```

At least one command must resolve in the same Windows account and execution context used by PAD.

### PAD succeeds but no current output appears

1. Verify that PAD waited for the batch file to finish.
2. Check the captured exit code.
3. Confirm the input files were copied before the batch step.
4. Confirm the newest modified files are the intended source set.
5. Run the batch file from Command Prompt under the PAD account to expose console errors.

### Python fails

Preserve the console/PAD error text and the input set. Review the newest diagnostics or partial output only for troubleshooting; do not treat partial artifacts as a successful run.

---

## Future integration path

```text
Constituents JSON
        ↓
SharePoint
        ↓
Power Automate
        ↓
SKY API Operations
```

# Operations Guide

## Monthly Workflow

### Step 1

Export the required files from Colleague.

Required files:

```text
RENXT-EXPORT_[DATE].csv

RENXT-EXPORT_Activities_File_[DATE].csv

RENXT-EXPORT_Education_File_[DATE].csv

RENXT-EXPORT_Military_File_[DATE].csv

RENXT-EXPORT_Relationships_File_[DATE].csv
```

Create/Export the required file from RENXT:

```text
CT_Process__Existing_IDs.xlsx
```

---

Ensure the following file is updated as needed:

```text
Degree-Location Program Codes.xlsx
```

---

### Step 2

Copy all files into the project root folder.

Example:

```text
C:\Users\kfletcher\Downloads\CTinput
```

---

### Step 3

Run the process.

```powershell
python run_ct_process.py
```

---

### Step 4

Review the generated workbook.

Open:

```text
output\ct_process_review.xlsx
```

Review:

- NEW records
- ConsCodes
- Employment updates
- Education updates
- Relationships
- Warning flags

---

### Step 5

Import new constituents.

Upload:

```text
output\ct_process_import.csv
```

to CT Process.

---

# Operational Validation Checklist

Review the workbook for:

## NEW Constituents

Verify:

```text
ConsCode assigned

Employee

Alumni

Employee + Alumni
```

No NEW record should have blank ConsCode.

---

## Existing Constituents

Verify only recent activity appears.

Education:

```text
graduation date within 90 days
```

Employment:

```text
ORFromDate within 90 days

or

ORToDate within 90 days
```

---

## Degree Translation

Verify:

```text
ESRDegree
```

contains translated values.

---

## Campus Translation

Verify:

```text
ESRCampus
```

contains translated values.

---

## Email Addresses

Verify:

```text
all email values are lowercase
```

---

# Troubleshooting

## Excel Workbook Will Not Save

Error:

```text
PermissionError
```

Cause:

Workbook is already open.

Resolution:

Close the workbook and rerun.

---

## Missing Transformer Module

Error:

```text
No module named transformers.*
```

Resolution:

Verify:

```text
transformers\
    __init__.py
```

exists and the transformer file was copied.

---

## Degree Lookup Issues

Verify:

```text
Degree-Location Program Codes.xlsx
```

contains the expected mappings.

---

# Future Automation Architecture

## Current

```text
RE NXT Export
      ↓
Python
      ↓
Review Workbook
      ↓
CSV
      ↓
CT Process
```

---

## Planned

```text
SharePoint
      ↓
Power Automate
      ↓
Python Runtime
      ↓
Review Workbook
      ↓
CSV
      ↓
CT Process
```

---

# Existing Constituent Update Vision

Future architecture:

```text
RE NXT Export
      ↓
Python Change Detection
      ↓
existing_updates.json
      ↓
Power Automate
      ↓
Blackbaud Connector
      ↓
Update Constituent
```

Potential updates:

```text
Employment

Education

Organizational Relationships
```

This avoids sending EXISTING records back through CT Process and instead updates RE NXT directly.

---

# Release Process

Before committing code:

1. Run test export.
2. Review workbook.
3. Validate diagnostics.
4. Validate schema analysis.
5. Commit changes.
6. Update CHANGELOG.md.

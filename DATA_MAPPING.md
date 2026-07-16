# Data Mapping and Business Rules

This document defines all business logic implemented by the CT Process Constituent Transformation Engine.

---

# Input Sources

## Core Export

```text
RENXT-EXPORT_[DATE].csv
```

Used for:

- Constituent information
- Name information
- Address information
- Employment information
- Phones
- Emails

---

## Activities Export

```text
RENXT-EXPORT_Activities_File_[DATE].csv
```

Used for:

- Education activity injection

---

## Education Export

```text
RENXT-EXPORT_Education_File_[DATE].csv
```

Used for:

- Degrees
- Majors
- Minors
- Attributes
- Class year

---

## Military Export

```text
RENXT-EXPORT_Military_File_[DATE].csv
```

Used for:

- Military service affiliations

---

## Relationship Export

```text
RENXT-EXPORT_Relationships_File_[DATE].csv
```

Used for:

- Personal relationships

---

# Constituent Classification

## Record Status

### NEW

Constituent does not exist in:

```text
CT_Process__Existing_IDs.xlsx
```

Output:

```text
record_status = NEW
```

---

### EXISTING

Constituent exists in:

```text
CT_Process__Existing_IDs.xlsx
```

Output:

```text
record_status = EXISTING
```

---

# ConsCode Rules

## NEW Constituents

### Employment Only

```text
Employment = Yes
Education = No
```

Output:

```text
Employee
```

---

### Education Only

```text
Employment = No
Education = Yes
```

Output:

```text
Alumni
```

---

### Employment and Education

```text
Employment = Yes
Education = Yes
```

Output:

```text
Employee
Alumni
```

---

## Existing Constituents

Current implementation:

```text
ConsCode is informational only.
```

Future updates may automate Constituent Code assignment through RE NXT connectors.

---

# Education Rules

## Degree Translation

Degrees are translated using:

```text
Degree-Location Program Codes.xlsx
```

Example:

```text
ASSOCIATE IN ARTS

↓

Associate in Arts
```

---

## Campus Translation

Campus codes are translated using:

```text
Degree-Location Program Codes.xlsx
```

Example:

```text
MOD

↓

Whiteman AFB, MO (MOD)
```

---

## Existing Constituent Filtering

For EXISTING constituents:

Degrees are retained only when:

```text
graduation_date is within the last 90 days
```

---

## New Constituent Filtering

For NEW constituents:

```text
All education records retained
```

---

# Employment Rules

Employment retained when:

```text
from_date within 90 days

OR

to_date within 90 days
```

This rule applies to:

```text
NEW
EXISTING
```

constituents.

---

# Relationship Rules

Relationships are exported as:

```text
IRLink
IRRelat
IRRecip
```

Relationship records are retained exactly as provided by transformation logic.

---

# Address Rules

## Duplicate Address Suppression

When:

```text
AddrType_2 = AddrType
```

Second address block is cleared.

Fields cleared:

```text
AddrLines_2
AddrCity_2
AddrCountry_2
AddrCounty_2
AddrState_2
AddrZIP_2
AddrSeasFrom_2
AddrType_2
AddrValidFrom_2
AddrValidTo_2
PrefAddr_2
```

---

# Name Normalization

Applied to:

```text
FirstName
MidName
LastName
NickName
AliasName
```

Examples:

```text
Doe-smith
→
Doe-Smith
```

```text
Kerri-ann
→
Kerri-Ann
```

```text
Mcdonald
→
McDonald
```

```text
Mcdougal
→
McDougal
```

---

# Email Normalization

Applied to all email values detected in phone/email output.

Examples:

```text
THISISMYEMAIL@EMAIL.COM

↓

thisismyemail@email.com
```

---

# Export Rules

## CSV

Purpose:

```text
CT Process Import
```

Primary deliverable.

---

## Review Workbook

Purpose:

```text
Human validation
```

Contains:

```text
Grouped columns
Filters
Freeze panes
Section colors
Warnings
```

---

# Future Business Rules

## Existing Constituent Updates

Future architecture:

```text
Python
    ↓
Change Detection
    ↓
JSON Output
    ↓
Power Automate
    ↓
RE NXT Connector
```

Potential automated updates:

```text
Education

Employment

Organizational Relationships
```

without passing the constituent through CT Process.

---

# Source of Truth

In the event of a conflict:

1. DATA_MAPPING.md
2. CHANGELOG.md
3. Source code
4. Legacy documentation

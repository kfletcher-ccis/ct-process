# Changelog

All notable changes to the CT Process Constituent Transformation Engine are documented in this file.

The format is based on:

- Added
- Changed
- Fixed
- Removed

---

# [Unreleased]

## Planned

### Automation

- SharePoint-triggered processing
- Power Automate integration
- Existing constituent update automation
- Run-history tracking
- Email notifications

### RE NXT Integration

- Existing constituent update detection
- Education update JSON output
- Employment update JSON output
- Organizational relationship update JSON output

---

# [2026-07-15]

## Added

### Review Workbook

- XLSX review workbook export
- Grouped workbook sections
- Freeze panes
- Filters
- Color-coded data blocks

### Transformations

- Name normalization
- Email normalization
- Existing-record filtering
- ConsCode generation

### Outputs

- Review workbook generation
- CSV export generation
- Diagnostics report generation
- Schema analysis generation

---

## Changed

### Workbook Layout

Added grouped workbook sections:

```text
Core
Phone
Employment
Education
Military
Relationships
```

### Freeze Pane

Changed from:

```text
A3
```

to:

```text
C3
```

### Export Sorting

NEW constituents are now exported before EXISTING constituents.

### Employment Filtering

Employment is retained only when:

```text
ORFromDate within 90 days

OR

ORToDate within 90 days
```

### Education Filtering

EXISTING constituents retain only degrees where:

```text
ESRDateGrad within 90 days
```

---

## Fixed

### Duplicate Address Block

Second address block is cleared when:

```text
AddrType_2 = AddrType
```

### Major Import IDs

Corrected:

```text
ESRMajESRImpID
```

to appear once per major set.

### Minor Import IDs

Corrected:

```text
ESRMinESRImpID
```

to appear once per minor set.

### Attribute Import IDs

Corrected:

```text
ESRAttrESRImpID
```

to appear once per attribute set.

### Email Formatting

Emails now output as lowercase.

Example:

```text
THISISMYEMAIL@EMAIL.COM

↓

thisismyemail@email.com
```

### Name Formatting

Examples:

```text
Doe-smith
→
Doe-Smith

Kerri-ann
→
Kerri-Ann

Mcdonald
→
McDonald
```

---

## Removed

### Debug Output

Removed:

```text
ASSOCIATE IN ARTS ->
...
```

Removed:

```text
Done
```

in favor of progress reporting and diagnostics.

---

# [2026-07-01]

## Added

### Initial Architecture

- Canonical constituent model
- Degree mapping
- Campus mapping
- Education transformation
- Military transformation
- Relationship transformation
- Existing ID matching

### Outputs

- Constituent JSON
- Diagnostics JSON
- Schema Analysis JSON

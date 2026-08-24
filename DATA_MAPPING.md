# DATA MAPPING

## Canonical Constituent Structure

### Core

Contains original source values.

Examples:

```json
{
  "ORPos": "Adjunct - Distance Education||Adjunct - Mathematics",
  "ORProf": "Online||Mathematics",
  "ORFromDate": "07/20/2026||01/12/2026"
}
```

Core represents source data exactly as received.

---

## Employment Mapping

### Source Fields

| Source | Target |
|----------|----------|
| ORPos | employment.position |
| ORProf | employment.profession |
| ORFromDate | employment.from_date |
| ORToDate | employment.to_date |
| ORIndustry | employment.industry |
| ORFullName | employment.organization |

---

### Employment Processing Rules

#### Positional Alignment

All employment fields are split using:

```text
||
```

while preserving positional alignment.

Example:

```text
ORPos:
A||B

ORFromDate:
2026-07-20||2026-01-12

ORToDate:
N/A||2026-05-03
```

Produces:

```text
Employment 1
    Position A
    From 2026-07-20
    To blank

Employment 2
    Position B
    From 2026-01-12
    To 2026-05-03
```

---

### Null Handling

The following values normalize to blank:

```text
N/A
NA
NULL
NONE
```

---

### Employment Filtering

Only records meeting the configured activity window survive:

```text
120 days
```

A record qualifies when:

```text
from_date within 120 days
OR
to_date within 120 days
```

---

## Education Mapping

### Source

Education export.

### Canonical Structure

```json
{
  "school_name": "...",
  "degree": "...",
  "major": "...",
  "minor": "...",
  "graduation_date": "..."
}
```

---

### Education Filtering

For EXISTING records:

```text
graduation_date
```

must fall within:

```text
120 days
```

For NEW records:

```text
All education records retained
```

---

## Update Detection

### EXISTING Records

Employment update:

```python
len(constituent.employment) > 0
```

Education update:

```python
len(constituent.education) > 0
```

Produces:

```json
{
  "update_flags": {},
  "update_actions": []
}
```

### Supported Actions

```text
EMPLOYMENT
EDUCATION
```

---

## JSON Outputs

### constituents.json

Canonical constituent model.

### diagnostics.json

Processing metrics.

### schema_analysis.json

Dynamic cardinality analysis.

### process_summary.json

Run-level operational reporting.

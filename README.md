# CT Process Constituent Transformation Engine

A Python-based ETL application that transforms Blackbaud Raiser's Edge NXT export files into CT Process import files, review workbooks, diagnostics, and constituent update datasets.

The project was designed to:

- Create NEW constituents for CT Process
- Detect update activity for EXISTING constituents
- Normalize source data
- Improve data quality
- Generate review artifacts prior to import
- Serve as a foundation for future RE NXT automation

---

# Features

## Data Transformation

- Degree translation
- Campus translation
- ConsCode determination
- Name normalization
- Email address normalization
- Relationship processing
- Military processing
- Employment processing
- Activity injection

## Data Quality

- Duplicate address suppression
- Existing-record filtering
- Education filtering
- Employment filtering
- Review workbook generation

## Outputs

- Review Workbook (.xlsx)
- CT Process Import (.csv)
- Constituent JSON
- Diagnostics Report
- Schema Analysis

---

# Project Structure

```text
build_constituents.py

builders/
    constituent_builder.py

helpers/
    common.py
    lookups.py
    name_normalization.py

loaders/
    core_loader.py
    education_loader.py
    activities_loader.py
    military_loader.py
    relationship_loader.py

transformers/
    core_transformer.py
    education_transformer.py
    relationship_transformer.py
    military_transformer.py
    conscode_transformer.py
    recent_filter_transformer.py

exporters/
    csv_exporter.py
    xlsx_review_exporter.py

tests/
    run_milestone1.py
    run_csv_export.py
    run_xlsx_review.py

output/
```

---

# Required Input Files

The application expects:

```text
RENXT-EXPORT_[DATE].csv

RENXT-EXPORT_Activities_File_[DATE].csv

RENXT-EXPORT_Education_File_[DATE].csv

RENXT-EXPORT_Military_File_[DATE].csv

RENXT-EXPORT_Relationships_File_[DATE].csv

CT_Process__Existing_IDs.xlsx

Degree-Location Program Codes.xlsx
```

---

# Installation

## Python Version

Recommended:

```text
Python 3.11+
```

## Install Dependencies

```powershell
pip install pandas
pip install openpyxl
```

---

# Usage

## Generate Review Workbook

```powershell
python tests\run_xlsx_review.py ^
    --input-dir . ^
    --output-dir .\output
```

Outputs:

```text
output\ct_process_review

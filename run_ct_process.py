def progress(step, total, text):
    percent = int(step / total * 100)

    print(
        f"[{step}/{total}] "
        f"{percent:3d}% "
        f"- {text}"
    )

progress(
    1,
    6,
    "Loading lookups"
)

progress(
    2,
    6,
    "Building constituents"
)

progress(
    3,
    6,
    "Applying transformations"
)

progress(
    4,
    6,
    "Generating diagnostics"
)

progress(
    5,
    6,
    "Creating review workbook"
)

progress(
    6,
    6,
    "Creating CSV export"
)



from build_constituents import build_constituents
from exporters.xlsx_review_exporter import XlsxReviewExporter
from exporters.csv_exporter import CsvExporter

from pathlib import Path

from build_constituents import build_constituents
from exporters.xlsx_review_exporter import XlsxReviewExporter
from exporters.csv_exporter import CsvExporter

inp = Path(".")

result = build_constituents(
    core_file=str(next(inp.glob("RENXT-EXPORT_[0-9]*.csv"))),
    activities_file=str(next(inp.glob("RENXT-EXPORT_Activities_File_*.csv"))),
    education_file=str(next(inp.glob("RENXT-EXPORT_Education_File_*.csv"))),
    military_file=str(next(inp.glob("RENXT-EXPORT_Military_File_*.csv"))),
    relationships_file=str(next(inp.glob("RENXT-EXPORT_Relationships_File_*.csv"))),
    existing_ids_file=str(inp / "CT_Process__Existing_IDs.xlsx"),
    lookup_workbook=str(inp / "Degree-Location Program Codes.xlsx"),
)

XlsxReviewExporter(
    result["schema"]
).export(
    result["constituents"],
    "output/ct_process_review.xlsx"
)

CsvExporter(
    result["schema"]
).export(
    result["constituents"],
    "output/ct_process_import.csv"
)

constituents = result["constituents"]

total_count = len(constituents)

new_count = sum(
    1
    for c in constituents.values()
    if c.record_status == "NEW"
)

existing_count = sum(
    1
    for c in constituents.values()
    if c.record_status == "EXISTING"
)

print()
print("Summary")
print("-------")
print(f"Total Constituents : {total_count}")
print(f"New Constituents   : {new_count}")
print(f"Existing Constituents : {existing_count}")

employment_count = sum(
    len(c.employment)
    for c in constituents.values()
)

education_count = sum(
    len(c.education)
    for c in constituents.values()
)

military_count = sum(
    len(c.military)
    for c in constituents.values()
)

relationship_count = sum(
    len(c.relationships)
    for c in constituents.values()
)

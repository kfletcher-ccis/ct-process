"""
Run Milestone 1 pipeline and immediately export CT Process CSV.

Example:
python -m tests.run_csv_export --input-dir . --output-dir .\output
"""

import argparse
from pathlib import Path

from build_constituents import build_constituents
from exporters.csv_exporter import CsvExporter
from serializers.constituent_serializer import ConstituentSerializer
from serializers.output_writer import OutputWriter

parser = argparse.ArgumentParser(description="Build canonical model and export CT Process CSV")
parser.add_argument("--input-dir", default=".")
parser.add_argument("--lookup-workbook", default="Degree-Location Program Codes.xlsx")
parser.add_argument("--existing-ids", default="CT_Process__Existing_IDs.xlsx")
parser.add_argument("--output-dir", default=".")
parser.add_argument("--csv-name", default="ct_process_import_preview.csv")
args = parser.parse_args()

inp = Path(args.input_dir)
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)

result = build_constituents(
    core_file=str(next(inp.glob("RENXT-EXPORT_[0-9]*.csv"))),
    activities_file=str(next(inp.glob("RENXT-EXPORT_Activities_File_*.csv"))),
    education_file=str(next(inp.glob("RENXT-EXPORT_Education_File_*.csv"))),
    military_file=str(next(inp.glob("RENXT-EXPORT_Military_File_*.csv"))),
    relationships_file=str(next(inp.glob("RENXT-EXPORT_Relationships_File_*.csv"))),
    existing_ids_file=str(inp / args.existing_ids),
    lookup_workbook=str(inp / args.lookup_workbook),
)

ConstituentSerializer.write_json(result["constituents"], str(out / "constituents.json"))
OutputWriter.write_json(result["diagnostics"], str(out / "diagnostics.json"))
OutputWriter.write_json(result["schema"], str(out / "schema_analysis.json"))

CsvExporter(result["schema"]).export(
    result["constituents"],
    str(out / args.csv_name),
)

print("CSV export complete")
print(f"Constituents: {len(result['constituents'])}")
print(f"CSV: {out / args.csv_name}")
print(f"Diagnostics: {out / 'diagnostics.json'}")
print(f"Schema: {out / 'schema_analysis.json'}")

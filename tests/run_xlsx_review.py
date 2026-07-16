"""
Run canonical model build and produce formatted XLSX review workbook.

Run from the project root, for example:
python -m tests.run_xlsx_review --input-dir . --output-dir .\output

Or directly:
python tests\run_xlsx_review.py --input-dir . --output-dir .\output
"""

import argparse
import sys
from pathlib import Path

# Allows this script to run either with:
#   python -m tests.run_xlsx_review
# or:
#   python tests\run_xlsx_review.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from build_constituents import build_constituents
from exporters.xlsx_review_exporter import XlsxReviewExporter
from serializers.constituent_serializer import ConstituentSerializer
from serializers.output_writer import OutputWriter


parser = argparse.ArgumentParser(
    description="Build canonical model and export formatted XLSX review workbook"
)
parser.add_argument("--input-dir", default=".")
parser.add_argument("--lookup-workbook", default="Degree-Location Program Codes.xlsx")
parser.add_argument("--existing-ids", default="CT_Process__Existing_IDs.xlsx")
parser.add_argument("--output-dir", default=".")
parser.add_argument("--xlsx-name", default="ct_process_review.xlsx")
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

ConstituentSerializer.write_json(
    result["constituents"],
    str(out / "constituents.json"),
)

OutputWriter.write_json(
    result["diagnostics"],
    str(out / "diagnostics.json"),
)

OutputWriter.write_json(
    result["schema"],
    str(out / "schema_analysis.json"),
)

XlsxReviewExporter(result["schema"]).export(
    result["constituents"],
    str(out / args.xlsx_name),
)

print("XLSX review export complete")
print(f"Constituents: {len(result['constituents'])}")
print(f"Workbook: {out / args.xlsx_name}")
print(f"Diagnostics: {out / 'diagnostics.json'}")
print(f"Schema: {out / 'schema_analysis.json'}")

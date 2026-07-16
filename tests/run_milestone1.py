import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path
from build_constituents import build_constituents
from serializers.constituent_serializer import ConstituentSerializer
from serializers.output_writer import OutputWriter

parser = argparse.ArgumentParser(description="Run Milestone 1 canonical model build")
parser.add_argument("--input-dir", default=".")
parser.add_argument("--lookup-workbook", default="Degree-Location Program Codes.xlsx")
parser.add_argument("--existing-ids", default="CT_Process__Existing_IDs.xlsx")
parser.add_argument("--output-dir", default=".")
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
print("Milestone 1 complete")
print(f"Constituents: {len(result['constituents'])}")
print(f"Diagnostics: {out / 'diagnostics.json'}")
print(f"Schema: {out / 'schema_analysis.json'}")

from pathlib import Path

from build_constituents import build_constituents
from exporters.xlsx_review_exporter import XlsxReviewExporter
from exporters.csv_exporter import CsvExporter

from helpers.file_management import (
    get_required_file,
    get_processing_timestamp,
    create_run_output_folder,
    archive_run_artifacts,
)

from serializers.constituent_serializer import ConstituentSerializer
from serializers.output_writer import OutputWriter

import json

# ----------------------------------------------------------
# Progress display
# ----------------------------------------------------------

def progress(step, total, text):

    percent = int((step / total) * 100)

    print(
        f"[{step}/{total}] "
        f"{percent:3d}% "
        f"- {text}"
    )

TOTAL_STEPS = 8

# ----------------------------------------------------------
# Main Processing
# ----------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
inp = SCRIPT_DIR

print()
print(f"Working Directory : {Path.cwd()}")
print(f"Script Directory  : {SCRIPT_DIR}")
print()

PROJECT_ROOT = Path(__file__).resolve().parent

inp = PROJECT_ROOT

try:

    # ------------------------------------------------------
    # Locate files
    # ------------------------------------------------------

    progress(
        1,
        TOTAL_STEPS,
        "Locating input files"
    )

    core_file = get_required_file(
        inp,
        "RENXT-EXPORT_[0-9]*.csv",
        "Core Export"
    )

    activities_file = get_required_file(
        inp,
        "RENXT-EXPORT_Activities_File_*.csv",
        "Activities Export"
    )

    education_file = get_required_file(
        inp,
        "RENXT-EXPORT_Education_File_*.csv",
        "Education Export"
    )

    military_file = get_required_file(
        inp,
        "RENXT-EXPORT_Military_File_*.csv",
        "Military Export"
    )

    relationships_file = get_required_file(
        inp,
        "RENXT-EXPORT_Relationships_File_*.csv",
        "Relationships Export"
    )

    # ------------------------------------------------------
    # Determine timestamp
    # ------------------------------------------------------

    timestamp = get_processing_timestamp(
        Path(core_file).name
    )

    output_folder = create_run_output_folder(
        SCRIPT_DIR,
        timestamp["folder_date"]
    )

    constituents_file = (
        output_folder
        / f"constituents_{timestamp['raw']}.json"
    )

    diagnostics_file = (
        output_folder
        / f"diagnostics_{timestamp['raw']}.json"
    )

    schema_file = (
        output_folder
        / f"schema_analysis_{timestamp['raw']}.json"
    )

    summary_json_file = (
        output_folder
        / f"process_summary_{timestamp['raw']}.json"
    )

    summary_txt_file = (
        output_folder
        / f"process_summary_{timestamp['raw']}.txt"
    )

    # ------------------------------------------------------
    # Build model
    # ------------------------------------------------------

    progress(
        2,
        TOTAL_STEPS,
        "Building constituent model"
    )

    result = build_constituents(
        core_file=core_file,
        activities_file=activities_file,
        education_file=education_file,
        military_file=military_file,
        relationships_file=relationships_file,
        existing_ids_file=str(
            inp / "CT_Process__Existing_IDs.xlsx"
        ),
        lookup_workbook=str(
            inp / "Degree-Location Program Codes.xlsx"
        ),
    )

    # ------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------

    progress(
        3,
        TOTAL_STEPS,
        "Creating constituents JSON"
    )

    ConstituentSerializer.write_json(
        result["constituents"],
        str(constituents_file),
    )

    progress(
        4,
        TOTAL_STEPS,
        "Creating diagnostics JSON"
    )

    OutputWriter.write_json(
        result["diagnostics"],
        str(diagnostics_file),
    )

    progress(
        5,
        TOTAL_STEPS,
        "Creating schema analysis JSON"
    )

    OutputWriter.write_json(
        result["schema"],
        str(schema_file),
    )

    constituents = result["constituents"]

    # ------------------------------------------------------
    # Review Workbook
    # ------------------------------------------------------

    progress(
        6,
        TOTAL_STEPS,
        "Creating review workbook"
    )

    review_file = (
        output_folder
        / f"ct_process_review_{timestamp['raw']}.xlsx"
    )

    XlsxReviewExporter(
        result["schema"]
    ).export(
        constituents,
        str(review_file)
    )

    # ------------------------------------------------------
    # CSV Export
    # ------------------------------------------------------

    progress(
        7,
        TOTAL_STEPS,
        "Creating CSV export"
    )

    csv_file = (
        output_folder
        / f"ct_process_import_{timestamp['raw']}.csv"
    )

    CsvExporter(
        result["schema"]
    ).export(
        constituents,
        str(csv_file)
    )

    # ------------------------------------------------------
    # Archive Inputs
    # ------------------------------------------------------

    archive_run_artifacts(
        project_root=SCRIPT_DIR,
        timestamp=timestamp,
        review_file=review_file,
        csv_file=csv_file,
        constituents_file=constituents_file,
        diagnostics_file=diagnostics_file,
        schema_file=schema_file,
        summary_json_file=summary_json_file,
        summary_txt_file=summary_txt_file,
    )

    progress(
        8,
        TOTAL_STEPS,
        "Archiving processed files"
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

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

    existing_employment_updates = sum(
        1
        for c in constituents.values()
        if (
            c.record_status == "EXISTING"
            and c.update_flags.get(
                "needs_employment_update",
                False
            )
        )
    )

    existing_education_updates = sum(
        1
        for c in constituents.values()
        if (
            c.record_status == "EXISTING"
            and c.update_flags.get(
                "needs_education_update",
                False
            )
        )
    )

    existing_any_updates = sum(
        1
        for c in constituents.values()
        if (
            c.record_status == "EXISTING"
            and c.update_flags.get(
                "needs_update",
                False
            )
        )
    )

    summary_payload = {
        "run_timestamp": timestamp["raw"],
        "run_folder": timestamp["folder_date"],

        "total_constituents": total_count,
        "new_constituents": new_count,
        "existing_constituents": existing_count,

        "employment_records": employment_count,
        "education_records": education_count,
        "military_records": military_count,
        "relationship_records": relationship_count,

        "existing_employment_updates":
            existing_employment_updates,

        "existing_education_updates":
            existing_education_updates,

        "existing_any_updates":
            existing_any_updates,

        "generated_files": {
            "constituents_json": str(constituents_file),
            "diagnostics_json": str(diagnostics_file),
            "schema_analysis_json": str(schema_file),
            "review_workbook": str(review_file),
            "csv_export": str(csv_file)
        }
    }

    with open(
        summary_json_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary_payload,
            f,
            indent=2,
            ensure_ascii=False
        )

    with open(
        summary_txt_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "CT PROCESS SUMMARY\n"
        )

        f.write(
            "=" * 60 + "\n\n"
        )

        f.write(
            f"Run Timestamp          : "
            f"{timestamp['raw']}\n"
        )

        f.write(
            f"Total Constituents     : "
            f"{total_count}\n"
        )

        f.write(
            f"New Constituents       : "
            f"{new_count}\n"
        )

        f.write(
            f"Existing Constituents  : "
            f"{existing_count}\n"
        )

        f.write(
            f"Employment Records     : "
            f"{employment_count}\n"
        )

        f.write(
            f"Education Records      : "
            f"{education_count}\n"
        )

        f.write(
            f"Military Records       : "
            f"{military_count}\n"
        )

        f.write(
            f"Relationship Records   : "
            f"{relationship_count}\n"
        )

        f.write("\n")

        f.write(
            "EXISTING RECORD UPDATE ACTIONS\n"
        )

        f.write(
            "-" * 60 + "\n"
        )

        f.write(
            f"Employment Updates     : "
            f"{existing_employment_updates}\n"
        )

        f.write(
            f"Education Updates      : "
            f"{existing_education_updates}\n"
        )

        f.write(
            f"Any Update Needed      : "
            f"{existing_any_updates}\n"
        )

        f.write("\n")

        f.write(
            "GENERATED FILES\n"
        )

        f.write(
            "-" * 60 + "\n"
        )

        f.write(
            f"Constituents JSON      : "
            f"{constituents_file.name}\n"
        )

        f.write(
            f"Diagnostics JSON       : "
            f"{diagnostics_file.name}\n"
        )

        f.write(
            f"Schema Analysis JSON   : "
            f"{schema_file.name}\n"
        )

        f.write(
            f"Review Workbook        : "
            f"{review_file.name}\n"
        )

        f.write(
            f"CSV Export             : "
            f"{csv_file.name}\n"
        )

    print()
    print("=" * 60)
    print("PROCESS SUMMARY")
    print("=" * 60)

    print(
        f"Total Constituents      : {total_count}"
    )

    print(
        f"New Constituents        : {new_count}"
    )

    print(
        f"Existing Constituents   : {existing_count}"
    )

    print(
        f"Employment Records      : {employment_count}"
    )

    print(
        f"Education Records       : {education_count}"
    )

    print(
        f"Military Records        : {military_count}"
    )

    print(
        f"Relationship Records    : {relationship_count}"
    )
    print()
    print("EXISTING RECORD UPDATE ACTIONS")
    print("-" * 60)

    print(
        f"Employment Updates      : "
        f"{existing_employment_updates}"
    )

    print(
        f"Education Updates       : "
        f"{existing_education_updates}"
    )

    print(
        f"Any Update Needed       : "
        f"{existing_any_updates}"
    )

    print()
    print(
        f"Review Workbook: {review_file}"
    )

    print(
        f"CSV Export: {csv_file}"
    )

except Exception as ex:

    print()
    print("=" * 60)
    print("GENERATED FILES")
    print("=" * 60)

    print(
        f"Constituents JSON : {constituents_file}"
    )

    print(
        f"Diagnostics JSON  : {diagnostics_file}"
    )

    print(
        f"Schema Analysis   : {schema_file}"
    )

    print(
        f"Review Workbook   : {review_file}"
    )

    print(
        f"CSV Export        : {csv_file}"
    )

    print()
    print("=" * 60)
    print("PROCESS FAILED")
    print("=" * 60)

    print(str(ex))

    raise
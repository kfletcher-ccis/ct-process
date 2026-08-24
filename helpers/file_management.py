from pathlib import Path
from shutil import move
import re

def get_required_file(folder, pattern, description):
    """
    Returns the first matching file.

    Raises FileNotFoundError if no match exists.
    Warns if multiple files match.
    """

    matches = list(folder.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"{description} not found ({pattern}) in {folder.resolve()}"
        )

    latest = max(
        matches,
        key=lambda p: p.stat().st_mtime
    )

    if len(matches) > 1:
        print(
            f"WARNING: Multiple {description} files found. "
            f"Using newest file: {latest.name}"
        )

    return str(latest)


def get_processing_timestamp(filename):
    """
    Example input:

        RENXT-EXPORT_19-08-2026_12-34-55.csv

    Returns:

    {
        "day": "19",
        "month": "08",
        "year": "2026",
        "time": "12-34-55",
        "raw": "19-08-2026_12-34-55",
        "folder_date": "2026-08-19"
    }
    """

    match = re.search(
        r"(\d{2})-(\d{2})-(\d{4})_(\d{2}-\d{2}-\d{2})",
        filename
    )

    if not match:
        raise ValueError(
            f"Unable to determine timestamp from {filename}"
        )

    day, month, year, time_part = match.groups()

    return {
        "day": day,
        "month": month,
        "year": year,
        "time": time_part,
        "raw": f"{day}-{month}-{year}_{time_part}",
        "folder_date": f"{year}-{month}-{day}"
    }


def create_run_output_folder(root_path, folder_date):
    """
    Creates:

        output/2026-08-19/
    """

    output_folder = (
        Path(root_path)
        / "output"
        / folder_date
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_folder

def archive_run_artifacts(
    project_root,
    timestamp,
    review_file,
    csv_file,
    constituents_file=None,
    diagnostics_file=None,
    schema_file=None,
    summary_json_file=None,
    summary_txt_file=None,
):

    root = Path(project_root)

    archive_folder = (
        root
        / "output"
        / timestamp["folder_date"]
    )

    archive_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    #
    # Move source CSVs
    #

    source_patterns = [
        "RENXT-EXPORT_[0-9]*.csv",
        "RENXT-EXPORT_Activities_File_*.csv",
        "RENXT-EXPORT_Education_File_*.csv",
        "RENXT-EXPORT_Military_File_*.csv",
        "RENXT-EXPORT_Relationships_File_*.csv",
    ]

    moved_count = 0

    for pattern in source_patterns:

        for file in root.glob(pattern):

            move(
                str(file),
                str(
                    archive_folder
                    / file.name
                )
            )

            moved_count += 1

    #
    # Copy Existing IDs workbook
    #

    existing_ids_file = (
        root
        / "CT_Process__Existing_IDs.xlsx"
    )

    if existing_ids_file.exists():

        renamed_file = (
            archive_folder
            / (
                "CT_Process__Existing_IDs_"
                f"{timestamp['raw']}.xlsx"
            )
        )

        move(
            str(existing_ids_file),
            str(renamed_file)
        )

    #
    # Move generated outputs
    #

    output_files = [
        review_file,
        csv_file,
        constituents_file,
        diagnostics_file,
        schema_file,
    ]

    for file in output_files:

        if not file:
            continue

        file = Path(file)

        if file.exists():

            move(
                str(file),
                str(
                    archive_folder
                    / file.name
                )
            )

    print()
    print(
        f"Archived {moved_count} source files to:"
    )
    print(
        archive_folder
    )
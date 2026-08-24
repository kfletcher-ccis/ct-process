from pathlib import Path
from shutil import move
import re


def archive_source_files(root_folder):
    root = Path(root_folder)

    core_files = list(
        root.glob("RENXT-EXPORT_*.csv")
    )

    if not core_files:
        print("No source files found.")
        return

    source_file = core_files[0]

    match = re.search(
        r"(\\d{2})-(\\d{2})-(\\d{4})_(\\d{2}-\\d{2}-\\d{2})",
        source_file.name
    )

    if not match:
        raise ValueError(
            f"Could not determine timestamp from {source_file.name}"
        )

    day, month, year, time_part = match.groups()

    archive_date = f"{year}-{month}-{day}"

    archive_folder = (
        root
        / "OLD"
        / archive_date
    )

    archive_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Move source CSVs
    for pattern in [
        "RENXT-EXPORT_*.csv",
        "RENXT-EXPORT_Activities_File_*.csv",
        "RENXT-EXPORT_Education_File_*.csv",
        "RENXT-EXPORT_Military_File_*.csv",
        "RENXT-EXPORT_Relationships_File_*.csv",
    ]:

        for file in root.glob(pattern):

            move(
                str(file),
                str(archive_folder / file.name)
            )

    # Rename and move Existing IDs workbook

    existing_ids = (
        root
        / "CT_Process__Existing_IDs.xlsx"
    )

    if existing_ids.exists():

        renamed = (
            archive_folder
            / f"CT_Process__Existing_IDs_{day}-{month}-{year}_{time_part}.xlsx"
        )

        move(
            str(existing_ids),
            str(renamed)
        )

    print(
        f"Archived source files to: "
        f"{archive_folder}"
    )
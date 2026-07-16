"""
Lookup loading and translation utilities.
"""

import pandas as pd

from loaders.base_loader import (
    load_excel_detect_header
)
from helpers.common import clean_null_value


class LookupManager:

    def __init__(self):

        self.degree_lookup = {}
        self.campus_lookup = {}

        self.degree_misses = set()
        self.campus_misses = set()

    # ---------------------------------------------------------
    # Degree Lookup
    # ---------------------------------------------------------

    def load_degree_lookup(
        self,
        workbook_path,
        sheet_name="Degree Codes"
    ):

        df = load_excel_detect_header(
            workbook_path,
            {
                "Academic Program",
                "Title",
                "RE Degree"
            }
        )

        self.degree_lookup = {}

        for _, row in df.iterrows():

            source = clean_null_value(
                row.get("Title", "")
            ).upper()

            if not source:
                continue

            self.degree_lookup[source] = {
                "degree": clean_null_value(
                    row.get("RE Degree", "")
                ),
                "major": clean_null_value(
                    row.get("RE Major", "")
                )
            }

    # ---------------------------------------------------------
    # Campus Lookup
    # ---------------------------------------------------------

    def load_campus_lookup(
        self,
        workbook_path,
        sheet_name="Location Codes"
    ):

        df = pd.read_excel(
            workbook_path,
            sheet_name=sheet_name,
            engine="openpyxl"
        )

        self.campus_lookup = {}

        for _, row in df.iterrows():

            source = clean_null_value(
                row.get("Location Code", "")
            ).upper()

            if not source:
                continue

            self.campus_lookup[source] = (
                clean_null_value(
                    row.get("RE Location", "")
                )
            )

    # ---------------------------------------------------------
    # Translators
    # ---------------------------------------------------------

    def translate_degree(
        self,
        source_degree
    ):

        key = clean_null_value(
            source_degree
        ).upper()

        if not key:
            return {
                "degree": "",
                "major": ""
            }

        result = self.degree_lookup.get(key)

        if result is None:

            self.degree_misses.add(key)

            return {
                "degree": "",
                "major": ""
            }

        return result

    def translate_campus(
        self,
        source_campus
    ):

        key = clean_null_value(
            source_campus
        ).upper()

        if not key:
            return ""

        result = self.campus_lookup.get(key)

        if result is None:

            self.campus_misses.add(key)

            return ""

        return result

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def get_diagnostics(self):

        return {

            "degree_lookup_misses":
                sorted(
                    list(self.degree_misses)
                ),

            "campus_lookup_misses":
                sorted(
                    list(self.campus_misses)
                )
        }
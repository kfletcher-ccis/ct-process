"""
Recent-record filtering for CT Process ETL output.

Rules implemented:
- Employment records are retained only when from_date or to_date is within the last N days,
  regardless of NEW/EXISTING status. This prevents old employment from appearing for NEW records.
- Education records are filtered only for EXISTING constituents. Existing constituents retain only
  degrees whose graduation_date is within the last N days. NEW constituents retain all education.

Recommended builder order:
1. Attach all records.
2. Apply ConsCodeTransformer so NEW classifications can use the full model.
3. Apply RecentFilterTransformer so review/CSV output includes only relevant recent records.
"""

from __future__ import annotations
from helpers.common import is_within_last_days


class RecentFilterTransformer:
    def __init__(self, days: int = 90):
        self.days = days

    def apply(self, constituent):
        # Employment: filter for both NEW and EXISTING.
        constituent.employment = [
            employment for employment in (constituent.employment or [])
            if (
                is_within_last_days(employment.from_date, self.days)
                or is_within_last_days(employment.to_date, self.days)
            )
        ]

        # Education: filter only for EXISTING people. NEW people retain all education.
        if constituent.record_status == "EXISTING":
            constituent.education = [
                degree for degree in (constituent.education or [])
                if is_within_last_days(degree.graduation_date, self.days)
            ]

        return constituent

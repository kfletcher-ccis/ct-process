"""End-to-end CT Process CSV exporter."""

import csv
from exporters.csv_schema_builder import CsvSchemaBuilder
from exporters.education_block_exporter import EducationBlockExporter
from exporters.relationship_block_exporter import RelationshipBlockExporter
from config import PROTECTED_COLUMNS


class CsvExporter:
    def __init__(self, schema_analysis, remove_empty_columns=True):
        self.schema_analysis = schema_analysis
        self.remove_empty_columns = remove_empty_columns
        self.schema_builder = CsvSchemaBuilder()
        self.education_exporter = EducationBlockExporter(
            max_degree_records=schema_analysis.get("max_degree_records", 0),
            max_major_records=schema_analysis.get("max_major_records", 0),
            max_minor_records=schema_analysis.get("max_minor_records", 0),
            max_attribute_records=schema_analysis.get("max_attribute_records", 0),
        )
        self.relationship_exporter = RelationshipBlockExporter(
            max_relationship_records=schema_analysis.get("max_relationship_records", 0)
        )

    def export(self, constituents, output_file):
        headers = self.schema_builder.build_headers(self.schema_analysis)
        rows = [self._build_row(c) for c in self._sorted_constituents(constituents)]

        if self.remove_empty_columns:
            headers, rows = self._remove_empty_columns(headers, rows)

        with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def _sorted_constituents(self, constituents):
        return sorted(
            constituents.values(),
            key=lambda c: (c.record_status != "NEW", c.lookup_id)
        )

    def _build_row(self, constituent):
        row = []
        row.extend(self._core_values(constituent))
        row.extend(self._phone_values(constituent))
        row.extend(self._employment_values(constituent))
        row.extend(self.education_exporter.export(constituent))
        row.extend(self._military_values(constituent))
        row.extend(self.relationship_exporter.export(constituent))
        return row

    def _core_values(self, constituent):
        core = constituent.core or {}
        return [
            constituent.record_status,
            constituent.lookup_id,
            core.get("ConsCode", ""),
            core.get("ConsCode_2", ""),
            core.get("Titl1", ""), core.get("FirstName", ""), core.get("MidName", ""), core.get("LastName", ""), core.get("Suff1", ""), core.get("NickName", ""),
            core.get("AliasType", ""), core.get("AliasName", ""), core.get("AliasType_2", ""), core.get("AliasName_2", ""),
            core.get("AliasType_3", ""), core.get("AliasName_3", ""), core.get("AliasType_4", ""), core.get("AliasName_4", ""),
            core.get("AliasType_5", ""), core.get("AliasName_5", ""), core.get("AliasType_6", ""), core.get("AliasName_6", ""),
            core.get("AliasType_7", ""), core.get("AliasName_7", ""), core.get("AliasType_8", ""), core.get("AliasName_8", ""),
            core.get("Bplace", ""), core.get("Bday", ""), core.get("SolCode", ""), core.get("KeyInd", ""),
            core.get("AddrLines", ""), core.get("AddrCity", ""), core.get("AddrCountry", ""), core.get("AddrCounty", ""), core.get("AddrState", ""), core.get("AddrZIP", ""), core.get("AddrSeasFrom", ""), core.get("AddrType", ""), core.get("AddrValidFrom", ""), core.get("AddrValidTo", ""), core.get("PrefAddr", ""),
            core.get("AddrLines_2", ""), core.get("AddrCity_2", ""), core.get("AddrCountry_2", ""), core.get("AddrCounty_2", ""), core.get("AddrState_2", ""), core.get("AddrZIP_2", ""), core.get("AddrSeasFrom_2", ""), core.get("AddrType_2", ""), core.get("AddrValidFrom_2", ""), core.get("AddrValidTo_2", ""), core.get("PrefAddr_2", ""),
            core.get("Gender", ""), core.get("Religion", ""), core.get("MrtlStat", ""),
        ]

    def _phone_values(self, constituent):
        values = []
        phones = constituent.phones or []
        for i in range(self.schema_analysis.get("max_phone_records", 0)):
            if i < len(phones):
                phone = phones[i]
                values.extend([phone.phone_type, phone.phone_value, self._bool_text(phone.is_primary)])
            else:
                values.extend(["", "", ""])
        return values

    def _employment_values(self, constituent):
        values = []
        records = constituent.employment or []
        for i in range(self.schema_analysis.get("max_employment_records", 0)):
            if i < len(records):
                emp = records[i]
                values.extend([
                    emp.organization, emp.position, emp.profession, emp.from_date, emp.to_date, emp.industry,
                    self._bool_text(emp.is_employer), self._bool_text(emp.is_primary), emp.relationship, emp.reciprocal,
                ])
            else:
                values.extend([""] * 10)
        return values

    def _military_values(self, constituent):
        values = []
        records = constituent.military or []
        for i in range(self.schema_analysis.get("max_military_records", 0)):
            if i < len(records):
                mil = records[i]
                values.extend([
                    mil.organization, mil.service_type, mil.branch,
                    self._bool_text(mil.is_employer), self._bool_text(mil.is_primary), mil.relationship, mil.reciprocal,
                ])
            else:
                values.extend([""] * 7)
        return values

    def _remove_empty_columns(self, headers, rows):
        if not rows:
            return headers, rows
        keep_indexes = []
        for idx, header in enumerate(headers):
            if header in PROTECTED_COLUMNS:
                keep_indexes.append(idx)
                continue
            if any(row[idx] not in (None, "") for row in rows):
                keep_indexes.append(idx)
        return [headers[i] for i in keep_indexes], [[row[i] for i in keep_indexes] for row in rows]

    @staticmethod
    def _bool_text(value):
        if value is True:
            return "TRUE"
        if value is False:
            return "FALSE"
        return ""

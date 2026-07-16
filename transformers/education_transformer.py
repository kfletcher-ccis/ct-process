from collections import defaultdict
from models import DegreeRecord, MajorRecord, MinorRecord, AttributeRecord
from helpers.common import normalize_lookup_id, clean_null_value, date_sort_key, year_from_date, build_import_id, repeated_values

class EducationTransformer:
    def __init__(self, lookup_manager):
        self.lookup_manager = lookup_manager

    def transform_dataframe(self, education_df, activity_map):
        grouped = defaultdict(list)
        for _, row in education_df.iterrows():
            lookup_id = normalize_lookup_id(row.get("ConsID", ""))
            grouped[lookup_id].append(row)
        results = {}
        for lookup_id, rows in grouped.items():
            results[lookup_id] = self._transform_degrees(rows, activity_map.get(lookup_id, []))
        return results

    def _transform_degrees(self, rows, activities):
        sorted_rows = sorted(rows, key=lambda r: (date_sort_key(r.get("ESRDateGrad", ""), ascending=False), date_sort_key(r.get("ESRDateEnt", ""), ascending=True)), reverse=True)
        results=[]
        for row_counter, row in enumerate(sorted_rows, start=1):
            degree = self._build_degree(row, row_counter)
            if degree:
                results.append(degree)
        # Activity injection: constituent-level activities attach only to primary sorted degree.
        if results and activities:
            primary = results[0]
            lookup_id = normalize_lookup_id(rows[0].get("ConsID", ""))
            for activity in activities:
                primary.attributes.append(AttributeRecord(
                    category=activity.category,
                    description=activity.description,
                    import_id=build_import_id(lookup_id, "ATT", primary.graduation_date, 1)
                ))
        return results

    def _build_degree(self, row, row_counter):
        lookup_id = normalize_lookup_id(row.get("ConsID", ""))
        degree_lookup = self.lookup_manager.translate_degree(row.get("ESRDegree", ""))
        if degree_lookup.get("degree") == "** DO NOT IMPORT TO RE **":
            return None
        degree = DegreeRecord(
            school_name=clean_null_value(row.get("ESRSchoolName", "")),
            entry_date=clean_null_value(row.get("ESRDateEnt", "")),
            left_date=clean_null_value(row.get("ESRDateLeft", "")),
            graduation_date=clean_null_value(row.get("ESRDateGrad", "")),
            degree=degree_lookup.get("degree", ""),
            campus=self.lookup_manager.translate_campus(row.get("ESRCampus", "")),
            primary_alumni=""
        )
        if degree.school_name == "Columbia College":
            degree.class_of = year_from_date(degree.graduation_date)
        self._build_majors(degree, row, lookup_id, row_counter, degree_lookup)
        self._build_minors(degree, row, lookup_id, row_counter)
        self._build_attributes(degree, row, lookup_id, row_counter)
        return degree

    def _build_majors(self, degree, row, lookup_id, row_counter, degree_lookup):
        majors = repeated_values(row, "ESRMajMajor", 10)
        # If source has no major but degree lookup provides RE Major, use it as a fallback.
        if not majors and degree_lookup.get("major"):
            majors = [degree_lookup["major"]]
        for major in majors:
            degree.majors.append(MajorRecord(major=major, import_id=build_import_id(lookup_id, "MAJ", degree.graduation_date, row_counter)))

    def _build_minors(self, degree, row, lookup_id, row_counter):
        for minor in repeated_values(row, "ESRMinMinor", 10):
            degree.minors.append(MinorRecord(minor=minor, import_id=build_import_id(lookup_id, "MIN", degree.graduation_date, row_counter)))

    def _build_attributes(self, degree, row, lookup_id, row_counter):
        for attr in repeated_values(row, "ESRAttrDesc", 20):
            degree.attributes.append(AttributeRecord(category="Honors", description=attr, import_id=build_import_id(lookup_id, "ATT", degree.graduation_date, row_counter)))

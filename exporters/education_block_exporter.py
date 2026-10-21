"""Education block flattener with one ImpID per major/minor/attribute set."""


class EducationBlockExporter:
    def __init__(self, max_degree_records, max_major_records, max_minor_records, max_attribute_records):
        self.max_degree_records = max_degree_records
        self.max_major_records = max_major_records
        self.max_minor_records = max_minor_records
        self.max_attribute_records = max_attribute_records

    def export(self, constituent):
        values = []
        degrees = constituent.education or []

        for degree_index in range(self.max_degree_records):
            if degree_index < len(degrees):
                values.extend(self._degree_values(degrees[degree_index]))
            else:
                values.extend(self._blank_degree_values())

        return values

    def _degree_values(self, degree):
        values = [
            degree.school_name,
            degree.entry_date,
            degree.left_date,
            degree.degree,
            degree.graduation_date,
            degree.class_of,
            degree.campus,
            degree.primary_alumni,
        ]

        # One major ImpID for the whole major set.
        values.append(degree.majors[0].import_id if degree.majors else "")
        for i in range(self.max_major_records):
            values.append(degree.majors[i].major if i < len(degree.majors) else "")

        # One minor ImpID for the whole minor set.
        values.append(degree.minors[0].import_id if degree.minors else "")
        for i in range(self.max_minor_records):
            values.append(degree.minors[i].minor if i < len(degree.minors) else "")

        # One attribute ImpID for the whole attribute set.
        values.append(degree.attributes[0].import_id if degree.attributes else "")
        for i in range(self.max_attribute_records):
            if i < len(degree.attributes):
                attr = degree.attributes[i]
                values.extend([attr.category, attr.description])
            else:
                values.extend(["", ""])

        return values

    def _blank_degree_values(self):
        width = 8
        width += 1 + self.max_major_records
        width += 1 + self.max_minor_records
        width += 1 + (self.max_attribute_records * 2)
        return [""] * width

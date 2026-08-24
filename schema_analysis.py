class SchemaAnalyzer:
    def analyze(self, constituents):
        result = {
            "max_phone_records": 0,
            "max_employment_records": 0,
            "max_degree_records": 0,
            "max_major_records": 0,
            "max_minor_records": 0,
            "max_attribute_records": 0,
            "max_military_records": 0,
            "max_relationship_records": 0,
        }
        for c in constituents.values():
            result["max_phone_records"] = max(result["max_phone_records"], len(c.phones))
            result["max_employment_records"] = max(result["max_employment_records"], len(c.employment))
            result["max_degree_records"] = max(result["max_degree_records"], len(c.education))
            result["max_military_records"] = max(result["max_military_records"], len(c.military))
            result["max_relationship_records"] = max(result["max_relationship_records"], len(c.relationships))
            for d in c.education:
                result["max_major_records"] = max(result["max_major_records"], len(d.majors))
                result["max_minor_records"] = max(result["max_minor_records"], len(d.minors))
                result["max_attribute_records"] = max(result["max_attribute_records"], len(d.attributes))
        return result

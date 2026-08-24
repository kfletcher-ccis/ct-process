class Diagnostics:
    def __init__(self):
        self.warning_messages = []
        self.degree_lookup_misses = set()
        self.campus_lookup_misses = set()
        self.relationship_warnings = []
        self.loader_counts = {}

    def analyze_constituents(self, constituents):
        output = {
            "loader_counts": self.loader_counts,
            "total_constituents": len(constituents),
            "new_records": 0,
            "existing_records": 0,
            "phone_records": 0,
            "employment_records": 0,
            "degree_records": 0,
            "military_records": 0,
            "relationship_records": 0,
            "new_employee": 0,
            "new_alumni": 0,
            "new_dual": 0,
            "new_blank": 0,
            "existing_needing_employment_update": 0,
            "existing_needing_education_update": 0,
            "existing_needing_both_updates": 0,
            "existing_needing_any_update": 0,
            "existing_needing_no_update": 0,
            "degree_lookup_misses": sorted(self.degree_lookup_misses),
            "campus_lookup_misses": sorted(self.campus_lookup_misses),
            "relationship_warnings": self.relationship_warnings,
            "warnings": self.warning_messages,
        }
        for c in constituents.values():
            if c.record_status == "NEW": output["new_records"] += 1
            else: output["existing_records"] += 1
            output["phone_records"] += len(c.phones)
            output["employment_records"] += len(c.employment)
            output["degree_records"] += len(c.education)
            output["military_records"] += len(c.military)
            output["relationship_records"] += len(c.relationships)
            if c.record_status == "EXISTING":
                flags = c.update_flags or {}
                employment_update = flags.get(
                    "needs_employment_update",
                    False
                )
                education_update = flags.get(
                    "needs_education_update",
                    False
                )
                if employment_update:
                    output[
                        "existing_needing_employment_update"
                    ] += 1
                if education_update:
                    output[
                        "existing_needing_education_update"
                    ] += 1
                if (
                    employment_update
                    and education_update
                ):
                    output[
                        "existing_needing_both_updates"
                    ] += 1
                if (
                    employment_update
                    or education_update
                ):
                    output[
                        "existing_needing_any_update"
                    ] += 1
                else:
                    output[
                        "existing_needing_no_update"
                    ] += 1
        return output

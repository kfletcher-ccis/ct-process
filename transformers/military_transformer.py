from collections import defaultdict
from models import MilitaryRecord
from helpers.common import normalize_lookup_id, split_pipe_values, safe_get

class MilitaryTransformer:
    def transform_dataframe(self, df):
        results = defaultdict(list)
        for _, row in df.iterrows():
            lookup_id = normalize_lookup_id(row.get("ConsID", ""))
            service_types = split_pipe_values(row.get("ORProf", ""))
            branches = split_pipe_values(row.get("ORIndustry", ""))
            max_count = max(len(service_types), len(branches))
            for i in range(max_count):
                results[lookup_id].append(MilitaryRecord(service_type=safe_get(service_types, i), branch=safe_get(branches, i)))
        return results

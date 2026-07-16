from collections import defaultdict
from models import AttributeRecord
from helpers.common import normalize_lookup_id, split_pipe_values

class ActivitiesTransformer:
    def transform_dataframe(self, df):
        results = defaultdict(list)
        for _, row in df.iterrows():
            lookup_id = normalize_lookup_id(row.get("ConsID", ""))
            for activity in split_pipe_values(row.get("ESRAttrDesc", "")):
                results[lookup_id].append(AttributeRecord(category="Student Activity", description=activity, import_id=""))
        return results

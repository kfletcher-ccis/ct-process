from collections import defaultdict
from models import RelationshipRecord
from helpers.common import normalize_lookup_id, split_pipe_values
from config import RELATIONSHIP_MAPPINGS

class RelationshipTransformer:
    def __init__(self):
        self.warnings = []

    def transform_dataframe(self, df):
        results = defaultdict(list)
        for _, row in df.iterrows():
            lookup_id = normalize_lookup_id(row.get("ConsID", ""))
            self._build_children(results[lookup_id], row)
            self._build_parents(results[lookup_id], row)
            self._build_named_relationships(results[lookup_id], row, lookup_id)
        return results

    def _build_children(self, records, row):
        # First IRLink column: related party is Child; reciprocal is Parent.
        for related_id in split_pipe_values(row.get("IRLink", "")):
            records.append(RelationshipRecord(related_lookup_id=normalize_lookup_id(related_id), relationship="Child", reciprocal="Parent"))

    def _build_parents(self, records, row):
        # Second IRLink column: related party is Parent; reciprocal is Child.
        for related_id in split_pipe_values(row.get("IRLink_2", "")):
            records.append(RelationshipRecord(related_lookup_id=normalize_lookup_id(related_id), relationship="Parent", reciprocal="Child"))

    def _build_named_relationships(self, records, row, lookup_id):
        values = split_pipe_values(row.get("IRLink_3", ""))
        for i in range(0, len(values), 2):
            if i + 1 >= len(values):
                self.warnings.append(f"Unpaired IRLink_3 value for lookup_id={lookup_id}: {values[i]}")
                continue
            related_id = normalize_lookup_id(values[i])
            source_rel = values[i + 1]
            relat, recip = RELATIONSHIP_MAPPINGS.get(source_rel, (source_rel, source_rel))
            records.append(RelationshipRecord(related_lookup_id=related_id, relationship=relat, reciprocal=recip))

    def get_warnings(self):
        return list(self.warnings)

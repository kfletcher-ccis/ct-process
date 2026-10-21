"""
Relationship block flattener.

Each RelationshipRecord becomes:
    IRLink, IRRelat, IRRecip
"""


class RelationshipBlockExporter:
    def __init__(self, max_relationship_records):
        self.max_relationship_records = max_relationship_records

    def export(self, constituent):
        values = []
        records = constituent.relationships or []

        for i in range(self.max_relationship_records):
            if i < len(records):
                relationship = records[i]
                values.extend([
                    relationship.related_lookup_id,
                    relationship.relationship,
                    relationship.reciprocal,
                ])
            else:
                values.extend(["", "", ""])

        return values

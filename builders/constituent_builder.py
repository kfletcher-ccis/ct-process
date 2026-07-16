from transformers.conscode_transformer import ConsCodeTransformer
from transformers.recent_filter_transformer import RecentFilterTransformer

class ConstituentBuilder:

    def __init__(
        self,
        core_transformer,
        education_transformer,
        activities_transformer,
        military_transformer,
        relationship_transformer,
        conscode_transformer=None
    ):
        self.core_transformer = core_transformer
        self.education_transformer = education_transformer
        self.activities_transformer = activities_transformer
        self.military_transformer = military_transformer
        self.relationship_transformer = relationship_transformer

        self.conscode_transformer = (
            conscode_transformer
            if conscode_transformer
            else ConsCodeTransformer()
        )

    def build_constituents(self, core_df, education_df, activities_df, military_df, relationships_df):
        constituents = {}
        for _, row in core_df.iterrows():
            c = self.core_transformer.transform_row(row)
            constituents[c.lookup_id] = c
        activity_map = self.activities_transformer.transform_dataframe(activities_df)
        education_map = self.education_transformer.transform_dataframe(education_df, activity_map)
        military_map = self.military_transformer.transform_dataframe(military_df)
        relationship_map = self.relationship_transformer.transform_dataframe(relationships_df)
        for lookup_id, records in education_map.items():
            if lookup_id in constituents:
                constituents[lookup_id].education = records
        for lookup_id, records in military_map.items():
            if lookup_id in constituents:
                constituents[lookup_id].military = records
        for lookup_id, records in relationship_map.items():
            if lookup_id in constituents:
                constituents[
                    lookup_id
                ].relationships = records
                
        # Apply ConsCode rules first so NEW values are based on the full model.
        for constituent in constituents.values():
            self.conscode_transformer.apply(constituent)

        # Then filter output records for recent activity.
        recent_filter_transformer = RecentFilterTransformer(days=90)
        for constituent in constituents.values():
            recent_filter_transformer.apply(constituent)

        return constituents
from loaders.core_loader import load_core
from loaders.education_loader import load_education
from loaders.activities_loader import load_activities
from loaders.military_loader import load_military
from loaders.relationships_loader import load_relationships
from loaders.existing_ids_loader import load_existing_ids
from helpers.lookups import LookupManager
from transformers.core_transformer import CoreTransformer
from transformers.education_transformer import EducationTransformer
from transformers.activities_transformer import ActivitiesTransformer
from transformers.military_transformer import MilitaryTransformer
from transformers.relationship_transformer import RelationshipTransformer
from builders.constituent_builder import ConstituentBuilder
from diagnostics import Diagnostics
from schema_analysis import SchemaAnalyzer

def build_constituents(core_file, education_file, activities_file, military_file, relationships_file, existing_ids_file, lookup_workbook):
    core_df = load_core(core_file)
    education_df = load_education(education_file)
    activities_df = load_activities(activities_file)
    military_df = load_military(military_file)
    relationships_df = load_relationships(relationships_file)
    existing_ids_map = load_existing_ids(existing_ids_file)

    lookups = LookupManager()
    lookups.load_degree_lookup(lookup_workbook)
    lookups.load_campus_lookup(lookup_workbook)

    relationship_transformer = RelationshipTransformer()
    builder = ConstituentBuilder(
        CoreTransformer(existing_ids_map),
        EducationTransformer(lookups),
        ActivitiesTransformer(),
        MilitaryTransformer(),
        relationship_transformer,
    )
    constituents = builder.build_constituents(core_df, education_df, activities_df, military_df, relationships_df)

    diagnostics = Diagnostics()
    diagnostics.loader_counts = {
        "core_rows": len(core_df),
        "education_rows": len(education_df),
        "activities_rows": len(activities_df),
        "military_rows": len(military_df),
        "relationship_rows": len(relationships_df),
        "existing_id_rows": len(existing_ids_map),
    }
    diagnostics.degree_lookup_misses = lookups.degree_misses
    diagnostics.campus_lookup_misses = lookups.campus_misses
    diagnostics.relationship_warnings = relationship_transformer.get_warnings()

    return {
        "constituents": constituents,
        "diagnostics": diagnostics.analyze_constituents(constituents),
        "schema": SchemaAnalyzer().analyze(constituents),
    }

PROTECTED_COLUMNS = {"ESRPrimAlum"}
NULL_VALUES = {"", "NA", "N/A", "NULL", "(null)", "NONE"}
CORE_ORGANIZATION_NAME = "Columbia College"
MILITARY_ORGANIZATION_NAME = "United States Military"
RELATIONSHIP_MAPPINGS = {
    "Brother": ("Sibling", "Sibling"),
    "Sister": ("Sibling", "Sibling"),
    "Grandfather": ("Grandparent", "Grandchild"),
    "Grandmother": ("Grandparent", "Grandchild"),
}
OUTPUT_CONSTITUENTS = "constituents.json"
OUTPUT_DIAGNOSTICS = "diagnostics.json"
OUTPUT_SCHEMA = "schema_analysis.json"

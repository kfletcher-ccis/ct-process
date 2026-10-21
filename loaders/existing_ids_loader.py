from loaders.base_loader import load_excel_detect_header
from helpers.common import normalize_lookup_id, clean_null_value

def load_existing_ids(file_path: str):
    df = load_excel_detect_header(file_path, {"lookup_id", "sky_id"})
    result = {}
    for _, row in df.iterrows():
        lookup_id = normalize_lookup_id(row.get("lookup_id", ""))
        if not lookup_id:
            continue
        sky_raw = clean_null_value(row.get("sky_id", ""))
        try:
            sky_id = int(float(sky_raw)) if sky_raw else None
        except ValueError:
            sky_id = None
        result[lookup_id] = {
            "sky_id": sky_id,
            "cons_import_id": clean_null_value(row.get("ConsImportID", "")) or None,
        }
    return result

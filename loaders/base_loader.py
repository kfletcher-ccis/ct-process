from __future__ import annotations
import pandas as pd
from helpers.common import normalize_duplicate_columns

def load_csv(file_path):
    """
    Load a CT Process CSV using the expected UTF-8 encoding first.

    Some RENXT exports may contain Windows-1252 characters such as
    non-breaking spaces. If UTF-8 decoding fails, retry using cp1252.
    """

    common_options = {
        "dtype": str,
        "skip_blank_lines": True,
        "keep_default_na": False,
    }

    try:
        return pd.read_csv(
            file_path,
            encoding="utf-8",
            **common_options
        )

    except UnicodeDecodeError:
        print()
        print(
            f"UTF-8 decoding failed for {file_path}."
        )
        print(
            "Retrying with Windows-1252 encoding..."
        )

        return pd.read_csv(
            file_path,
            encoding="cp1252",
            **common_options
        )

def load_excel_detect_header(file_path: str, required_headers: set[str]):
    raw = pd.read_excel(file_path, header=None, dtype=str, engine="openpyxl", keep_default_na=False)
    header_idx = None
    for idx, row in raw.iterrows():
        vals = {str(v).strip() for v in row.tolist() if str(v).strip()}
        if required_headers.issubset(vals):
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError(f"Could not detect header row containing {required_headers} in {file_path}")
    headers = [str(v).strip() for v in raw.iloc[header_idx].tolist()]
    df = raw.iloc[header_idx+1:].copy()
    df.columns = headers
    df = df.loc[:, [c for c in df.columns if c and c != 'nan']]
    df.columns = normalize_duplicate_columns(df.columns)
    return df.reset_index(drop=True)

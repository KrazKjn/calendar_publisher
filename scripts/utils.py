# utils.py

import os

def validate_csv_path(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    if not path.lower().endswith(".csv"):
        raise ValueError(f"Invalid file type: {path} (expected .csv)")

def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)

def get_first_folder_from_path(path_str):
    parts = path_str.strip("/").split("/")
    return parts[0] if parts else None

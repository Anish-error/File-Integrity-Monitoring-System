import json
from pathlib import Path


def create_baseline(file_hashes):
    """Return a baseline dictionary from {relative_path: SHA-256} hashes."""
    return dict(file_hashes)


def save_baseline(path, baseline):
    """Save baseline hashes as JSON."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4, sort_keys=True)


def load_baseline(path):
    """Load baseline hashes from JSON."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid baseline format: expected a JSON object.")
    return data

import hashlib
from pathlib import Path


def hash_file(file_path):
    """Calculate a file's SHA-256 hash without loading it all into memory."""
    digest = hashlib.sha256()

    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)

    return digest.hexdigest()


def calculate_file_hashes(folder):
    """Return hashes for every regular file under folder, using relative paths."""
    folder = Path(folder)
    hashes = {}

    for path in sorted(folder.rglob("*")):
        if path.is_file():
            relative_path = path.relative_to(folder).as_posix()
            hashes[relative_path] = hash_file(path)

    return hashes

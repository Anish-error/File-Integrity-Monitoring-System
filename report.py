from datetime import datetime
from pathlib import Path


def generate_report(report_path, current_hashes, baseline, changes, first_run=False):
    """Write a readable summary of the most recent scan."""
    report_path = Path(report_path)

    if first_run:
        lines = [
            "FILE INTEGRITY MONITORING REPORT",
            "=" * 32,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Scan type: Initial baseline creation",
            f"Files recorded in baseline: {len(current_hashes)}",
            "",
            "No comparison was performed on this first run.",
        ]
    else:
        modified = sorted(name for name, status in changes.items() if status == "MODIFIED")
        deleted = sorted(name for name, status in changes.items() if status == "DELETED")
        new = sorted(name for name, status in changes.items() if status == "NEW")
        unchanged = sorted(
            name for name in (set(current_hashes) & set(baseline))
            if current_hashes[name] == baseline[name]
        )

        lines = [
            "FILE INTEGRITY MONITORING REPORT",
            "=" * 32,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Scan type: Comparison with saved baseline",
            f"Files currently found: {len(current_hashes)}",
            f"Unchanged files: {len(unchanged)}",
            f"Modified files: {len(modified)}",
            f"Deleted files: {len(deleted)}",
            f"New files: {len(new)}",
            "",
            "DETECTED CHANGES",
            "-" * 16,
        ]

        if not changes:
            lines.append("No changes detected.")
        else:
            for status, names in (
                ("MODIFIED", modified),
                ("DELETED", deleted),
                ("NEW", new),
            ):
                for name in names:
                    lines.append(f"[{status}] {name}")

        lines.extend(["", "UNCHANGED FILES", "-" * 15])
        lines.extend(unchanged or ["None"])

    with report_path.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")

from pathlib import Path

from baseline import create_baseline, load_baseline, save_baseline
from hasher import calculate_file_hashes
from logger_config import setup_logger
from report import generate_report

PROJECT_DIR = Path(__file__).resolve().parent
MONITORED_DIR = PROJECT_DIR / "monitored_files"
BASELINE_FILE = PROJECT_DIR / "baseline.json"
REPORT_FILE = PROJECT_DIR / "report.txt"
LOG_FILE = PROJECT_DIR / "integrity.log"


def monitor_files():
    """Create a baseline on the first run; compare hashes on later runs."""
    logger = setup_logger(LOG_FILE)
    MONITORED_DIR.mkdir(exist_ok=True)

    files_now = calculate_file_hashes(MONITORED_DIR)

    if not BASELINE_FILE.exists():
        baseline = create_baseline(files_now)
        save_baseline(BASELINE_FILE, baseline)
        message = (
            "Baseline created successfully. Run the program again after "
            "changing files in the monitored_files folder to detect changes."
        )
        print(message)
        logger.info(message)
        generate_report(REPORT_FILE, files_now, {}, [], first_run=True)
        print(f"Baseline saved to: {BASELINE_FILE.name}")
        print(f"Report saved to:   {REPORT_FILE.name}")
        return

    baseline = load_baseline(BASELINE_FILE)
    changes = {}
    current_names = set(files_now)
    baseline_names = set(baseline)

    for name in sorted(current_names & baseline_names):
        if files_now[name] != baseline[name]:
            changes[name] = "MODIFIED"

    for name in sorted(baseline_names - current_names):
        changes[name] = "DELETED"

    for name in sorted(current_names - baseline_names):
        changes[name] = "NEW"

    if not changes:
        print("No changes detected. All monitored files match the baseline.")
        logger.info("Scan completed: no changes detected.")
    else:
        print("Changes detected:")
        for name, status in changes.items():
            print(f"  [{status}] {name}")
            logger.warning("%s: %s", status, name)

    generate_report(REPORT_FILE, files_now, baseline, changes, first_run=False)
    print(f"\nLog saved to:    {LOG_FILE.name}")
    print(f"Report saved to: {REPORT_FILE.name}")
    print("\nNote: The baseline is not automatically updated. This preserves the")
    print("original reference until you deliberately reset it.")

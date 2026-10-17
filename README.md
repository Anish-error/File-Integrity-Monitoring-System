<<<<<<< HEAD
# File Integrity Monitor (Python)

A beginner-friendly project that checks whether files have been modified, deleted, or added by comparing their SHA-256 hashes with a saved baseline.

## Requirements

- Python 3.8 or newer
- No external packages required

## Project structure

```text
File_Integrity_Monitor/
├── main.py
├── monitor.py
├── baseline.py
├── hasher.py
├── logger_config.py
├── report.py
├── baseline.json          # created on first run
├── integrity.log          # created when the program runs
├── report.txt             # created when the program runs
└── monitored_files/
    └── sample.txt
```

## Run the project

1. Extract the ZIP file.
2. Open a terminal in the `File_Integrity_Monitor` folder.
3. Run:

   ```bash
   python main.py
   ```

4. On the first run, the program creates `baseline.json` with hashes of files in `monitored_files/`.
5. Edit `monitored_files/sample.txt`, add a file, or remove a file.
6. Run `python main.py` again. The program reports modified, new, and deleted files.

## Important notes

- Only files inside `monitored_files/` are scanned.
- The first run creates the baseline; it does not detect changes on that same run.
- The baseline is deliberately not updated automatically. This allows later scans to compare against the original reference.
- To start over with a fresh baseline, close the program and delete `baseline.json`. Then run `python main.py` again. This replaces the reference with the files currently in `monitored_files/`.
- `integrity.log` and `report.txt` are saved in the project folder.
- SHA-256 checks content integrity; it does not identify who changed a file or prove that a file is safe.
- For a stronger security design, keep the baseline somewhere an untrusted user cannot edit.

## Quick test

1. Run the program once.
2. Open `monitored_files/sample.txt` and change its text.
3. Run the program again.
4. Check the console, `integrity.log`, and `report.txt` for a `MODIFIED` result.
=======
# File-Integrity-Monitoring-System
>>>>>>> 5c7896ff572caff254b977b28f3e49b40f180fc2

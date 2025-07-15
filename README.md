# CSV to SQLite Import Tool

This tool helps streamline the process of generating a SQLite database from a collection of CSV files and a SQL schema. It includes two core utilities:

1. **`generate_sqlite.py`** — Imports CSV data into a SQLite database based on a schema.
2. **`get_column_names.py`** — Prints column names from each CSV file in a folder.

## Features

- Automatically creates a SQLite database from a schema file.
- Imports all `.csv` files in the specified directory into matching tables.
- Retries CSVs that fail due to dependency order (e.g., foreign key constraints).
- Skips empty files silently.
- Minimal console output for clean logs.

## Usage

### 1. Generate SQLite Database

Ensure `schema.sql` and your `.csv` files are in the same folder. Then run:

```bash
python generate_sqlite.py
```

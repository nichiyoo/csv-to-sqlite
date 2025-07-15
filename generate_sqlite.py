import os
import sqlite3
import pandas as pd
from collections import deque


def generate_sqlite(db: str, schema: str, folder: str) -> None:
    """
    Creates a new SQLite database from a schema file and imports all CSV files from a folder into corresponding tables.

    Args:
        db (str): Path to the SQLite database file to create.
        schema (str): Filename of the SQL schema file located inside the folder.
        folder (str): Path to the folder containing the schema and CSV files.

    Notes:
        - If the database already exists, it will be deleted.
        - CSV filenames (without extension) must match table names defined in the schema.
        - CSVs that fail to import due to dependency issues will be retried.
        - Empty CSV files are skipped silently.
    """
    if os.path.exists(db):
        os.remove(db)

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    schema_path = os.path.join(folder, schema)
    if not os.path.exists(schema_path):
        return

    with open(schema_path, "r") as f:
        for stmt in f.read().split(";"):
            if stmt.strip():
                try:
                    cur.execute(stmt)
                except sqlite3.Error:
                    pass
        conn.commit()

    done = set()
    files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    queue = deque(files)
    retry = {f: 0 for f in files}
    retries = len(files) + 1

    while queue:
        f = queue.popleft()
        if f in done or retry[f] >= retries:
            continue

        path = os.path.join(folder, f)
        table = os.path.splitext(f)[0]

        try:
            df = pd.read_csv(path)
            df.to_sql(table, conn, if_exists="append", index=False)
            done.add(f)
        except pd.errors.EmptyDataError:
            done.add(f)
        except (sqlite3.OperationalError, sqlite3.IntegrityError):
            retry[f] += 1
            queue.append(f)
        except Exception:
            pass

    conn.close()


def main() -> None:
    """
    Entry point for running the SQLite generation using the current directory.
    Assumes 'schema.sql' and CSV files are located in the current working directory.
    """
    cdir = os.getcwd()

    data = os.path.join(cdir, "data")
    schema = os.path.join(cdir, "schema.sql")
    database = os.path.join(cdir, "database.sqlite")

    generate_sqlite(database, schema, data)


if __name__ == "__main__":
    main()

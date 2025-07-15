import os
import pandas as pd


def get_column_names(folder: str) -> None:
    """
    Prints the column names of all CSV files in the specified folder.

    Args:
        folder (str): Path to the folder containing CSV files.
    """
    if not os.path.isdir(folder):
        return

    found = False
    for fname in os.listdir(folder):
        if not fname.endswith(".csv"):
            continue

        found = True
        path = os.path.join(folder, fname)

        try:
            df = pd.read_csv(path, nrows=0)
            print(f"{fname}: {', '.join(df.columns)}")
        except pd.errors.EmptyDataError:
            pass
        except Exception:
            pass

    if not found:
        print("No CSV files found.")


def main() -> None:
    """
    Entry point to scan current directory for CSV files and list their columns.
    """
    cdir = os.getcwd()
    data = os.path.join(cdir, "data")

    get_column_names(data)


if __name__ == "__main__":
    main()

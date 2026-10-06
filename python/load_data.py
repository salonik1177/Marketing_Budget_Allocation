
from pathlib import Path
import duckdb

# Locate the project and data folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Create a persistent DuckDB database
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"
con = duckdb.connect(str(DB_PATH))

# Map each table to its Parquet file
files = {
    "channels": "channels.parquet",
    "campaigns": "campaigns.parquet",
    "ad_groups": "ad_groups.parquet",
    "daily_performance": "daily_performance.parquet",
    "conversions": "conversions.parquet",
}

try:
    # Load each Parquet file into a DuckDB table
    for table_name, file_name in files.items():
        file_path = DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing file: {file_path}"
            )

        path_sql = file_path.as_posix().replace("'", "''")

        con.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_parquet('{path_sql}')
            """
        )

        print(f"Loaded table: {table_name}")

    # Verify row counts
    print("\n--- ROW COUNTS ---")

    for table_name in files:
        count = con.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(f"{table_name}: {count:,} rows")

    # Preview daily performance data
    print("\n--- DAILY PERFORMANCE PREVIEW ---")

    con.sql("""
        SELECT *
        FROM daily_performance
        LIMIT 5
    """).show()

    print(f"\nDatabase saved at: {DB_PATH}")

finally:
    con.close()
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:

    con.execute("""
        COPY channel_performance
        TO 'channel_performance.csv'
        WITH (HEADER, DELIMITER ',')
    """)

    con.execute("""
        COPY campaign_performance
        TO 'campaign_performance.csv'
        WITH (HEADER, DELIMITER ',')
    """)

    print("\nPower BI files exported successfully.")

    print("Created:")
    print(" - channel_performance.csv")
    print(" - campaign_performance.csv")

finally:
    con.close()
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    query = """
        SELECT
            DATE_TRUNC('month', activity_date) AS month,
            SUM(impressions) AS impressions,
            SUM(clicks) AS clicks,
            SUM(spend) AS spend,
            SUM(conversions) AS conversions,
            SUM(conversion_value) AS conversion_value
        FROM daily_performance
        GROUP BY 1
        ORDER BY 1
    """

    df = con.execute(query).df()

    output_path = BASE_DIR / "monthly_performance.csv"
    df.to_csv(output_path, index=False)

    print("\nMonthly performance table created.")
    print(f"Rows: {len(df)}")
    print(f"Saved to: {output_path}")

finally:
    con.close()
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    result = con.execute("""
        SELECT
            COUNT(*) AS total_campaigns,
            COUNT(*) FILTER (
                WHERE active_days > 0
            ) AS campaigns_with_activity,
            COUNT(*) FILTER (
                WHERE spend > 0
            ) AS campaigns_with_spend,
            COUNT(*) FILTER (
                WHERE spend > budget
            ) AS campaigns_over_budget
        FROM campaign_performance
    """).fetchone()

    print("\n--- CAMPAIGN VALIDATION ---")
    print(f"Total campaigns:          {result[0]}")
    print(f"Campaigns with activity:  {result[1]}")
    print(f"Campaigns with spend:     {result[2]}")
    print(f"Campaigns over budget:    {result[3]}")

finally:
    con.close()
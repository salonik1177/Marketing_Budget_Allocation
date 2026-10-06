
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    print("\n--- CHANNEL BUDGET ALLOCATION ANALYSIS ---")

    query = """
        WITH campaign_performance AS (
            SELECT
                a.campaign_id,
                SUM(p.spend) AS total_spend,
                SUM(p.conversions) AS total_conversions,
                SUM(p.conversion_value) AS conversion_value
            FROM ad_groups a
            JOIN daily_performance p
                ON a.ad_group_id = p.ad_group_id
            GROUP BY a.campaign_id
        )

        SELECT
            ch.channel_name,
            ch.is_paid,

            COUNT(DISTINCT c.campaign_id) AS campaigns,

            COUNT(DISTINCT c.campaign_id) FILTER (
                WHERE cp.campaign_id IS NOT NULL
            ) AS campaigns_with_activity,

            ROUND(SUM(c.budget), 2) AS total_listed_budget,

            ROUND(
                SUM(COALESCE(cp.total_spend, 0)), 2
            ) AS total_spend,

            ROUND(
                100.0 * SUM(COALESCE(cp.total_spend, 0))
                / NULLIF(SUM(c.budget), 0),
                2
            ) AS spend_to_budget_pct,

            SUM(COALESCE(cp.total_conversions, 0))
                AS total_conversions,

            ROUND(
                SUM(COALESCE(cp.conversion_value, 0)), 2
            ) AS conversion_value,

            ROUND(
                SUM(COALESCE(cp.conversion_value, 0))
                / NULLIF(SUM(COALESCE(cp.total_spend, 0)), 0),
                2
            ) AS roas

        FROM campaigns c

        JOIN channels ch
            ON c.channel_id = ch.channel_id

        LEFT JOIN campaign_performance cp
            ON c.campaign_id = cp.campaign_id

        GROUP BY
            ch.channel_name,
            ch.is_paid

        ORDER BY total_spend DESC
    """

    df = con.execute(query).df()
    print(df.to_string(index=False))

    output_path = BASE_DIR / "channel_budget_analysis.csv"
    df.to_csv(output_path, index=False)

    print(f"\nResults saved to: {output_path}")

finally:
    con.close()
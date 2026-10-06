
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    print("\n--- CAMPAIGN BUDGET ANALYSIS ---")

    query = """
        WITH campaign_performance AS (
            SELECT
                a.campaign_id,
                SUM(p.spend) AS total_spend,
                SUM(p.conversions) AS total_conversions,
                SUM(p.conversion_value) AS total_conversion_value,
                SUM(p.clicks) AS total_clicks,
                SUM(p.impressions) AS total_impressions

            FROM ad_groups a
            JOIN daily_performance p
                ON a.ad_group_id = p.ad_group_id

            GROUP BY a.campaign_id
        )

        SELECT
            c.campaign_id,
            c.campaign_name,
            ch.channel_name,
            c.objective,
            c.budget,

            COALESCE(cp.total_spend, 0) AS total_spend,

            ROUND(
                c.budget - COALESCE(cp.total_spend, 0),
                2
            ) AS budget_remaining,

            ROUND(
                100.0 * COALESCE(cp.total_spend, 0)
                / NULLIF(c.budget, 0),
                2
            ) AS budget_utilization_pct,

            COALESCE(cp.total_conversions, 0)
                AS total_conversions,

            ROUND(
                COALESCE(cp.total_conversion_value, 0),
                2
            ) AS total_conversion_value,

            ROUND(
                COALESCE(cp.total_conversion_value, 0)
                / NULLIF(cp.total_spend, 0),
                2
            ) AS roas

        FROM campaigns c

        JOIN channels ch
            ON c.channel_id = ch.channel_id

        LEFT JOIN campaign_performance cp
            ON c.campaign_id = cp.campaign_id

        ORDER BY budget_utilization_pct DESC NULLS LAST
    """

    df = con.execute(query).df()

    print(df.head(20).to_string(index=False))

    output_path = BASE_DIR / "budget_analysis.csv"
    df.to_csv(output_path, index=False)

    print(f"\nFull results saved to: {output_path}")

finally:
    con.close()

from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    print("\n--- CAMPAIGN PERFORMANCE ANALYSIS ---")

    query = """
        SELECT
            c.campaign_id,
            c.campaign_name,
            ch.channel_name,
            c.objective,
            c.budget,

            SUM(p.impressions) AS impressions,
            SUM(p.clicks) AS clicks,
            ROUND(SUM(p.spend), 2) AS spend,
            SUM(p.conversions) AS conversions,

            ROUND(SUM(p.conversion_value), 2)
                AS conversion_value,

            ROUND(
                SUM(p.conversion_value)
                / NULLIF(SUM(p.spend), 0),
                2
            ) AS roas,

            ROUND(
                SUM(p.spend)
                / NULLIF(SUM(p.conversions), 0),
                2
            ) AS cpa,

            ROUND(
                100.0 * SUM(p.spend)
                / NULLIF(c.budget, 0),
                2
            ) AS budget_utilization_pct

        FROM campaigns c

        JOIN channels ch
            ON c.channel_id = ch.channel_id

        JOIN ad_groups a
            ON c.campaign_id = a.campaign_id

        JOIN daily_performance p
            ON a.ad_group_id = p.ad_group_id

        GROUP BY
            c.campaign_id,
            c.campaign_name,
            ch.channel_name,
            c.objective,
            c.budget

        ORDER BY conversion_value DESC
    """

    df = con.execute(query).df()

    print(df.head(20).to_string(index=False))

    # Export the full campaign analysis
    output_path = BASE_DIR / "campaign_analysis.csv"
    df.to_csv(output_path, index=False)

    print(f"\nFull results saved to: {output_path}")

finally:
    con.close()
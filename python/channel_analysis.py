
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    print("\n--- CHANNEL PERFORMANCE ANALYSIS ---")

    query = """
        SELECT
            ch.channel_name,
            ch.medium,
            ch.is_paid,

            SUM(p.impressions) AS impressions,
            SUM(p.clicks) AS clicks,
            ROUND(SUM(p.spend), 2) AS spend,
            SUM(p.conversions) AS conversions,

            ROUND(SUM(p.conversion_value), 2)
                AS conversion_value,

            -- Click-through rate (%)
            ROUND(
                100.0 * SUM(p.clicks)
                / NULLIF(SUM(p.impressions), 0),
                2
            ) AS ctr_pct,

            -- Cost per click
            ROUND(
                SUM(p.spend)
                / NULLIF(SUM(p.clicks), 0),
                2
            ) AS cpc,

            -- Conversion rate (%)
            ROUND(
                100.0 * SUM(p.conversions)
                / NULLIF(SUM(p.clicks), 0),
                2
            ) AS conversion_rate_pct,

            -- Cost per conversion
            ROUND(
                SUM(p.spend)
                / NULLIF(SUM(p.conversions), 0),
                2
            ) AS cpa,

            -- Return on ad spend, based on conversion value
            ROUND(
                SUM(p.conversion_value)
                / NULLIF(SUM(p.spend), 0),
                2
            ) AS roas

        FROM daily_performance p

        JOIN ad_groups a
            ON p.ad_group_id = a.ad_group_id

        JOIN campaigns c
            ON a.campaign_id = c.campaign_id

        JOIN channels ch
            ON c.channel_id = ch.channel_id

        GROUP BY
            ch.channel_name,
            ch.medium,
            ch.is_paid

        ORDER BY spend DESC
    """

    df = con.execute(query).df()
    print(df.to_string(index=False))

finally:
    con.close()
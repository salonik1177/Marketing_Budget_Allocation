from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

con = duckdb.connect(str(DB_PATH))

try:

    # ============================================================
    # 1. CHANNEL PERFORMANCE TABLE
    # ============================================================

    con.execute("""
        CREATE OR REPLACE TABLE channel_performance AS

        SELECT
            ch.channel_id,
            ch.channel_name,
            ch.medium,
            ch.is_paid,

            SUM(p.impressions) AS impressions,
            SUM(p.clicks) AS clicks,
            SUM(p.spend) AS spend,
            SUM(p.conversions) AS conversions,
            SUM(p.conversion_value) AS conversion_value,

            ROUND(
                100.0 * SUM(p.clicks)
                / NULLIF(SUM(p.impressions), 0),
                2
            ) AS ctr_pct,

            ROUND(
                SUM(p.spend)
                / NULLIF(SUM(p.clicks), 0),
                2
            ) AS cpc,

            ROUND(
                100.0 * SUM(p.conversions)
                / NULLIF(SUM(p.clicks), 0),
                2
            ) AS conversion_rate_pct,

            ROUND(
                SUM(p.spend)
                / NULLIF(SUM(p.conversions), 0),
                2
            ) AS cpa,

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
            ch.channel_id,
            ch.channel_name,
            ch.medium,
            ch.is_paid
    """)


    # ============================================================
    # 2. CAMPAIGN PERFORMANCE TABLE
    # ============================================================
    
    con.execute("""
    CREATE OR REPLACE TABLE campaign_performance AS

    WITH performance AS (

        SELECT
            a.campaign_id,

            MIN(p.activity_date) AS first_activity_date,
            MAX(p.activity_date) AS last_activity_date,

            COUNT(DISTINCT p.activity_date)
                AS active_days,

            SUM(p.impressions) AS impressions,
            SUM(p.clicks) AS clicks,
            SUM(p.spend) AS spend,
            SUM(p.conversions) AS conversions,
            SUM(p.conversion_value) AS conversion_value

        FROM ad_groups a

        JOIN daily_performance p
            ON a.ad_group_id = p.ad_group_id

        GROUP BY
            a.campaign_id
    )

    SELECT
        c.campaign_id,
        c.campaign_name,
        c.channel_id,
        ch.channel_name,

        c.objective,
        c.started_on,
        c.ended_on,
        c.budget,

        perf.first_activity_date,
        perf.last_activity_date,

        COALESCE(perf.active_days, 0)
            AS active_days,

        COALESCE(perf.impressions, 0)
            AS impressions,

        COALESCE(perf.clicks, 0)
            AS clicks,

        COALESCE(perf.spend, 0)
            AS spend,

        COALESCE(perf.conversions, 0)
            AS conversions,

        COALESCE(perf.conversion_value, 0)
            AS conversion_value,

        ROUND(
            100.0 * COALESCE(perf.clicks, 0)
            / NULLIF(COALESCE(perf.impressions, 0), 0),
            2
        ) AS ctr_pct,

        ROUND(
            COALESCE(perf.spend, 0)
            / NULLIF(COALESCE(perf.clicks, 0), 0),
            2
        ) AS cpc,

        ROUND(
            100.0 * COALESCE(perf.conversions, 0)
            / NULLIF(COALESCE(perf.clicks, 0), 0),
            2
        ) AS conversion_rate_pct,

        ROUND(
            COALESCE(perf.spend, 0)
            / NULLIF(COALESCE(perf.conversions, 0), 0),
            2
        ) AS cpa,

        ROUND(
            COALESCE(perf.conversion_value, 0)
            / NULLIF(COALESCE(perf.spend, 0), 0),
            2
        ) AS roas,

        ROUND(
            100.0 * COALESCE(perf.spend, 0)
            / NULLIF(c.budget, 0),
            2
        ) AS budget_utilization_pct

    FROM campaigns c

    JOIN channels ch
        ON c.channel_id = ch.channel_id

    LEFT JOIN performance perf
        ON c.campaign_id = perf.campaign_id
""")
    # ============================================================
    # 3. VALIDATION
    # ============================================================

    print("\n--- ANALYTICAL TABLES CREATED ---")

    print("\nChannel Performance:")
    con.sql("""
        SELECT *
        FROM channel_performance
        ORDER BY spend DESC
    """).show()

    print("\nCampaign Performance:")
    con.sql("""
        SELECT
            campaign_id,
            campaign_name,
            channel_name,
            objective,
            budget,
            spend,
            conversions,
            conversion_value,
            roas,
            budget_utilization_pct
        FROM campaign_performance
        ORDER BY conversion_value DESC
        LIMIT 10
    """).show()


    # ============================================================
    # 4. RECONCILIATION
    # ============================================================

    print("\n--- RECONCILIATION ---")

    con.sql("""
        SELECT
            SUM(spend) AS total_spend,
            SUM(conversions) AS total_conversions,
            SUM(conversion_value) AS total_conversion_value
        FROM channel_performance
    """).show()

    con.sql("""
        SELECT
            SUM(spend) AS total_spend,
            SUM(conversions) AS total_conversions,
            SUM(conversion_value) AS total_conversion_value
        FROM campaign_performance
    """).show()


    print("\nAnalytical tables successfully created.")

finally:
    con.close()
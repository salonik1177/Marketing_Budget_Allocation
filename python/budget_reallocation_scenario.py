
from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "marketing_analytics.duckdb"

TRANSFER_RATE = 0.10  # Transfer 10% of donor channel spend

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    query = """
        WITH campaign_performance AS (
            SELECT
                a.campaign_id,
                SUM(p.spend) AS spend,
                SUM(p.conversion_value) AS conversion_value
            FROM ad_groups a
            JOIN daily_performance p
                ON a.ad_group_id = p.ad_group_id
            GROUP BY a.campaign_id
        )

        SELECT
            ch.channel_name,
            SUM(COALESCE(cp.spend, 0)) AS spend,
            SUM(COALESCE(cp.conversion_value, 0))
                AS conversion_value,

            SUM(COALESCE(cp.conversion_value, 0))
                / NULLIF(SUM(COALESCE(cp.spend, 0)), 0)
                AS roas

        FROM campaigns c
        JOIN channels ch
            ON c.channel_id = ch.channel_id
        LEFT JOIN campaign_performance cp
            ON c.campaign_id = cp.campaign_id

        WHERE ch.is_paid = TRUE

        GROUP BY ch.channel_name
        HAVING SUM(COALESCE(cp.spend, 0)) > 0
    """

    df = con.execute(query).df()

finally:
    con.close()

    print("\n--- SANITY CHECKS ---")
print("Number of paid channels:", len(df))
print("Total channel spend:", df["spend"].sum())
print("Total conversion value:", df["conversion_value"].sum())

print("\n--- CHANNEL VALUES ---")
print(
    df[["channel_name", "spend", "conversion_value", "roas"]]
    .sort_values("roas")
    .to_string(index=False)
)

# Identify the lowest- and highest-ROAS channels
donor_idx = df["roas"].idxmin()
receiver_idx = df["roas"].idxmax()

donor = df.loc[donor_idx, "channel_name"]
receiver = df.loc[receiver_idx, "channel_name"]

# Calculate transfer amount
transfer_amount = df.loc[donor_idx, "spend"] * TRANSFER_RATE

# Baseline totals
baseline_spend = df["spend"].sum()
baseline_value = df["conversion_value"].sum()

# Scenario allocation
df["scenario_spend"] = df["spend"]

df.loc[donor_idx, "scenario_spend"] -= transfer_amount
df.loc[receiver_idx, "scenario_spend"] += transfer_amount

# Estimate conversion value using historical channel ROAS
df["scenario_conversion_value"] = (
    df["scenario_spend"] * df["roas"]
)

df["scenario_change_value"] = (
    df["scenario_conversion_value"] - df["conversion_value"]
)

scenario_spend = df["scenario_spend"].sum()
scenario_value = df["scenario_conversion_value"].sum()

# Validation checks
assert abs(scenario_spend - baseline_spend) < 0.01
assert abs(
    df["scenario_spend"].sum() - df["spend"].sum()
) < 0.01

print("\n--- HYPOTHETICAL BUDGET REALLOCATION ---")
print(f"Donor channel: {donor}")
print(f"Receiving channel: {receiver}")
print(f"Transfer amount: {transfer_amount:,.2f}")

print("\n--- BASELINE VS SCENARIO ---")
print(f"Baseline spend: {baseline_spend:,.2f}")
print(f"Scenario spend: {scenario_spend:,.2f}")
print(f"Baseline conversion value: {baseline_value:,.2f}")
print(f"Scenario conversion value: {scenario_value:,.2f}")
print(f"Estimated change in value: {scenario_value - baseline_value:,.2f}")

print("\n--- CHANNEL-LEVEL SCENARIO ---")
print(
    df[
        [
            "channel_name",
            "spend",
            "scenario_spend",
            "conversion_value",
            "scenario_conversion_value",
            "roas",
            "scenario_change_value",
        ]
    ].round(2).to_string(index=False)
)

output_path = BASE_DIR / "budget_reallocation_scenario.csv"
df.to_csv(output_path, index=False)

print(f"\nResults saved to: {output_path}")
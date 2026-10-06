# Marketing Budget Allocation & Campaign Performance Analysis

## Business Problem

Marketing teams need to understand whether their advertising budget is being allocated effectively across channels and campaigns.

This project analyzes marketing campaign performance to identify:

- Which channels generate the strongest returns relative to spend
- Which campaigns consume significantly more budget than planned
- Where marketing spend is concentrated
- How campaign performance changes over time
- Whether a hypothetical budget reallocation could improve conversion value

The analysis combines SQL, Python, DuckDB and Power BI to transform raw campaign data into business-focused insights and a hypothetical budget allocation scenario.

---

## Project Objective

The primary objective was to evaluate marketing spend efficiency and identify opportunities for budget optimization.

The analysis focuses on four key areas:

1. **Channel Performance**
2. **Campaign Performance**
3. **Budget Utilization**
4. **Hypothetical Budget Reallocation**

---

## Key Business Questions

### Channel Performance

- Which paid channels generate the highest ROAS?
- How much spend and conversion value does each channel generate?
- Which channels appear relatively less efficient?

### Campaign Performance

- Which campaigns generate the highest conversion value?
- Which campaigns have the largest budget overruns?
- How much marketing spend is associated with campaigns with activity?

### Budget Optimization

- Where is marketing budget being overspent?
- What happens if part of the budget is hypothetically shifted from a lower-ROAS channel to a higher-ROAS channel?

---

# Dataset

The project uses a multi-table marketing campaign dataset containing campaign, channel, ad group, daily performance and conversion data.

The dataset contains:

- 9 marketing channels
- 600 campaigns
- 3,000 ad groups
- 260,000 daily performance records
- 40,000 conversion records

The main source tables are stored in the `data/` directory.

### Source Tables

| Table | Description |
|---|---|
| `channels` | Marketing channel and paid/organic classification |
| `campaigns` | Campaign-level information including budget, objective and dates |
| `ad_groups` | Campaign advertising group information |
| `daily_performance` | Daily impressions, clicks, spend and conversion metrics |
| `conversions` | Conversion-level information |

---

# Analytical Approach

## 1. Data Loading & Validation

The raw Parquet files were loaded into DuckDB and validated before analysis.

Validation checks included:

- Campaign counts
- Campaigns with activity
- Campaigns with spend
- Budget utilization
- Spend reconciliation
- Conversion reconciliation
- Conversion value reconciliation
- Zero-spend campaigns

The final analytical tables were reconciled to ensure that channel-level and campaign-level totals matched.

---

## 2. SQL Analysis

SQL was used to create reusable analytical tables at two levels:

### Channel Performance

Metrics calculated include:

- Impressions
- Clicks
- Spend
- Conversions
- Conversion Value
- CTR
- CPC
- Conversion Rate
- CPA
- ROAS

### Campaign Performance

Campaign-level analysis includes:

- Campaign budget
- Actual spend
- Conversion value
- Conversions
- ROAS
- Budget utilization
- Active days
- First and last activity dates

---

## 3. Python Analysis

Python was used for:

- Data preparation
- Analytical validation
- Campaign analysis
- Channel analysis
- Monthly performance analysis
- Budget reconciliation
- Budget reallocation scenario modelling
- Exporting datasets for Power BI

---

# Key Findings

## Overall Marketing Performance

The analysis found:

| Metric | Result |
|---|---:|
| Total Marketing Spend | **3.24M** |
| Total Conversion Value | **2.52M** |
| Total Conversions | **34,392** |
| Blended ROAS | **0.78** |
| Campaigns | **600** |
| Campaigns with Activity | **516** |
| Campaigns with Spend | **355** |
| Campaigns Over Budget | **58** |

---

## Paid Channel Performance

Among paid channels, Display generated the highest historical ROAS.

| Channel | Spend | Conversion Value | ROAS |
|---|---:|---:|---:|
| Display | 941.5K | 525.9K | **0.56** |
| Paid Search | 276.0K | 152.4K | **0.55** |
| Affiliate | 534.7K | 287.2K | **0.54** |
| Paid Social | 511.0K | 272.8K | **0.53** |
| Video | 714.6K | 378.3K | **0.53** |
| Retargeting | 262.8K | 134.7K | **0.51** |

Display had the highest historical ROAS among the paid channels analyzed, while Retargeting had the lowest.

---

## Campaign Budget Overruns

The analysis identified **58 campaigns that exceeded their allocated budgets**.

The five largest absolute budget overruns were:

| Campaign | Budget | Actual Spend | Over Budget | Utilization |
|---|---:|---:|---:|---:|
| Spring Launch UK | 81.1K | 357.5K | **+276.4K** | 440.8% |
| Summer Sale NL | 47.1K | 273.7K | **+226.6K** | 581.0% |
| Spring Launch US | 6.8K | 143.8K | **+137.0K** | 2,114.8% |
| New Year UK | 13.4K | 149.7K | **+136.3K** | 1,117.3% |
| Summer Sale UK | 25.0K | 140.2K | **+115.2K** | 560.6% |

These campaigns warrant further investigation into campaign controls, budget settings and allocation practices.

---

# Hypothetical Budget Reallocation

A scenario model was created to evaluate a hypothetical budget transfer between paid channels.

### Scenario

**10% of Retargeting spend was hypothetically reallocated to Display.**

| Scenario Metric | Result |
|---|---:|
| Donor Channel | Retargeting |
| Receiving Channel | Display |
| Budget Transferred | **26.28K** |
| Baseline Conversion Value | **1.751M** |
| Scenario Conversion Value | **1.752M** |
| Estimated Increase | **+1.21K** |

The scenario indicates a small positive change in estimated conversion value under the model assumptions.

### Important

This is a **hypothetical scenario**, not a forecast or guaranteed business outcome.

The model assumes that:

- Historical channel-level ROAS remains constant
- 10% of Retargeting spend can be transferred to Display
- Total marketing spend remains unchanged
- No diminishing returns occur
- There are no channel capacity constraints

Therefore, the scenario should be interpreted as a directional budget optimization exercise rather than a prediction of future performance.

---

# Power BI Dashboard

The final Power BI dashboard contains three pages.

## 1. Executive Performance

Provides a high-level view of:

- Total Spend
- Total Conversion Value
- Total Conversions
- Overall ROAS
- CPA
- CTR
- Channel performance
- Monthly spend and conversion value trends

![Executive Performance](dashboard/ExecutivePerformance.png)

---

## 2. Campaign Performance

Focuses on campaign-level performance and budget control.

The page includes:

- Total campaigns
- Campaigns with activity
- Campaigns with spend
- Campaign spend
- Campaigns over budget
- Top campaigns by spend vs budget
- Top campaigns by conversion value
- Top 5 campaigns by absolute budget overrun

![Campaign Performance](dashboard/CampaignPerformance.png)

---

## 3. Budget Reallocation Scenario

Shows the hypothetical budget reallocation from Retargeting to Display.

The page compares:

- Baseline conversion value
- Scenario conversion value
- Budget transferred
- Estimated change in conversion value

![Budget Reallocation Scenario](dashboard/BudgetScenario.png)

---

# Business Recommendations

Based on the analysis:

### 1. Review budget allocation across paid channels

Display had the strongest historical ROAS among the paid channels analyzed, while Retargeting had the lowest.

Budget decisions should therefore consider channel-level efficiency rather than allocating spend evenly.

### 2. Investigate major campaign overruns

The 58 campaigns exceeding budget indicate a need for stronger budget monitoring.

The largest absolute overruns should be investigated first.

### 3. Monitor campaigns with extreme budget utilization

Some campaigns spent several times their allocated budget.

These campaigns should be reviewed for:

- Budget configuration
- Campaign duration
- Automated bidding behavior
- Tracking or data quality issues
- Approval and budget-control processes

### 4. Use scenario modelling before changing budgets

The reallocation analysis demonstrates how historical performance can be used to evaluate potential budget changes before implementation.

However, future scenarios should incorporate diminishing returns, channel capacity and incremental performance when those data become available.

---

# Tools & Technologies

### Data & Database

- DuckDB
- Parquet
- SQL

### Programming

- Python
- Pandas

### Business Intelligence

- Microsoft Power BI

### Analysis

- KPI Analysis
- Campaign Performance Analysis
- ROAS Analysis
- Budget Utilization
- Scenario Modelling
- Data Validation
- Reconciliation

---

# Project Structure

```text
marketing-budget-allocation/
│
├── data/
│   ├── ad_groups.parquet
│   ├── campaigns.parquet
│   ├── channels.parquet
│   ├── conversions.parquet
│   ├── daily_performance.parquet
│   └── marketing_campaigns.schema.sql
│
├── dashboard/
│   └── Marketing_Budget_Allocation.pbix
│   ├── executive_performance.png
│   ├── campaign_performance.png
│   └── budget_reallocation.png
│
├── python/
│   ├── load_data.py
│   ├── build_analytics_tables.py
│   ├── create_monthly_performance.py
│   ├── campaign_analysis.py
│   ├── channel_analysis.py
│   ├── budget_analysis.py
│   ├── channel_budget_analysis.py
│   ├── budget_reallocation_scenario.py
│   ├── export_powerbi_data.py
│   └── validate_campaigns.py
│
└── outputs/
    ├── channel_performance.csv
    ├── campaign_performance.csv
    ├── monthly_performance.csv
    └── budget_reallocation_scenario.csv

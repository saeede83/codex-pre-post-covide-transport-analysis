from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "fta_monthly_modal_timeseries.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "output"


# Agencies and modes chosen for metro-level comparability.
TARGETS = [
    {
        "metro": "New York",
        "agency": "MTA New York City Transit",
        "mode": "HR",
        "mode_group": "Rail",
    },
    {
        "metro": "New York",
        "agency": "MTA New York City Transit",
        "mode": "MB",
        "mode_group": "Bus",
    },
    {
        "metro": "San Francisco",
        "agency": "San Francisco Bay Area Rapid Transit District",
        "mode": "HR",
        "mode_group": "Rail",
    },
    {
        "metro": "San Francisco",
        "agency": "City and County of San Francisco",
        "mode": "LR",
        "mode_group": "Rail",
    },
    {
        "metro": "San Francisco",
        "agency": "City and County of San Francisco",
        "mode": "MB",
        "mode_group": "Bus",
    },
    {
        "metro": "Chicago",
        "agency": "Chicago Transit Authority",
        "mode": "HR",
        "mode_group": "Rail",
    },
    {
        "metro": "Chicago",
        "agency": "Chicago Transit Authority",
        "mode": "MB",
        "mode_group": "Bus",
    },
]

BASELINE_START = pd.Timestamp("2014-01-01")
BASELINE_END = pd.Timestamp("2019-12-31")
COVID_START = pd.Timestamp("2020-03-01")
LATEST_DATE = pd.Timestamp("2025-12-01")


def ensure_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    usecols = ["Agency", "Mode", "Year", "Month", "Unlinked Passenger Trips"]
    df = pd.read_csv(RAW_PATH, usecols=usecols)

    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    df["month_num"] = df["Month"].map(month_map)
    df["date"] = pd.to_datetime(
        {"year": df["Year"], "month": df["month_num"], "day": 1},
        errors="coerce",
    )
    df["upt"] = pd.to_numeric(df["Unlinked Passenger Trips"], errors="coerce")
    df = df.dropna(subset=["date", "upt"])
    df = df[(df["date"] >= BASELINE_START) & (df["date"] <= LATEST_DATE)].copy()
    return df


def build_target_panel(df: pd.DataFrame) -> pd.DataFrame:
    targets = pd.DataFrame(TARGETS)
    panel = df.merge(
        targets,
        how="inner",
        left_on=["Agency", "Mode"],
        right_on=["agency", "mode"],
    )
    panel = panel[["date", "metro", "mode_group", "upt"]]
    panel = panel.groupby(["date", "metro", "mode_group"], as_index=False)["upt"].sum()
    panel["year"] = panel["date"].dt.year
    panel["month"] = panel["date"].dt.month
    return panel


def add_baseline_index(panel: pd.DataFrame) -> pd.DataFrame:
    baseline = panel[
        (panel["date"] >= BASELINE_START) & (panel["date"] <= BASELINE_END)
    ]
    month_baseline = (
        baseline.groupby(["metro", "mode_group", "month"], as_index=False)["upt"]
        .mean()
        .rename(columns={"upt": "baseline_upt"})
    )
    panel = panel.merge(month_baseline, how="left", on=["metro", "mode_group", "month"])
    panel["index_vs_2014_2019_month"] = panel["upt"] / panel["baseline_upt"] * 100
    return panel


def build_metro_totals(panel: pd.DataFrame) -> pd.DataFrame:
    metro = panel.groupby(["date", "metro"], as_index=False)["upt"].sum()
    metro["year"] = metro["date"].dt.year
    metro["month"] = metro["date"].dt.month

    base = metro[(metro["date"] >= BASELINE_START) & (metro["date"] <= BASELINE_END)]
    month_base = (
        base.groupby(["metro", "month"], as_index=False)["upt"]
        .mean()
        .rename(columns={"upt": "baseline_upt"})
    )
    metro = metro.merge(month_base, how="left", on=["metro", "month"])
    metro["index_vs_2014_2019_month"] = metro["upt"] / metro["baseline_upt"] * 100
    metro["index_3mma"] = (
        metro.sort_values("date")
        .groupby("metro")["index_vs_2014_2019_month"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )
    return metro


def recovery_milestones(metro: pd.DataFrame) -> pd.DataFrame:
    pandemic = metro[metro["date"] >= COVID_START].copy()
    rows: list[dict] = []
    for city, sub in pandemic.groupby("metro"):
        sub = sub.sort_values("date")
        trough = sub.loc[sub["index_vs_2014_2019_month"].idxmin()]

        row: dict[str, object] = {
            "metro": city,
            "trough_date": trough["date"].date().isoformat(),
            "trough_index": round(float(trough["index_vs_2014_2019_month"]), 1),
        }
        after_trough = sub[sub["date"] > trough["date"]]
        for threshold in [50, 75, 90]:
            hit = after_trough[after_trough["index_3mma"] >= threshold]
            row[f"first_{threshold}_pct_date_3mma"] = (
                hit.iloc[0]["date"].date().isoformat() if not hit.empty else None
            )
        latest = sub.iloc[-1]
        row["latest_date"] = latest["date"].date().isoformat()
        row["latest_index"] = round(float(latest["index_vs_2014_2019_month"]), 1)
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("metro")
    milestone_cols = [
        "first_50_pct_date_3mma",
        "first_75_pct_date_3mma",
        "first_90_pct_date_3mma",
    ]
    out[milestone_cols] = out[milestone_cols].fillna("Not reached")
    return out


def annual_summary(panel: pd.DataFrame, metro: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    mode_annual = (
        panel.groupby(["metro", "mode_group", "year"], as_index=False)["upt"].sum()
        .sort_values(["metro", "mode_group", "year"])
    )
    metro_annual = (
        metro.groupby(["metro", "year"], as_index=False)["upt"].sum().sort_values(
            ["metro", "year"]
        )
    )

    mode_annual["mode_share_pct"] = (
        mode_annual["upt"]
        / mode_annual.groupby(["metro", "year"])["upt"].transform("sum")
        * 100
    )
    return mode_annual, metro_annual


def period_summary(metro: pd.DataFrame) -> pd.DataFrame:
    periods = [
        ("Pre-COVID", pd.Timestamp("2014-01-01"), pd.Timestamp("2019-12-31")),
        ("Shock", pd.Timestamp("2020-03-01"), pd.Timestamp("2021-12-31")),
        ("Recovery", pd.Timestamp("2022-01-01"), pd.Timestamp("2025-12-31")),
    ]
    rows = []
    for label, start, end in periods:
        sub = metro[(metro["date"] >= start) & (metro["date"] <= end)]
        g = sub.groupby("metro", as_index=False)["index_vs_2014_2019_month"].mean()
        g["period"] = label
        rows.append(g)
    out = pd.concat(rows, ignore_index=True)
    out = out.rename(columns={"index_vs_2014_2019_month": "avg_index"})
    out["avg_index"] = out["avg_index"].round(1)
    return out[["metro", "period", "avg_index"]].sort_values(["metro", "period"])


def plot_outputs(metro: pd.DataFrame, panel: pd.DataFrame, mode_annual: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")
    palette = {"New York": "#1f77b4", "San Francisco": "#ff7f0e", "Chicago": "#2ca02c"}

    # 1) Metro index over time.
    fig, ax = plt.subplots(figsize=(11, 5))
    for city, sub in metro.groupby("metro"):
        ax.plot(sub["date"], sub["index_vs_2014_2019_month"], label=city, color=palette[city])
    ax.axhline(100, color="black", linewidth=1, linestyle="--", alpha=0.8)
    ax.axvline(pd.Timestamp("2020-03-01"), color="red", linewidth=1, linestyle=":")
    ax.set_title("Transit Ridership Index vs 2014-2019 Monthly Baseline")
    ax.set_ylabel("Index (100 = 2014-2019 month average)")
    ax.set_xlabel("Date")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "metro_ridership_index.png", dpi=180)
    plt.close(fig)

    # 2) Raw monthly trips.
    fig, ax = plt.subplots(figsize=(11, 5))
    for city, sub in metro.groupby("metro"):
        ax.plot(sub["date"], sub["upt"] / 1_000_000, label=city, color=palette[city])
    ax.axvline(pd.Timestamp("2020-03-01"), color="red", linewidth=1, linestyle=":")
    ax.set_title("Monthly Unlinked Passenger Trips")
    ax.set_ylabel("Trips (millions)")
    ax.set_xlabel("Date")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "metro_monthly_trips.png", dpi=180)
    plt.close(fig)

    # 3) Rail vs bus index facets.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for i, city in enumerate(["New York", "San Francisco", "Chicago"]):
        sub = panel[panel["metro"] == city]
        for mode, mode_sub in sub.groupby("mode_group"):
            axes[i].plot(
                mode_sub["date"],
                mode_sub["index_vs_2014_2019_month"],
                label=mode,
                linewidth=2,
            )
        axes[i].axhline(100, color="black", linewidth=1, linestyle="--", alpha=0.8)
        axes[i].axvline(pd.Timestamp("2020-03-01"), color="red", linewidth=1, linestyle=":")
        axes[i].set_title(city)
        axes[i].set_xlabel("Date")
    axes[0].set_ylabel("Index")
    axes[-1].legend(loc="lower right")
    fig.suptitle("Rail vs Bus Recovery by Metro")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "rail_bus_recovery_facets.png", dpi=180)
    plt.close(fig)

    # 4) Mode share trend post-2018.
    share = mode_annual[mode_annual["year"] >= 2018].copy()
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for i, city in enumerate(["New York", "San Francisco", "Chicago"]):
        sub = share[share["metro"] == city]
        for mode, mode_sub in sub.groupby("mode_group"):
            axes[i].plot(mode_sub["year"], mode_sub["mode_share_pct"], marker="o", label=mode)
        axes[i].set_title(city)
        axes[i].set_xlabel("Year")
        axes[i].set_xticks(sorted(sub["year"].unique()))
    axes[0].set_ylabel("Mode share of metro total (%)")
    axes[-1].legend(loc="best")
    fig.suptitle("Bus vs Rail Share Shift")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "mode_share_shift.png", dpi=180)
    plt.close(fig)


def write_report(
    metro: pd.DataFrame,
    recovery: pd.DataFrame,
    period: pd.DataFrame,
    mode_annual: pd.DataFrame,
) -> None:
    latest = (
        metro.sort_values("date")
        .groupby("metro", as_index=False)
        .tail(1)[["metro", "date", "upt", "index_vs_2014_2019_month"]]
        .copy()
    )
    latest["upt_millions"] = (latest["upt"] / 1_000_000).round(2)
    latest["index_vs_2014_2019_month"] = latest["index_vs_2014_2019_month"].round(1)

    avg_2025 = (
        metro[metro["date"].dt.year == 2025]
        .groupby("metro", as_index=False)["index_vs_2014_2019_month"]
        .mean()
        .rename(columns={"index_vs_2014_2019_month": "avg_2025_index"})
    )
    avg_2025["avg_2025_index"] = avg_2025["avg_2025_index"].round(1)

    mode_2025 = mode_annual[mode_annual["year"] == 2025][
        ["metro", "mode_group", "mode_share_pct"]
    ].copy()
    mode_2025["mode_share_pct"] = mode_2025["mode_share_pct"].round(1)

    lines = []
    lines.append("# Transit Ridership Deep Dive: NYC, San Francisco, Chicago")
    lines.append("")
    lines.append("## Scope")
    lines.append(
        "- Data: FTA NTD Monthly Modal Time Series (2014-01 to 2025-12), Unlinked Passenger Trips."
    )
    lines.append("- Metros and modes:")
    lines.append("  - New York: MTA NYCT Heavy Rail (subway) + Motor Bus")
    lines.append("  - San Francisco: BART Heavy Rail + Muni Light Rail + Muni Motor Bus")
    lines.append("  - Chicago: CTA Heavy Rail + Motor Bus")
    lines.append("- Baseline: monthly mean for the same calendar month over 2014-2019.")
    lines.append("")

    lines.append("## Recovery Milestones (3-month moving-average index)")
    lines.append(recovery.to_markdown(index=False))
    lines.append("")

    lines.append("## Average Index by Period")
    lines.append(period.to_markdown(index=False))
    lines.append("")

    lines.append("## Latest Month Snapshot")
    lines.append(latest.to_markdown(index=False))
    lines.append("")
    lines.append("## 2025 Average Index")
    lines.append(avg_2025.to_markdown(index=False))
    lines.append("")
    lines.append("## 2025 Mode Share")
    lines.append(mode_2025.sort_values(["metro", "mode_group"]).to_markdown(index=False))
    lines.append("")
    top_2025 = avg_2025.sort_values("avg_2025_index", ascending=False).iloc[0]
    bottom_2025 = avg_2025.sort_values("avg_2025_index", ascending=True).iloc[0]
    mode_2019 = mode_annual[mode_annual["year"] == 2019][
        ["metro", "mode_group", "mode_share_pct"]
    ].rename(columns={"mode_share_pct": "mode_share_2019"})
    mode_delta = mode_2025.merge(mode_2019, on=["metro", "mode_group"], how="left")
    mode_delta["delta"] = mode_delta["mode_share_pct"] - mode_delta["mode_share_2019"]
    bus_shift = mode_delta[mode_delta["mode_group"] == "Bus"].sort_values(
        "delta", ascending=False
    )

    lines.append("## High-level Findings")
    lines.append(
        f"- {top_2025['metro']} is closest to pre-COVID baseline in 2025 (average index {top_2025['avg_2025_index']})."
    )
    lines.append(
        f"- {bottom_2025['metro']} remains farthest from baseline in 2025 (average index {bottom_2025['avg_2025_index']})."
    )
    lines.append(
        "- All three metros experienced a deep April 2020 trough, but recovery pace diverged substantially by city."
    )
    lines.append(
        f"- Bus share rose the most in {bus_shift.iloc[0]['metro']} (+{bus_shift.iloc[0]['delta']:.1f} percentage points vs 2019), indicating a stronger bus rebound relative to rail."
    )
    lines.append("")
    lines.append("## Caveats")
    lines.append(
        "- Series are unlinked trips, not unique riders; transfers can inflate counts relative to people."
    )
    lines.append(
        "- Metro definitions aggregate selected operators/modes for comparability and may differ from local reporting totals."
    )

    (OUTPUT_DIR / "findings.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    raw = load_data()
    panel = build_target_panel(raw)
    panel = add_baseline_index(panel)
    metro = build_metro_totals(panel)
    recovery = recovery_milestones(metro)
    mode_annual, metro_annual = annual_summary(panel, metro)
    period = period_summary(metro)

    panel.sort_values(["metro", "mode_group", "date"]).to_csv(
        PROCESSED_DIR / "metro_mode_monthly_panel.csv", index=False
    )
    metro.sort_values(["metro", "date"]).to_csv(
        PROCESSED_DIR / "metro_total_monthly_panel.csv", index=False
    )
    recovery.to_csv(PROCESSED_DIR / "recovery_milestones.csv", index=False)
    period.to_csv(PROCESSED_DIR / "period_average_index.csv", index=False)
    mode_annual.to_csv(PROCESSED_DIR / "mode_annual_summary.csv", index=False)
    metro_annual.to_csv(PROCESSED_DIR / "metro_annual_summary.csv", index=False)

    plot_outputs(metro, panel, mode_annual)
    write_report(metro, recovery, period, mode_annual)


if __name__ == "__main__":
    main()

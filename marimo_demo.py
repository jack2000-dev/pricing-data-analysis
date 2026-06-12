import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    return mo, pd, plt


@app.cell
def _(pd):
    # Load dataset
    df = pd.read_csv("data/processed/stg_delivery_fee_movement.csv")
    return (df,)


@app.cell
def _(df):
    # Data inspection
    def first_look(df):
        print(f"Shape: {df.shape}")
        print(f"\nColumn types:\n{df.dtypes}")
        print(f"\nMissing values (%):\n{(df.isnull().mean() * 100).round(1)}")
        print(f"\nDuplicates: {df.duplicated().sum()}")
        print(f"\nFirst 5 rows:\n{df.head()}")
        print(f"\nBasic stats:\n{df.describe(include='all')}")

    first_look(df)
    return


@app.cell
def _(df, pd):
    # Clean data
    df["date"] = pd.to_datetime(df["date"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Overall Delivery Fee Trends
    """)
    return


@app.cell
def _(df, plt):
    # 1.1) Overall Daily Average Delivery Fee
    daily_avg = df.groupby("date")["DeliveryFee($)"].mean()

    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(
        daily_avg.index, daily_avg.values, marker="o", linewidth=2, color="#2563EB"
    )
    ax1.set_title("Overall Daily Average Delivery Fee", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Avg Delivery Fee ($)")
    ax1.grid(True, alpha=0.3)
    fig1.autofmt_xdate(rotation=45)
    fig1.tight_layout()
    fig1
    return


@app.cell
def _(df, plt):
    # 1.2) Daily Average Delivery Fee by City trends
    city_daily = df.groupby(["date", "City"])["DeliveryFee($)"].mean().unstack("City")

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    for city in city_daily.columns:
        ax2.plot(
            city_daily.index, city_daily[city], marker="o", linewidth=2, label=city
        )
    ax2.set_title("Daily Average Delivery Fee by City", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Avg Delivery Fee ($)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.autofmt_xdate(rotation=45)
    fig2.tight_layout()
    fig2
    return


@app.cell
def _(df, pd, plt):
    # 1.3) Distance fee trends
    _df = df.copy()
    _df["distance_band"] = pd.cut(
        _df["Distance(KM)"],
        bins=[-1, 3, 6, 10],
        labels=["Short (0-3 km)", "Medium (4-6 km)", "Long (7-9 km)"],
    )
    band_daily = (
        _df.groupby(["date", "distance_band"])["DeliveryFee($)"]
        .mean()
        .unstack("distance_band")
    )

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    for band in band_daily.columns:
        ax3.plot(
            band_daily.index, band_daily[band], marker="o", linewidth=2, label=band
        )
    ax3.set_title(
        "Daily Average Delivery Fee by Distance Band", fontsize=14, fontweight="bold"
    )
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Avg Delivery Fee ($)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    fig3.autofmt_xdate(rotation=45)
    fig3.tight_layout()
    fig3
    return


@app.cell
def _(df, plt):
    # 1.4) Weekend trends

    # Create day of week
    df["Day_Number"] = df["date"].dt.dayofweek # Order of the day
    df["Day_of_Week"] = df["date"].dt.day_name()
    df["Is_Weekend"] = df["Day_of_Week"].isin(["Saturday", "Sunday"])

    # Calc
    weekday_avg = (
        df.groupby(["Day_Number", "Day_of_Week", "City"])["DeliveryFee($)"]
        .mean()
        .unstack("City")
        .sort_index(level=0)
    )


    # Plot (Bar)
    fig4, ax4 = plt.subplots(figsize=(12, 6))

    weekday_avg.plot(kind="bar", ax=ax4)

    ax4.set_title("Average Delivery Fee by Day of Week", fontsize=14, fontweight="bold")
    ax4.set_xlabel("Day of Week")
    ax4.set_ylabel("Average Delivery Fee ($)")
    ax4.grid(axis="y", alpha=0.3)
    ax4.set_xticklabels(weekday_avg.index.get_level_values("Day_of_Week"), rotation=0)

    fig4.tight_layout()
    fig4


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analyze
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Distance fee
    """)
    return


@app.cell
def _():
    # Distance fee trends


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Standard base fee
    """)
    return


@app.cell
def _():
    # Standard base fee = minimum fee at 0

    base = (df[df["Distance(KM)"] == 0]
            .groupby(["City", "restaurant_id"])["fee"]
            .min().rename("base_fee"))
    df = df.merge(base, on=["City", "restaurant_id"])
    return (df,)


if __name__ == "__main__":
    app.run()

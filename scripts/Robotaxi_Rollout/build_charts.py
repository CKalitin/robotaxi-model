"""Builds the Robotaxi_Rollout chart set (Tesla + Waymo) from the CSVs in
datasets/Robotaxi_Rollout/. Run from repo root: python3 scripts/Robotaxi_Rollout/build_charts.py

Outputs PNGs into datasets/Robotaxi_Rollout/charts/{tesla,waymo,combined}/.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "Robotaxi_Rollout"
OUT = DATA / "charts"
TODAY = pd.Timestamp("2026-09-23")
SOURCE_NOTE = "Source: datasets/Robotaxi_Rollout/ (this repo) — official disclosures + community trackers, compiled 2026-09-23"

COLORS = {"tesla": "#CC0000", "waymo": "#4285F4"}

plt.rcParams.update({
    "figure.constrained_layout.use": False,
    "text.parse_math": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
})


def savefig(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.text(0.01, 0.012, SOURCE_NOTE, fontsize=6.5, color="0.45", ha="left", va="bottom")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")


def style_date_axis(ax):
    ax.set_xlim(right=TODAY + pd.Timedelta(days=30))
    # Granularity adapts to each chart's own span: a ~year-or-shorter Tesla chart gets
    # monthly ticks, a multi-year Waymo chart gets yearly ticks — computed from the axes'
    # actual xlim rather than a fixed rule, so it's correct per-chart automatically.
    locator = mdates.AutoDateLocator(minticks=4, maxticks=9)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))


def pad_top(ax, factor=1.18):
    """Leave headroom above the data so annotation labels/legend don't crowd the top edge."""
    ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * factor)


def annotate_events(ax, events, color, y_levels=(0.80, 0.68, 0.56, 0.44), fontsize=7, cluster_days=20):
    """events: list of (date, label). Events within `cluster_days` of each other are grouped
    onto one vertical line (so a 4-city launch day or several regulatory filings a few weeks
    apart don't each get their own dashed line), but each label is drawn as its OWN short
    rotated text, fanned out with a small horizontal step — never comma-joined into one long
    string. A joined string is exactly what ran off the bottom of the axes before: long
    combined labels have to grow far enough downward to spell themselves out, and that
    downward run eventually exceeds the axes and gets clipped by the figure edge. Fanning
    keeps every label's own vertical extent short regardless of how many events cluster."""
    ordered = sorted(((pd.Timestamp(d), lbl) for d, lbl in events), key=lambda e: e[0])
    clusters = []  # each entry: [anchor_date, last_date, labels]
    for date, label in ordered:
        if clusters and (date - clusters[-1][1]).days <= cluster_days:
            clusters[-1][2].append(label)
            clusters[-1][1] = date  # chain-cluster: compare against the latest event, not
            # the cluster's first one, so a run of events each <=cluster_days apart fully
            # merges even if the run's total span exceeds cluster_days (e.g. three launches
            # 19 and 13 days apart in turn span 32 days total but belong in one cluster).
        else:
            clusters.append([date, date, [label]])
    for i, (anchor, _last, labels) in enumerate(clusters):
        ax.axvline(anchor, color=color, alpha=0.25, lw=0.9, linestyle="--", zorder=1)
        y = y_levels[i % len(y_levels)]
        for j, label in enumerate(labels):
            ax.annotate(
                label, xy=(anchor, y), xycoords=("data", "axes fraction"),
                xytext=(4 + j * 13, 0), textcoords="offset points",
                rotation=90, fontsize=fontsize, color=color, ha="left", va="top", alpha=0.9,
            )


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_company(name):
    geo = pd.read_csv(DATA / name / "geographies.csv")
    # Anchored at the start: some "not yet launched" rows embed an unrelated "as of
    # YYYY-MM-DD" date later in the string (a status-check date, not a launch date), which
    # an unanchored regex would wrongly pick up as a real launch.
    geo["date_public_launch_parsed"] = pd.to_datetime(
        geo["date_public_launch"].str.strip().str.extract(r"^(\d{4}-\d{2}-\d{2})")[0], errors="coerce"
    )
    tracker = pd.read_csv(DATA / name / "fleet_tracker_scrape.csv")
    tracker["date_scraped"] = pd.to_datetime(tracker["date_scraped"], errors="coerce")
    ridership = pd.read_csv(DATA / name / "ridership.csv")
    ridership["date_parsed"] = pd.to_datetime(
        ridership["date"].str.strip().str.extract(r"^(\d{4}-\d{2}(?:-\d{2})?)")[0], errors="coerce"
    )
    area = pd.read_csv(DATA / "derived" / f"{name}_service_area_events.csv")
    area["date"] = pd.to_datetime(area["date"])
    fleet = pd.read_csv(DATA / "derived" / f"{name}_fleet_size_events.csv")
    fleet["date"] = pd.to_datetime(fleet["date"])
    population = pd.read_csv(DATA / name / "population_covered.csv")
    population["date"] = pd.to_datetime(population["date"], format="mixed")
    return dict(geo=geo, tracker=tracker, ridership=ridership, area=area, fleet=fleet, population=population)


tesla = load_company("tesla")
waymo = load_company("waymo")

# Short display names for chart labels only (raw geography strings in the CSVs are left as
# researched — these are purely so annotation text stays compact and readable).
SHORT_GEO_NAME = {
    "Phoenix/Chandler/Tempe/Mesa/Gilbert": "Phoenix",
    "San Francisco Bay Area (SF/Oakland/Peninsula/South Bay)": "SF Bay Area",
    "Los Angeles / West LA / Santa Monica / Culver City / South LA": "Los Angeles",
}

# ===========================================================================
# 1. Geography-entry timeline (cumulative count vs time, labeled steps)
# ===========================================================================

def geography_timeline(company, color, label):
    geo = company["geo"].dropna(subset=["date_public_launch_parsed"]).sort_values("date_public_launch_parsed")
    grouped = geo.groupby("date_public_launch_parsed")["geography"].apply(list)
    dates = list(grouped.index)
    counts = np.cumsum([len(v) for v in grouped])
    return dates, counts, grouped


def draw_geography_timeline(company_key, company, annotated):
    dates, counts, grouped = geography_timeline(company, COLORS[company_key], company_key)
    fig, ax = plt.subplots(figsize=(11, 6))
    plot_dates = [dates[0] - pd.Timedelta(days=20)] + list(dates) + [TODAY]
    plot_counts = [0] + list(counts) + [counts[-1]]
    ax.step(plot_dates, plot_counts, where="post", color=COLORS[company_key], lw=2)
    ax.scatter(dates, counts, color=COLORS[company_key], zorder=3, s=28)
    ax.set_ylabel("Cumulative geographies with public service")
    ax.set_title(f"{company_key.title()} Robotaxi — geographies entered over time")
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    pad_top(ax, factor=1.1)
    if annotated:
        events = [(date, SHORT_GEO_NAME.get(name, name)) for date, names in grouped.items() for name in names]
        annotate_events(ax, events, "0.15", fontsize=7.5)
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / company_key / f"geography_timeline{suffix}.png")


for key, comp in (("tesla", tesla), ("waymo", waymo)):
    draw_geography_timeline(key, comp, annotated=False)
    draw_geography_timeline(key, comp, annotated=True)


def draw_geography_timeline_combined():
    fig, ax = plt.subplots(figsize=(11, 6))
    for key, comp in (("tesla", tesla), ("waymo", waymo)):
        dates, counts, _ = geography_timeline(comp, COLORS[key], key)
        plot_dates = [dates[0] - pd.Timedelta(days=20)] + list(dates) + [TODAY]
        plot_counts = [0] + list(counts) + [counts[-1]]
        ax.step(plot_dates, plot_counts, where="post", color=COLORS[key], lw=2.2, label=key.title())
        ax.scatter(dates, counts, color=COLORS[key], zorder=3, s=24)
    ax.set_ylabel("Cumulative geographies with public service")
    ax.set_title("Tesla Robotaxi vs Waymo — geographies entered over time")
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left")
    savefig(fig, OUT / "combined" / "geography_timeline_comparison.png")


draw_geography_timeline_combined()

# ===========================================================================
# 2. Service area vs time (known-components sum; plain, annotated, stacked)
# ===========================================================================

def build_area_grid(area_df, exclude_geo=()):
    """Returns (grid dates, per-geography wide DataFrame ffilled from 0)."""
    df = area_df[~area_df["geography"].isin(list(exclude_geo) + ["ALL_COMPANY_STATED"])].copy()
    df = df[~df["event"].str.contains("incremental", case=False, na=False)]
    df = df.dropna(subset=["area_sq_mi"])
    if df.empty:
        return None, None
    start = df["date"].min() - pd.Timedelta(days=10)
    grid = pd.date_range(start, TODAY, freq="D")
    wide = pd.DataFrame(index=grid)
    for geo, sub in df.groupby("geography"):
        sub = sub.sort_values("date")
        s = pd.Series(sub["area_sq_mi"].values, index=sub["date"].values)
        s = s.reindex(grid, method=None)
        s = s.combine_first(pd.Series(0.0, index=[grid[0]]))
        s = s.ffill().fillna(0.0)
        wide[geo] = s
    return grid, wide


def area_events_for_annotation(area_df, exclude_geo=()):
    df = area_df[~area_df["geography"].isin(list(exclude_geo) + ["ALL_COMPANY_STATED"])].copy()
    df = df[~df["event"].str.contains("incremental", case=False, na=False)]
    df = df.dropna(subset=["area_sq_mi"])
    return [(row.date, row.geography) for row in df.itertuples()]


def draw_service_area(company_key, company, annotated, exclude_geo=()):
    grid, wide = build_area_grid(company["area"], exclude_geo=exclude_geo)
    fig, ax = plt.subplots(figsize=(11, 6))
    total = wide.sum(axis=1)
    ax.plot(grid, total, color=COLORS[company_key], lw=2.2, label="Sum of known geography service areas")

    stated = company["area"][company["area"]["geography"] == "ALL_COMPANY_STATED"].sort_values("date")
    if not stated.empty:
        s_grid = pd.date_range(stated["date"].min(), TODAY, freq="D")
        s = pd.Series(stated["area_sq_mi"].values, index=stated["date"].values).reindex(s_grid).ffill()
        ax.plot(s_grid, s, color="0.25", lw=1.8, linestyle=":", label="Company-stated total (official)")
        ax.scatter(stated["date"], stated["area_sq_mi"], color="0.25", zorder=4, s=26)

    ax.set_ylabel("Service area (sq mi)")
    ax.set_title(f"{company_key.title()} Robotaxi — total service area over time")
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    pad_top(ax)
    ax.legend(loc="upper left")
    if annotated:
        annotate_events(ax, area_events_for_annotation(company["area"], exclude_geo=exclude_geo), "0.2")
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / company_key / f"service_area_total{suffix}.png")


def draw_service_area_stacked(company_key, company, exclude_geo=()):
    grid, wide = build_area_grid(company["area"], exclude_geo=exclude_geo)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    cmap = plt.get_cmap("tab20")
    cols = list(wide.columns)
    ax.stackplot(grid, [wide[c].values for c in cols], labels=cols,
                 colors=[cmap(i / max(len(cols) - 1, 1)) for i in range(len(cols))], alpha=0.9)
    ax.set_ylabel("Service area (sq mi)")
    ax.set_title(f"{company_key.title()} Robotaxi — service area by geography (stacked)")
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", fontsize=7.5, ncol=2)
    savefig(fig, OUT / company_key / "service_area_stacked.png")


TESLA_AREA_EXCLUDE = ()  # Bay Area has no numeric area anywhere, so it's naturally absent from the sum
WAYMO_AREA_EXCLUDE = ("London",)  # testing-only, not commercial service

for key, comp, excl in (("tesla", tesla, TESLA_AREA_EXCLUDE), ("waymo", waymo, WAYMO_AREA_EXCLUDE)):
    draw_service_area(key, comp, annotated=False, exclude_geo=excl)
    draw_service_area(key, comp, annotated=True, exclude_geo=excl)
    draw_service_area_stacked(key, comp, exclude_geo=excl)


def draw_service_area_comparison():
    fig, ax = plt.subplots(figsize=(11, 6))
    for key, comp, excl in (("tesla", tesla, TESLA_AREA_EXCLUDE), ("waymo", waymo, WAYMO_AREA_EXCLUDE)):
        grid, wide = build_area_grid(comp["area"], exclude_geo=excl)
        ax.plot(grid, wide.sum(axis=1), color=COLORS[key], lw=2.2, label=f"{key.title()} (sum of known geographies)")
    ax.set_ylabel("Service area (sq mi)")
    ax.set_title("Tesla Robotaxi vs Waymo — total service area over time\n(known-component sums; Tesla Bay Area size never disclosed — Tesla total is an undercount)")
    ax.title.set_fontsize(11)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left")
    savefig(fig, OUT / "combined" / "service_area_comparison.png")


draw_service_area_comparison()

# ===========================================================================
# 3. Fleet size vs time
# ===========================================================================

def draw_tesla_fleet(annotated):
    tr = tesla["tracker"].dropna(subset=["date_scraped"]).copy()
    tr = tr[pd.to_numeric(tr["estimated_vehicle_count"], errors="coerce").notna()]
    tr["estimated_vehicle_count"] = tr["estimated_vehicle_count"].astype(float)
    summed = tr.groupby("date_scraped")["estimated_vehicle_count"].sum().sort_index()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(summed.index, summed.values, color=COLORS["tesla"], marker="o", lw=1.8,
            label="Sum of community-tracker counts (same-date geographies only)")

    official = tesla["fleet"]
    claim = official[official["geography"].str.contains("Musk claim", na=False)]
    txdmv = official[official["geography"].str.contains("TxDMV", na=False)]
    ax.scatter(claim["date"], claim["fleet_size"], color="black", marker="*", s=180, zorder=5,
               label="Musk earnings-call claim (unverified)")
    ax.plot(txdmv["date"], txdmv["fleet_size"], color="0.25", marker="s", lw=1.6, linestyle="--", zorder=4,
            label="Texas DMV regulatory registry (statewide, TX only)")

    ax.set_ylabel("Vehicles")
    ax.set_title("Tesla Robotaxi — fleet size over time\n(no official company-wide count exists; lines below are trackers/regulators, not Tesla)")
    ax.title.set_fontsize(11)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    pad_top(ax)
    ax.legend(loc="lower right", fontsize=8)
    if annotated:
        events = [(r.date, f"Musk claim: {r.fleet_size:g}") for r in claim.itertuples()]
        events += [(r.date, f"TX DMV: {r.fleet_size:g}") for r in txdmv.itertuples()]
        annotate_events(ax, events, "0.15")
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / "tesla" / f"fleet_size{suffix}.png")


def draw_waymo_fleet(annotated):
    fl = waymo["fleet"]
    official = fl[(fl["geography"] == "ALL_COMPANY") & (fl["is_official"])].sort_values("date")
    grid = pd.date_range(official["date"].min(), TODAY, freq="D")
    s = pd.Series(official["fleet_size"].values, index=official["date"].values).reindex(grid).ffill()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(grid, s, color=COLORS["waymo"], lw=2.2, label="Company-wide fleet (official disclosures)")
    ax.scatter(official["date"], official["fleet_size"], color=COLORS["waymo"], zorder=4, s=32)

    components = fl[fl["geography"] != "ALL_COMPANY"]
    ax.scatter(components["date"], components["fleet_size"], color="0.3", marker="D", s=40, zorder=4,
               label="Regional component figures (not additive to total)")

    ax.set_ylabel("Vehicles")
    ax.set_title("Waymo — fleet size over time")
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    pad_top(ax)
    ax.legend(loc="upper left", fontsize=8)
    if annotated:
        # Only label the official company-wide line + the TX DMV regulatory line by name;
        # the regional component diamonds stay on the chart (and in the legend) but unlabeled
        # in text — with 3 more of them in the same crowded 2025-2026 window, spelling each
        # one out by name was the main source of overlapping text.
        events = [(r.date, f"{r.fleet_size:g}") for r in official.itertuples()]
        txdmv = components[components["geography"].str.contains("TxDMV", na=False)]
        events += [(r.date, f"TX DMV: {r.fleet_size:g}") for r in txdmv.itertuples()]
        annotate_events(ax, events, "0.15", fontsize=7)
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / "waymo" / f"fleet_size{suffix}.png")


draw_tesla_fleet(annotated=False)
draw_tesla_fleet(annotated=True)
draw_waymo_fleet(annotated=False)
draw_waymo_fleet(annotated=True)

# ===========================================================================
# 4. Ridership vs time
# ===========================================================================

def draw_tesla_ridership(annotated):
    r = tesla["ridership"]
    miles = r[r["metric_type"] == "cumulative_paid_robotaxi_miles"].dropna(subset=["date_parsed"]).sort_values("date_parsed").copy()
    miles["value"] = miles["value"].astype(float)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(miles["date_parsed"], miles["value"], color=COLORS["tesla"], marker="o", lw=2.2)
    ax.set_ylabel("Cumulative paid Robotaxi miles")
    ax.set_title("Tesla Robotaxi — cumulative paid miles over time\n(Tesla has never disclosed a ride count — miles is the only official usage metric)")
    ax.title.set_fontsize(11)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}k"))
    if annotated:
        events = [(r_.date_parsed, f"{r_.value/1e6:.2f}M mi") for r_ in miles.itertuples()]
        annotate_events(ax, events, "0.15", y_levels=(0.5,))
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / "tesla" / f"ridership{suffix}.png")


def draw_waymo_ridership(annotated):
    r = waymo["ridership"]
    weekly = r[r["metric_type"] == "weekly_paid_trips"].dropna(subset=["date_parsed"]).sort_values("date_parsed").copy()
    weekly = weekly[weekly["is_official"] == True]  # noqa: E712
    weekly["value"] = weekly["value"].astype(float)
    grid = pd.date_range(weekly["date_parsed"].min(), TODAY, freq="D")
    s = pd.Series(weekly["value"].values, index=weekly["date_parsed"].values).reindex(grid).ffill()

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(grid, s, color=COLORS["waymo"], lw=2.2, label="Weekly paid trips (official)")
    ax.scatter(weekly["date_parsed"], weekly["value"], color=COLORS["waymo"], zorder=4, s=28)
    ax.axhline(1_000_000, color="0.4", linestyle=":", lw=1.3, label="1M/week target (end of 2026, company goal)")

    ax.set_ylabel("Weekly paid trips")
    ax.set_title("Waymo — weekly paid ridership over time (official disclosures)")
    style_date_axis(ax)
    ax.set_ylim(bottom=0, top=1_100_000)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1e3:.0f}k"))
    ax.legend(loc="upper left")
    if annotated:
        events = [(r_.date_parsed, f"{r_.value/1e3:.0f}k/wk") for r_ in weekly.itertuples()]
        annotate_events(ax, events, "0.15")
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / "waymo" / f"ridership{suffix}.png")


draw_tesla_ridership(annotated=False)
draw_tesla_ridership(annotated=True)
draw_waymo_ridership(annotated=False)
draw_waymo_ridership(annotated=True)

# ===========================================================================
# 5. Population covered vs time (plain, annotated, stacked; est. — see
#    population_covered.csv in each company folder for per-row methodology)
# ===========================================================================

def _pop_formatter(v, _):
    return f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}k"


def build_population_grid(pop_df, exclude_geo=()):
    """Same forward-fill-from-zero approach as build_area_grid, but for
    population_covered.csv, which has no 'incremental' rows and no ALL_COMPANY_STATED
    equivalent to filter out."""
    df = pop_df[~pop_df["geography"].isin(exclude_geo)].copy()
    df = df.dropna(subset=["population_covered"])
    if df.empty:
        return None, None
    start = df["date"].min() - pd.Timedelta(days=10)
    grid = pd.date_range(start, TODAY, freq="D")
    wide = pd.DataFrame(index=grid)
    for geo, sub in df.groupby("geography"):
        sub = sub.sort_values("date")
        s = pd.Series(sub["population_covered"].values, index=sub["date"].values)
        s = s.reindex(grid, method=None)
        s = s.combine_first(pd.Series(0.0, index=[grid[0]]))
        s = s.ffill().fillna(0.0)
        wide[geo] = s
    return grid, wide


def population_events_for_annotation(pop_df, exclude_geo=()):
    df = pop_df[~pop_df["geography"].isin(exclude_geo)].copy()
    df = df.dropna(subset=["population_covered"])
    df = df[df["population_covered"] > 0]  # skip the pre-launch "0, not applicable" rows
    return [(row.date, SHORT_GEO_NAME.get(row.geography, row.geography)) for row in df.itertuples()]


POPULATION_TITLE_NOTE = "est. — official figures where stated, Census-density-based estimates otherwise; see population_covered.csv"


def draw_population(company_key, company, annotated):
    grid, wide = build_population_grid(company["population"])
    fig, ax = plt.subplots(figsize=(11, 6))
    total = wide.sum(axis=1)
    ax.plot(grid, total, color=COLORS[company_key], lw=2.2, label="Sum of known geography population covered")

    ax.set_ylabel("Population covered")
    ax.set_title(f"{company_key.title()} Robotaxi — population covered over time\n({POPULATION_TITLE_NOTE})")
    ax.title.set_fontsize(10)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    pad_top(ax)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pop_formatter))
    ax.legend(loc="upper left")
    if annotated:
        annotate_events(ax, population_events_for_annotation(company["population"]), "0.2")
    suffix = "_annotated" if annotated else ""
    savefig(fig, OUT / company_key / f"population_covered{suffix}.png")


def draw_population_stacked(company_key, company):
    grid, wide = build_population_grid(company["population"])
    fig, ax = plt.subplots(figsize=(11, 6.5))
    cmap = plt.get_cmap("tab20")
    cols = list(wide.columns)
    labels = [SHORT_GEO_NAME.get(c, c) for c in cols]
    ax.stackplot(grid, [wide[c].values for c in cols], labels=labels,
                 colors=[cmap(i / max(len(cols) - 1, 1)) for i in range(len(cols))], alpha=0.9)
    ax.set_ylabel("Population covered")
    ax.set_title(f"{company_key.title()} Robotaxi — population covered by geography (stacked)\n({POPULATION_TITLE_NOTE})")
    ax.title.set_fontsize(10)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pop_formatter))
    ax.legend(loc="upper left", fontsize=7.5, ncol=2)
    savefig(fig, OUT / company_key / "population_covered_stacked.png")


for key, comp in (("tesla", tesla), ("waymo", waymo)):
    draw_population(key, comp, annotated=False)
    draw_population(key, comp, annotated=True)
    draw_population_stacked(key, comp)


def draw_population_comparison():
    fig, ax = plt.subplots(figsize=(11, 6))
    for key, comp in (("tesla", tesla), ("waymo", waymo)):
        grid, wide = build_population_grid(comp["population"])
        ax.plot(grid, wide.sum(axis=1), color=COLORS[key], lw=2.2, label=f"{key.title()} (sum of known geographies)")
    ax.set_ylabel("Population covered")
    ax.set_title(f"Tesla Robotaxi vs Waymo — population covered over time\n({POPULATION_TITLE_NOTE})")
    ax.title.set_fontsize(11)
    style_date_axis(ax)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pop_formatter))
    ax.legend(loc="upper left")
    savefig(fig, OUT / "combined" / "population_covered_comparison.png")


draw_population_comparison()

print("\nDone.")

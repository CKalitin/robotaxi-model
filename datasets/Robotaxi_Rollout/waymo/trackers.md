# Waymo tracker / watcher sites

Original entries below were verified by WebSearch and/or WebFetch on 2026-07-22; this section was
refreshed on 2026-09-23 (re-checked each existing tracker, plus one newly-discovered tracker,
fsddb.com/robotaxi — see item 0 below). URLs are real search-result URLs, not invented. Several of
these track both Waymo and Tesla — only the Waymo-relevant coverage is described here; see the
sibling `tesla/` dataset for Tesla-specific detail.

## 0. Texas Robotaxi Database (fsddb.com/robotaxi) — NEW as of this 2026-09-23 refresh
- URL: https://fsddb.com/robotaxi
- What it tracks: A live-updating frontend on the same underlying TxDMV SB2807 Automated Vehicle
  Registry that texasavtracker.com also reads, but — unlike texasavtracker.com — its numeric table
  rendered successfully via a plain WebFetch on 2026-09-23, making it the more directly usable of
  the two Texas-registry trackers for this dataset's purposes.
- Methodology: Same as texasavtracker.com (pulls from the state's mandatory AV registry), but adds
  a per-vehicle-type breakdown (e.g., Jaguar I-PACE vs. Zeekr RT) and week-over-week / 30-day
  growth deltas not seen on texasavtracker.com's static shell.
- Data as observed 2026-09-23: Waymo at 989 total Texas-registered vehicles (767 Jaguar I-PACE +
  222 Zeekr RT), "synced just now," +1 vehicle week-over-week, +298 vehicles (43%) over the prior
  30 days, and "12 outstanding complaints filed with Texas DMV." Also lists Avride (344), Zoox (44).
- Activity: Actively maintained; live sync timestamp confirms near-real-time updates from the
  state registry.
- Recommendation: for future refreshes of this dataset, try fsddb.com/robotaxi before
  texasavtracker.com when a directly-renderable numeric Texas figure is needed.

## 1. Robotaxi Tracker (robotaxitracker.com)
- URL: https://robotaxitracker.com/ (methodology: https://robotaxitracker.com/methodology ;
  fleet registry: https://robotaxitracker.com/vehicles ; also distributed as an iOS app,
  https://apps.apple.com/us/app/-/id6757382794)
- What it tracks: Tesla and Waymo robotaxi fleets across major US markets — live wait times,
  fleet-growth charts, a searchable vehicle registry (filterable by plate, color, provider,
  service area), and "unsupervised ride" percentages.
- Methodology: Independent, community-driven project built by developer Ethan McKanna. Combines
  crowdsourced "discovered vehicle" sightings (plate spotting submitted by users) with public
  regulatory data (e.g., Texas DMV AV registry) and other public disclosures. Explicitly states
  no affiliation with Tesla, Waymo, Alphabet, or their subsidiaries.
  (https://www.rideai.org/companies/robotaxi-tracker, https://grokipedia.com/page/Robotaxi_Tracker)
- Coverage: Austin, San Francisco Bay Area, Los Angeles, Phoenix, Atlanta, Dallas, Houston (per
  its provider/city filter UI as observed 2026-07-22).
- Data currency / limitations: The site's own methodology page acknowledges that "community
  discovered vehicles data for Waymo remains incomplete, with coverage varying significantly by
  service area" — i.e., Waymo counts are known to be undercounts, more so than its Tesla
  Austin-only coverage (which is easier to spot exhaustively in a single, smaller launch city).
  The live count tables are rendered client-side (JavaScript), so an automated WebFetch on
  2026-07-22 could only retrieve the static page shell/navigation, not current numeric counts —
  see `fleet_tracker_scrape.csv` for what was and wasn't observable.
- Activity: Appears actively maintained (has both a live web dashboard and a dedicated iOS app;
  covered favorably by The Driverless Digest as a useful third-party fleet-tracking project).
  Re-checked 2026-09-23: WebFetch again returned only the static page title/shell
  ("Robotaxi Tracker — Fleet Data & Service Maps"), not live counts — same limitation as before,
  unchanged since 2026-07-22.

## 2. Robotaxi Safety Tracker (robotaxi-safety-tracker.com)
- URL: https://robotaxi-safety-tracker.com/ (about: https://robotaxi-safety-tracker.com/about.html ;
  methodology: https://robotaxi-safety-tracker.com/methodology.html)
- What it tracks: **Tesla only** — explicitly states it monitors "Tesla's robotaxi safety
  performance in Austin, Texas — the only location where Tesla operates fully unsupervised
  (Level 4) autonomous vehicles." It does **not** track Waymo. Included here only to document
  that it was checked and ruled out as a Waymo source (per the task's instruction to verify
  rather than assume).
- Methodology (for completeness): Computes miles-per-incident by combining an estimated fleet
  size (Tesla's own Q3 2025 disclosure) x an assumed 115 mi/vehicle/day, divided into
  NHTSA-reported incidents; open-source on GitHub, accepts public corrections.
- Activity: Appears actively maintained (references Q3 2025 disclosures and ongoing GitHub
  contributions) but has no last-updated timestamp visible.

## 3. thechargeport.com — "Robotaxi Status" tracker
- URL: https://thechargeport.com/robotaxi-tracker
- What it tracks: A narrative/curated "status" page covering Waymo, Tesla, and Zoox
  side-by-side — operating cities, approximate fleet-size ranges, weekly ride volumes,
  cumulative-mile milestones, and vehicle platforms in use (e.g., Jaguar I-PACE, Zeekr "Ojai,"
  Hyundai IONIQ 5 for Waymo).
- Methodology: Synthesizes operator press releases, SEC/NHTSA filings, and news coverage rather
  than performing its own vehicle spotting or holding a live registry. As observed 2026-07-22 it
  explicitly flagged its own numbers as approximate ("Scale is approximate — July 2026 reports
  put the in-service fleet at roughly 3,500-4,000 vehicles") and cited the Dec 2025 NHTSA SGO
  filing (3,067 5th-gen vehicles) as its anchor data point.
- Coverage: Lists all 11 Waymo commercial metros as of July 2026 (Phoenix, SF Bay Area, LA,
  Atlanta, Austin, Dallas, Houston, San Antonio, Orlando, Miami, Nashville) but does not provide
  a per-city vehicle-count breakdown.
- Activity: Page is dated "Robotaxi Status July 2026," suggesting monthly-ish refresh cadence; a
  curated aggregator rather than an automated tracker. Re-checked 2026-09-23: page had updated its
  own dateline to "Robotaxi Status September 2026" (confirming the ~monthly cadence) and its
  Waymo figures accordingly, now stating ~4,000 vehicles (~300 of them the new 6th-gen Ojai),
  >500,000 weekly paid rides, ~4M weekly autonomous miles, 20M+ lifetime trips, and 14 active US
  metros — see `fleet_tracker_scrape.csv` for the full 2026-09-23 snapshot. It also surfaced one
  operationally useful detail not found in primary-source searches during this refresh: "freeway
  rides, paused since late May 2026, began returning on July 29, 2026 after software updates
  addressing freeway construction zones."

## 4. Texas Autonomous Fleet Tracker (Texas AV Tracker)
- URL: https://texasavtracker.com/
- What it tracks: The only tracker in this list backed by a *regulatory mandate*: it presents
  data from the Texas DMV (TxDMV) Automated Vehicle Registry, created under Texas SB 2807
  (effective 2026-05-28), which legally requires companies testing/deploying AVs in Texas to
  register their fleets and report safety information publicly. The site states it
  "auto-updates every 60 seconds" from that registry.
- Methodology: Pulls directly from a government data source rather than crowdsourcing — the
  strongest methodology of any tracker in this list, though it is still a third-party frontend
  on top of the state registry, not the registry itself.
  See also TechCrunch's coverage of the underlying registry launch:
  https://techcrunch.com/2026/05/28/waymo-dominates-texas-autonomous-vehicle-registrations-as-tesla-trails-behind/
  (reporting 577 Waymo vehicles registered statewide in Texas vs. far smaller Tesla/Avride/Nuro
  counts).
- Coverage: Texas only (statewide; does not appear to break out registration by individual
  Texas city in the portions WebFetch could render).
- Data currency / limitations: WebFetch on 2026-07-22 could only retrieve the tracker's static
  page shell (mentions of "Live counts," "Daily Texas fleet totals," a "View fleet -> Live"
  link) — the live numeric table renders client-side and was not captured directly; the 577
  figure used in `fleet_tracker_scrape.csv` comes from a news article reading the same registry,
  not a direct scrape.
- Activity: Very new (registry went live 2026-05-28 under a new state law) but appears
  authoritative and actively maintained by virtue of its statutory basis. Re-checked 2026-09-23:
  still only the static page shell was retrievable via WebFetch (live table remains client-side
  JS); see item 0 above (fsddb.com/robotaxi) for a directly-renderable frontend on the same
  underlying registry, which on 2026-09-23 showed 989 Waymo vehicles statewide, up from the 577
  figure reported via news coverage of this same registry on 2026-05-28.

## 5. AV Map (avmap.io)
- URL: https://avmap.io/
- What it tracks: Described in search results as an interactive map of autonomous-vehicle
  deployments worldwide, covering Waymo, Tesla, Zoox, Apollo Go, WeRide, Nuro, Uber, and Lyft
  robotaxi service areas / coverage zones.
- Methodology / coverage / activity: Could not be determined beyond the page title — WebFetch on
  2026-07-22 returned only the page header with no body content, and no independent
  methodology page was found via search. Listed here for completeness (a real, found URL) but
  flagged as **unverified beyond its existence and stated topic** — do not cite specific AV Map
  numbers without a follow-up fetch that actually renders content.

## 6. The Driverless Digest (Substack/newsletter — not a live tracker, but a key secondary aggregator)
- URL: https://www.thedriverlessdigest.com/ (podcast: https://podcasts.apple.com/us/podcast/the-driverless-digest-podcast/id1811181944)
- What it does: Written/hosted by Harry Campbell. Not a live vehicle tracker, but the single most
  useful secondary source found in this research for compiling Waymo's fleet-size and
  weekly-ride-count *history* over time (e.g., "Waymo Now Has 2,000 Vehicles in Their US Fleet,"
  "Waymo Hits 500,000 Weekly Rides and Over 4 Million Miles," a CPUC-data deep dive with Dr.
  Matthew Raifman on deadheading/utilization). Frequently the earliest secondary source to
  compile and contextualize official Waymo/Alphabet disclosures.
- Methodology: Journalistic — draws on official Waymo blog posts, Alphabet earnings calls, CPUC
  regulatory filings, and NHTSA data, with its own trend analysis layered on top.
- Activity: Very actively maintained (multiple posts per month observed through July 2026).

## 7. worldmetrics.org and axis-intelligence.com "Waymo Statistics" pages (secondary aggregators — use with caution)
- URLs: https://worldmetrics.org/waymo-statistics/ and https://axis-intelligence.com/waymo-statistics/
- What they do: Both are SEO-style "verified statistics" round-up pages, not trackers. Per the
  task's instruction to check whether their numbers trace to primary sources:
  - **axis-intelligence.com** was reasonably well-sourced for the core fleet/ride numbers
    (explicitly cited NHTSA SGO Dec-2025 data, Waymo's own "Safety Impact Data Hub," CPUC
    filings, and Alphabet earnings-call reporting), but its "WURI" metric was self-created with
    no external validation, and it had an internal inconsistency between a Bloomberg-sourced
    $355M annualized revenue run-rate and the site's own derived $510M calculation.
  - **worldmetrics.org** showed clearer signs of staleness/inaccuracy: it listed San Francisco's
    launch year as "2022" and Los Angeles as "2024" with an Austin service area of "43 sq mi,"
    figures that are either outdated or in tension with primary reporting found elsewhere in this
    research (e.g., SF paid-driverless permit was 2023-08; Austin's launch-time area is reported
    elsewhere as ~37 sq mi, later 90-130 sq mi). Treat any single-page pull from worldmetrics.org
    as needing independent verification before use.
- Recommendation: Neither site is cited as a primary source for any number in `geographies.csv`,
  `timeline.md`, or `ridership.csv` in this dataset; they were consulted only to cross-check
  claims already sourced elsewhere.

## Not found / explicitly ruled out
- No dedicated, purely-Waymo (non-Tesla) crowdsourced vehicle-spotting site with its own
  independent live map was found beyond Robotaxi Tracker and AV Map above.
- No official Waymo API or public live fleet-count feed exists; Waymo's own "Service areas" help
  page (https://support.google.com/waymo/answer/9059119?hl=en) shows *where* the app currently
  operates but never a vehicle count.

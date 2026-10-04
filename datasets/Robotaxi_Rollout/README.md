# Robotaxi Rollout Dataset

Tracks the public rollout of Tesla Robotaxi and Waymo across geographies: market-entry
dates, service-area expansions, official fleet sizes, ridership, and independent
(community/tracker-site) fleet-size estimates.

Status: **in progress** — populated by automated web research on 2026-07-22. Treat all
figures as a snapshot as of the `last_updated` / `date_scraped` value in each row, not
as live data. Community tracker counts (license-plate/VIN spotting sites) are
self-reported and undercounts are likely, especially in early/limited-access phases.

## Folder structure

```
Robotaxi_Rollout/
  tesla/
    geographies.csv          official market entry + expansion data, one row per geography
    fleet_tracker_scrape.csv snapshot counts pulled from community tracker sites
    trackers.md              links to license-plate/VIN tracker sites + what they cover
    timeline.md               narrative, dated timeline of official milestones
    sources.md                list of primary/official sources used (Tesla IR, blog, filings)
  waymo/
    geographies.csv
    fleet_tracker_scrape.csv
    trackers.md
    timeline.md
    sources.md
```

## `geographies.csv` schema

| column | meaning |
|---|---|
| geography | city/metro name as commonly referenced |
| state | US state (or region) |
| country | country |
| metro_area | broader metro/service-area grouping if applicable |
| date_service_announced | date company announced intent to launch here (if distinct from launch) |
| date_public_launch | date service actually became available (earliest form, e.g. safety-driver/employee-only counts separately in notes) |
| access_type_at_launch | e.g. "safety driver, invite-only", "public app, no safety driver", "waitlist" |
| current_status | as of last_updated: active / expanding / testing / paused |
| official_fleet_size | latest official (company-stated) vehicle count for this geography, if ever disclosed |
| official_fleet_size_date | date that figure was stated |
| official_fleet_size_source_url | URL |
| notes | freeform |
| last_updated | date this row was last verified |

## `fleet_tracker_scrape.csv` schema

| column | meaning |
|---|---|
| date_scraped | date this snapshot was pulled |
| geography | as above |
| tracker_name | name of the tracking site/project |
| tracker_url | URL (deep link to the geography/filter view if possible) |
| estimated_vehicle_count | count reported by the tracker at scrape time |
| method_notes | how the tracker collects data (e.g. crowdsourced plate spotting, API) |
| confidence_notes | caveats on reliability |

## Known limitations

- Neither company publishes a live, authoritative fleet-count API; official numbers come
  from earnings calls, blog posts, press interviews, and regulatory filings, and are
  sparse/irregular.
- Community trackers are the best available proxy for current fleet size but are
  crowdsourced and can lag or undercount.
- Ridership figures are almost never broken out by geography officially; where absent,
  see notes for third-party estimates and their methodology.

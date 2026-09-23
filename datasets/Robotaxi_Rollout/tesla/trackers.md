# Tesla Robotaxi tracker / watcher sites

Independent (non-Tesla) sites and apps that track Tesla's robotaxi fleet, originally found via
live web search on 2026-07-22 and **re-verified/re-searched on 2026-09-23** (dozens of fresh
WebSearch/WebFetch calls — see `sources.md`). All URLs below were located via actual search
results or direct navigation — none are guessed. See `fleet_tracker_scrape.csv` for specific
numbers pulled from these sites (or, where the site is JavaScript-rendered and WebFetch could not
execute it, numbers as cited by journalism that visited the live site on a given date).

---

## NEW as of 2026-09-23: Robotaxi Tracker (open-robotaxi.vercel.app)
- **URL:** https://open-robotaxi.vercel.app/
- **What it tracks:** Tesla Robotaxi + Cybercab deployment progress, bilingual, explicitly "Not
  affiliated with Tesla, Inc." and "Not investment advice."
- **Methodology:** Self-described as "source-linking" every claim, and explicitly separating (1)
  official Tesla announcements, (2) regulatory filings (TX vehicle registrations), (3) community
  observer reports, and (4) testing/preparation activity. Distinguishes its own modeled "active
  commercial" fleet estimate from raw TxDMV registration counts ("registered capacity ≠ daily
  active").
- **Coverage as of the 2026-08-31 page snapshot:** 7 "live" cities — 6 unsupervised (Austin,
  Dallas, Houston, Miami, Tampa, Orlando) and 1 supervised (SF Bay Area) — plus a separate
  testing/permitting list covering Phoenix, Las Vegas, Charlotte, New Orleans, and San Antonio.
  This is the source that surfaced Charlotte and New Orleans as pre-launch testing markets not
  present in Tesla's official 7-city announcement (see `geographies.csv`); San Antonio was named
  by this tracker but no independent corroborating sighting/report was found in this research
  pass, so it was not added as its own geographies.csv row.
- **Access:** Successfully fetched directly via WebFetch on 2026-09-23 (unlike most other trackers
  in this file, its content rendered without JS issues).
- **Confidence:** Newly discovered this pass; methodology description is plausible and
  well-articulated but the site's authorship/operator identity could not be independently verified
  beyond its own self-description — treat as a useful cross-check, not a primary source on its
  own.

---

## Robotaxi Tracker (robotaxitracker.com)
- **URL:** https://robotaxitracker.com/ (vehicle registry deep-links like
  `https://robotaxitracker.com/vehicles?area=austin&provider=tesla`)
- **Also has an iOS/iPadOS/visionOS app:** "Robotaxi Tracker" on the Apple App Store
  (https://apps.apple.com/us/app/robotaxi-tracker/id6757382794)
- **What it tracks:** Both Tesla Robotaxi and Waymo fleets. Per-vehicle profiles (model, color,
  first/last spotted, total trips), searchable by license plate; fleet-wide dashboards with
  active/inactive vehicle counts, unsupervised-vs-supervised splits, and live wait times per area.
- **Methodology:** Founded and built by Ethan McKanna (widely reported as a Texas A&M engineering
  student), who reverse-engineered Tesla's Robotaxi rider app APIs to poll ride availability and
  wait times across fixed points in each service area roughly every 5 minutes, combined with a
  crowdsourced community database of individually spotted/plate-identified vehicles (users submit
  sightings, trip logs, and AI-assisted vehicle-color detection). Waymo data is aggregated
  similarly from public app/API signals.
- **Coverage as of mid-2026:** Austin, TX (Tesla & Waymo); San Francisco Bay Area (Tesla & Waymo);
  Los Angeles, CA (Waymo); Phoenix, AZ (Waymo); Atlanta, GA (Waymo); recently added Zoox support
  and Las Vegas wait-time data. Dallas/Houston Tesla filters also exist
  (`?area=dallas`, `?area=houston`).
  Source: Grokipedia "Robotaxi Tracker" page; Apple App Store listing.
- **Activity/maintenance:** Very actively cited — it is the single most-referenced independent
  Tesla robotaxi data source in 2026 journalism (Electrek, CleanTechnica, TechCrunch-adjacent
  coverage all cite it repeatedly through May-July 2026). Sponsored by "Autolane" (described as an
  "air traffic control" service for AVs) per the site's own homepage text.
- **Access caveat for this research:** The site is heavily JavaScript-rendered. Direct WebFetch on
  2026-07-22 could only retrieve a cached/pre-rendered homepage summary (34 rider vehicles / 17
  unsupervised / 42 Cybercabs in Austin test fleet at fetch time) — the live filterable vehicle
  table itself would not load without JS execution. All historical numbers in
  `fleet_tracker_scrape.csv` beyond the direct 2026-07-22 fetch are sourced from news outlets that
  visited/cited the live site on a specific date.
- **Re-checked 2026-09-23:** Site is still live and still the single most-cited independent Tesla
  robotaxi source (search results continue to reference it heavily through September 2026,
  including in coverage of the September Cybercab launch/NHTSA audit). Direct WebFetch again
  returned only the bare page title with no rendered data (same JS-rendering limitation as before);
  September figures in this dataset were obtained via journalism/aggregators that cite the live
  site (Teslarati "surges Robotaxi fleet ahead of Cybercab launch event"; NextBigFuture). Also
  newly noted: robotaxitracker.com is attributed in September 2026 coverage to "Whole Mars
  Catalog" in addition to the earlier Ethan McKanna attribution — this dataset was not able to
  fully reconcile whether these are the same person/project or a rebrand/collaboration; flagged as
  an open attribution question, not resolved as of 2026-09-23.

## Austin Tesla Robotaxi Tracker (austin-robotaxi-tracker.netlify.app)
- **URL:** https://austin-robotaxi-tracker.netlify.app/
- **What it tracks:** Austin-specific Tesla Robotaxi fleet size, growth over time, and "every
  spotted car" (per its own search-result description).
- **Methodology:** Community/crowdsourced plate-spotting, in the same vein as robotaxitracker.com.
  CleanTechnica has attributed a very similar/identical tracker (referred to there as
  "teslarobotaxitracker.com") to Ethan McKanna as well, and it is unclear from public reporting
  whether austin-robotaxi-tracker.netlify.app is McKanna's original project, a fork, or a distinct
  effort by another individual — this dataset was not able to fully disambiguate site ownership
  with high confidence and flags it as **unverified**.
- **Coverage:** Austin, TX only (Tesla-specific; no Waymo data per its title).
- **Access caveat for this research:** Also JavaScript-rendered; WebFetch on 2026-07-22 returned
  only the page `<title>` ("Austin Tesla Robotaxi Tracker") with no data content, and an attempted
  API endpoint (`/api/stats`) returned HTTP 404. No live numbers could be pulled from this site
  directly in this research pass; treat any figures attributed to it elsewhere as third-hand.

## Texas Autonomous Fleet Tracker (texasavtracker.com, formerly texasavtracker.pages.dev)
- **URL (current, as of 2026-09-23):** https://texasavtracker.com/ — the site appears to have
  moved from the `texasavtracker.pages.dev` Cloudflare Pages URL used in the 2026-07-22 research
  pass to its own `texasavtracker.com` domain by September 2026; both were checked in this update
  and the `.com` domain is now the one surfacing in search results and news citations.
- **Prior URL:** https://texasavtracker.pages.dev/
- **What it tracks:** Official Texas DMV Automated Vehicle Registry data, created under Texas SB
  2807, which took effect 2026-05-28 and requires AV companies testing/deploying in Texas to
  register fleet counts with the state. The tracker lists Tesla, Waymo, Zoox, and Avride, with
  "Daily Texas fleet totals."
- **Methodology:** NOT a plate-spotting/crowdsourced tracker — it republishes/visualizes the
  state's own official registry (auto-refreshing "every 60 seconds" per its own homepage copy),
  making it the closest thing to an "official" (regulatory, not company-stated) vehicle count
  available for Texas.
- **Built by:** Attributed on-page to X user "@dallasteslaclub."
- **Coverage:** Texas only, statewide (not broken out by city — Austin/Dallas/Houston figures for
  Tesla are combined into one number).
- **Access caveat for this research:** JavaScript-rendered; direct WebFetch on 2026-07-22 returned
  only an unrendered "Loading fleet history..." placeholder. Numbers in this dataset are sourced
  from TechCrunch (2026-05-28: Tesla 42 / Waymo 577 / Avride 317 / Nuro 47, statewide) and
  Benzinga (2026-07-03: Tesla ~175 statewide), both of which cite this tracker/the underlying DMV
  data directly.
- **Re-checked 2026-09-23 (at the new texasavtracker.com URL):** Same JS-rendering limitation —
  direct WebFetch again returned only "Loading fleet history..." / "Loading verified
  boundaries..." placeholders. Site now describes its own methodology (per secondary citations) as
  polling the TxDMV Motor Carrier Credentialing System hourly. Current-quarter numbers obtained via
  NextBigFuture's September 2026 coverage: Tesla 420 (375 Model Y + 45 Cybercab) vs Waymo 988,
  both as of 2026-09-02.

## Tesla Robotaxi Safety Tracker (robotaxi-safety-tracker.com)
- **URL:** https://robotaxi-safety-tracker.com/ (expansion/city table at
  https://robotaxi-safety-tracker.com/expansion.html)
- **What it tracks:** A safety-focused metric — "Miles Per Incident" (MPI) for Tesla's Austin
  unsupervised fleet — rather than raw fleet counts, though it does surface fleet-size figures as
  an input to its model. The `expansion.html` sub-page separately maintains a city-by-city
  expansion status table (live/announced/preparing).
- **Methodology (per its own "About/Methodology" text):** Pulls daily fleet-size figures from
  robotaxitracker.com; estimates ~115 miles/vehicle/day based on a Tesla Q3 2025 earnings
  disclosure; records incidents from NHTSA's Standing General Order 2021-01 public crash-reporting
  data; fits an exponential trend line toward human-driver crash-rate benchmarks (using ~500,000
  miles between police-reported crashes for humans, 1M+ for Waymo, as reference points).
- **Coverage:** Austin, TX unsupervised operations specifically for the safety/MPI analysis; a
  broader (but less detailed) expansion table covering all announced Tesla robotaxi cities.
- **Activity/maintenance:** Offers downloadable CSV/JSON datasets and references an associated
  Substack newsletter and GitHub repo, suggesting an individual analyst/hobbyist maintainer with
  ongoing (if not necessarily daily) updates. Page content fetched 2026-07-22 was explicitly
  labeled "as of January 2026" with some fields showing placeholder ("--") values, suggesting the
  page had gone stale for at least several months by the time of this research.
- **Re-checked 2026-09-23:** Not re-fetched directly in this pass (budget was prioritized toward
  higher-yield sources); still surfaces in general searches for Tesla robotaxi tracking sites.
  Status/freshness as of September 2026 not independently re-verified — treat the January-2026
  vintage caveat above as still the operative one until a future pass re-fetches it directly.

## The Charge Port — "Robotaxi Status" tracker
- **URL:** https://thechargeport.com/robotaxi-tracker
- **What it tracks:** A cross-operator status page covering Waymo, Tesla, and Zoox — cities of
  operation, fleet-size estimates, safety-driver requirements, pricing, and capability comparisons
  (e.g., noting Tesla FSD/Robotaxi is "the only production system that drives on any road" while
  Waymo/Zoox rely on HD-mapped geofences).
- **Methodology (per the page's own text):** States that "every operator status, city list, and
  capability claim on this page is reconciled against primary sources (operator press releases,
  SEC filings, state DMV/CPUC records, and dated trade reporting) on a monthly cycle." Page stated
  a last-verification date of 2026-07-18 when fetched on 2026-07-22.
- **Coverage:** Multi-operator, national (US) — not spotting-based; it is closer to a curated news
  digest/status board than a live vehicle registry.
- **Re-checked 2026-09-23:** Still active and well-maintained — re-fetched directly via WebFetch,
  page now self-titled "Robotaxi Status September 2026" with a stated last-verified date of
  2026-09-05, consistent with its claimed monthly reconciliation cadence. Confirms Tesla active in
  7 US metros (Austin, Dallas, Houston, Miami, Orlando, Tampa, SF Bay Area) with Phoenix and Las
  Vegas both still listed as "Preparations Underway." States plainly that "Tesla does not disclose
  how many vehicles now run unsupervised," using the 420-vehicle TxDMV figure as the best available
  proxy for Texas.

## Robo Tracker (robotracker.app)
- **URL:** https://robotracker.app/
- **What it tracks:** Per its own SEO description, a general robotaxi-tracking site/app in the
  same space as robotaxitracker.com.
- **Access caveat:** Repeated WebFetch attempts on 2026-07-22 returned HTTP 403 / 429 (rate
  limited) errors; this research could not retrieve any content from the site and cannot verify
  its methodology or current data first-hand. Listed here for completeness because it surfaced
  directly in search results, but **treat as unverified**.

## Ride AI — Robotaxi Tracker company profile
- **URL:** https://www.rideai.org/companies/robotaxi-tracker
- **What it is:** A third-party directory/profile page describing the robotaxitracker.com
  project (not a distinct tracker itself). Describes it as aggregating "crowdsourced sightings,
  public data, and dynamic fleet analytics" for an audience of "media, researchers, and industry
  stakeholders."

## Grokipedia — "Robotaxi Tracker" page
- **URL:** https://grokipedia.com/page/Robotaxi_Tracker
- **What it is:** An encyclopedia-style profile of the robotaxitracker.com project (not a live
  data source). Useful as a secondary description of methodology and history but WebFetch on this
  URL returned HTTP 403 during this research; information here comes from the WebSearch result
  snippet only, not a full-page fetch.

## Not a Tesla App (notateslaapp.com)
- **URL:** https://www.notateslaapp.com/
- **What it is:** Not a fleet-spotting tracker itself, but a Tesla-focused news outlet that
  publishes frequent, detailed Robotaxi launch/expansion articles (city-by-city launch
  announcements, earnings-call recaps) and is one of the more granular sources for exact
  geofence descriptions and launch-day details used throughout this dataset (see `sources.md`).

## TeslaFSDTracker (teslafsdtracker.com)
- **URL:** https://teslafsdtracker.com/CYBRLFT
- **What it tracks:** A broader Tesla FSD/Autopilot statistics site with a dedicated "CYBRLFT"
  section that appears (based on site navigation only — WebFetch could not retrieve detailed page
  content) to track Cybercab/Robotaxi-related metrics alongside an "FSD Survey" and "Road Trip"
  section. Could not be substantively evaluated in this research pass; listed for completeness
  only, **treat as unverified/low-confidence**.

---

### Sites that did NOT pan out as distinct trackers
- **thechargeport.com** and **robotaxi-safety-tracker.com** both function partly as curated
  status/analysis pages rather than raw crowdsourced vehicle registries — included above with that
  distinction noted.
- No dedicated, named Tesla-robotaxi tracker specific to Miami, Orlando, Tampa, Phoenix, or Las
  Vegas was found as of 2026-07-22 — coverage of those markets to date (Miami launched 2026-07-03;
  Orlando/Tampa 2026-07-21) relies on one-off journalist field reports rather than a persistent
  tracker site/URL. Expect robotaxitracker.com and/or successor sites to add these areas as the
  services mature.

### Update 2026-09-23
- Miami, Orlando, and Tampa are now folded into the general multi-city trackers'
  coverage (robotaxitracker.com, open-robotaxi.vercel.app, thechargeport.com all now list all 7
  active Tesla metros as of September 2026), so the "no dedicated tracker" gap noted above for
  those three cities has effectively closed — they are simply not broken out with their own
  standalone site the way robotaxitracker.com breaks out Austin/Dallas/Houston.
  Phoenix and Las Vegas still have no dedicated tracker (unsurprising, since neither has launched).
  robotracker.app was NOT re-attempted this pass (was rate-limited/unreachable on 2026-07-22);
  status unknown.

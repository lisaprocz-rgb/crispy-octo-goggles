# PA County Desk — build files

How the tool at `/pa_county_desk.html` is rebuilt.

## Source of truth

`PA Counties Workbook for Portal Pages 3.xlsx`, front page ("PA Counties" tab) only. This is the ONLY source
for county data. The three RVPD (BM) county files are the authoritative hours for Bucks, Chester and Montgomery.

The scripts themselves live in the VoterPro folder under `county-desk-build/`.

## Rebuild, in order

    python3 extract.py          # workbook -> counties_raw.json (67 counties x 25 fields)
    python3 classify.py         # -> counties_classified.json, 10 bucket dimensions
    python3 build_issues.py     # carried-over corrections -> issues.json
    python3 parse_actuals.py    # the 3 RVPD (BM) files -> actuals.json
    python3 build_locations.py  # -> locations.json, 209 drop box / satellite locations
    python3 build_should.py     # -> issues_final.json, before/after values and categories
    python3 build.py            # -> pa_county_desk.html
    python3 verify.py           # every embedded cell vs the workbook; buckets partition 67
    python3 verify_links.py     # every URL in the tool vs link_checks.json

## Files that carry state between runs, do not delete

- `link_checks.json` — every URL that has been opened, with what was on the page. 366 entries.
  `verify_links.py` fails the build if the tool recommends a URL not recorded here as loading.
- `issues_baseline.json` — the previous workbook version's issue keys, so a new upload can show what is NEW.
- `locations_hours.xlsx` — the hours overlay. Hours typed into it are read back on the next build and win over
  what the county publishes. Matched on County + Type + Location name.

## Link rules

A URL may not appear in a recommendation until it has been opened and seen to load. Check every URL in scope,
not just the suspicious ones, and state coverage as a fraction of the whole. A link that loads is not a link
that works: the most common defect in this data is a page that opens and describes an election that has already
happened.

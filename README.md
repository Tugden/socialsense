# socialsense

A small, extensible toolkit for turning raw social media analytics exports
into readable reports.

Built around one TikTok account with roughly 530k followers and twelve months
of data, but the loader layer is deliberately separated so other platforms can
be added without touching the metrics.

## Status

Work in progress.

- [x] Load follower history from TikTok exports
- [x] Reconstruct missing year information from date labels
- [x] Load overview, content and viewer exports
- [ ] Metrics layer
- [ ] HTML report

## Why the structure looks like this

The three layers change at different speeds, so they live in different modules:

| Module | Responsibility | Knows about |
|---|---|---|
| `loaders.py` | Read export files, return clean tables | File formats, column names |
| `metrics.py` | Turn tables into numbers | Only the column names we chose |
| `report.py` | Turn numbers into a report | Nothing about files |

If TikTok renames a column, only `loaders.py` changes. If a new platform is
added, it gets a new loader and nothing else moves.

Every loader returns the same shape regardless of which platform it read, so
the metrics never need to know where a number came from.

## The date problem

TikTok exports label days as `September 10` with no year. A 365-row export
therefore spans two calendar years with nothing in the file to distinguish
them.

`dates.py` reconstructs the year by assuming rows are in chronological order
and incrementing whenever the month goes backwards, for example December to
January. The starting year is passed in as an argument rather than hardcoded
or read from the system clock, which keeps the function deterministic: the
same input always produces the same output, and it can be tested without any
real export files.

## What the loaders return

Four exports, four loaders, each returning a fixed set of columns:

| Loader | Source file | Columns |
|---|---|---|
| `load_followers` | `FollowerHistory.xlsx` | date, followers, delta |
| `load_overview` | `Overview.xlsx` | date, views, profile_views, likes, comments, shares |
| `load_viewers` | `Viewers.xlsx` | date, total_viewers, new_viewers, returning_viewers |
| `load_content` | `Content.xlsx` | title, posted, views, likes, shares, comments |

Column selection happens on the way out of every loader. If TikTok adds a
column to an export, the output of these functions does not change.

## Known data quirks

Three things in the raw exports that the loaders have to account for, and one
they deliberately do not:

**Content dates cannot be resolved.** Unlike the daily exports, `Content.xlsx`
is sorted by view count rather than chronologically, so the year-reconstruction
trick in `dates.py` does not apply. `load_content` leaves the post date as text
rather than producing a date that would be silently wrong.

**Viewer counts are not always numeric.** `Total Viewers` contains at least one
value pandas cannot parse, so `load_viewers` coerces the column and lets the bad
rows become nulls instead of failing the whole load.

**The exports do not cover identical date ranges.** The viewer export starts one
day later than the others, which matters when joining tables on date.

**Comment counts are net, not gross.** The daily comment figure goes negative on
many days, which means deletions are being subtracted from new comments. The
loaders pass this through unchanged: it is a property of the source data, not
something to silently repair.

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pandas openpyxl
```

Place TikTok exports in `data/`:

```
data/FollowerHistory.xlsx
data/Overview.xlsx
data/Content.xlsx
data/Viewers.xlsx
```

## Usage

```bash
python -m socialsense.loaders
python -m socialsense.metrics
```

## Note on data

The `data/` directory is not committed. Sample files with the same column
shape and synthetic numbers will be added under `data/sample/` so the project
can be run without access to a real account export.
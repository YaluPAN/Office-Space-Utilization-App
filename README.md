# Brightline desk usage

## Run it

**Double-click `index.html`.** It opens in any modern browser (Chrome, Edge, Safari, Firefox). You don't need a server, an install or an internet connection. The charts are plain SVG; only the monospace font comes from Google Fonts, and the page falls back to a system font when offline.

`index.html` reads its data from `data.js` in the same folder.
`data.js` (already built) holds the bookings. To refresh it from a new export:

```
python3 build_data.py path/to/bookings.csv
```

## explore_bookings.ipynb - Data Exploration

Goal: understand this dataset before building the UI, and find the things that would make a naive answer wrong

Questions covered:
1. Whether data that should be unique has duplicates, e.g. duplicate `booking_id`s
2. Basic numbers: how many desks per floor, how many teams, and how many people per team
3. Checks on `booking_date`, `booked_at`, `checked_in_at`
- How many rows have `booked_at` later than `checked_in_at`
- Whether `booking_date` and `booked_at` are both present on every row; if not, the check-in system may have a problem
- Whether `booking_date` and `checked_in_at` are ever inconsistent
- `booking_date` and `checked_in_at` only fall on Monday–Friday; there is no weekend data
4. Cross-classification into four states: booked but not checked in / checked in but not booked / booked and checked in normally / booked and checked in but with a timestamp anomaly
5. Missing check-ins (no-shows) — distribution by day of week / floor / team
6. Per-floor summary

## Definitions (also shown on screen)

| Term | Definition |
|---|---|
| **Used desk** | A booking with a check-in time. Any check-in counts. |
| **Booked but unused (no-show)** | A booking with no check-in, on a reliable check-in day. |
| **Desk usage** | Used desks ÷ (desks × reliable check-in days in the selected period). |
| **Office day** | A weekday in the selected dates that has bookings in the export. The export has weekdays only. |
| **Reliable check-in day** | An office day that isn't an outage day (below). |
| **Booking date** | Every booking counts on the day the desk was booked *for*, never on the day the booking was made. |
| **Desks** | Floor 1 = 90, Floor 2 = 110, Floor 3 = 110, Floor 4 = 90 (400 total). They're set in `CAPACITY` in `index.html`, and they match the distinct desk IDs in the file exactly. |

With a team selected, desk usage shows the share of the selected floors' desks that team filled. The denominator stays the same, so teams can be compared.


## Other things found in the data

- **Check-in before the booking was made.** 3,698 bookings (about 1 in 5) have a check-in time earlier than the time the booking was created. All of them are same-day bookings, so this looks like walk-ins: someone sits down, scans in, and the booking is logged afterwards. These **count as used**. The drill-down labels them "walk-in".
- **Every day in the file is a weekday.** There are 66 weekdays from 1 Jun to 31 Aug 2026, with no bank-holiday gaps. A weekend-only range shows an explicit "No bookings found" message.
- **Clean otherwise:** no duplicate booking IDs, no desk booked twice on the same day, no person with two bookings on the same day, every desk on the floor its ID says, and every check-in on the booked date.

## How the screen keeps its numbers consistent

The headline cards, the chart, the table under it and the heatmap are all built from the same filtered list of bookings. The chart and the table come from the same grouped rows, and a line under the table checks that the group totals add back up to the headline figures (✓). Every bar, row, cell and card opens the bookings behind it. The drawer's totals match the number you clicked.

## Where no-shows concentrate

The no-show section has two parts:

- **A team × day-of-week heatmap.** Each cell shows the no-show rate and the number of unused desk-days. Colours run from 10% to 55% and don't rescale when you filter, so a colour means the same thing in every view. Cells with fewer than 20 bookings are greyed out because they're too small to judge.
- **A "Booked vs used" bar chart** that switches between team, day and floor. Rows are sorted by unused desk-days.

Clicking any cell or bar opens those bookings with the No-shows tab selected.

## Checked against the data

The app's figures were checked against an independent Python pass over `bookings.csv`. With all filters at their defaults:

- 62 office days, 16,685 bookings, 11,701 used, 4,984 no-shows.
- 47.2% desk usage (189 of 400 desks on an average reliable day) and a 29.9% no-show rate.
- 66 office days including the outage: 17,929 bookings, an average of 272 desks booked per day.
- Top peak days: 284 checked in on Jul 21, Jul 28 and Aug 26 (a three-way tie).
- Three floors (310 desks): 26 of 66 days had more than 310 desks booked; 0 of 62 reliable days had more than 310 recorded arrivals. 37 of 66 days had at least 264 booked; 11 of 62 had at least 264 recorded arrivals.

## Left out, on purpose or for time

- **People who sat down without checking in** can't be seen in this data, so usage may be slightly understated.
- **Half-day use** isn't measured. A check-in at 8 AM and one at 11:40 AM count the same, and the export has no check-out time.
- **The three-floor section shows evidence, not a recommendation.** It compares daily demand with 310 desks (one 90-desk floor given back) and assumes anyone can sit on any floor. It ignores team neighbourhoods, meeting rooms, growth and hiring plans.
- **Monthly trends** aren't shown as a chart. Use the Jun / Jul / Aug quick picks to compare months.
- **No CSV/PDF export, saved views, dark mode or mobile layout.** These were out of scope per the brief.
- **No automated tests.** The checks were a scripted run in headless Chrome: drill-downs, a weekend-only range, an outage-only range, a reversed date range, and the floor and team filters.

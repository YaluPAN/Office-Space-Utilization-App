#!/usr/bin/env python3
"""Convert bookings.csv into data.js, which index.html loads.

    python3 build_data.py                 # reads bookings.csv, writes data.js
    python3 build_data.py other.csv       # reads a different export.

This step only reshapes the file; it makes no business decisions. Every rule
(what counts as a used desk, which days are untrustworthy, floor capacities)
lives in index.html, so the same rules apply whether the data comes from
data.js or from a CSV dropped into the page.

Employee IDs are deliberately NOT copied into data.js. The app reports by
team, never by person.
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = ["booking_id", "booking_date", "desk_id", "floor", "team", "booked_at", "checked_in_at"]


def minutes_from_midnight(ts, day):
    """Minutes between `day` 00:00 and timestamp `ts` (negative = earlier day)."""
    t = datetime.strptime(ts.strip()[:16], "%Y-%m-%d %H:%M")
    return int((t - day).total_seconds() // 60)


def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "bookings.csv")
    out = Path(__file__).with_name("data.js")

    with src.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"{src} is missing columns: {', '.join(missing)}")
        raw = list(reader)

    dates = sorted({r["booking_date"] for r in raw})
    teams = sorted({r["team"].strip() for r in raw})
    date_idx = {d: i for i, d in enumerate(dates)}
    team_idx = {t: i for i, t in enumerate(teams)}

    rows, skipped = [], 0
    for r in raw:
        try:
            day = datetime.strptime(r["booking_date"], "%Y-%m-%d")
            booked = minutes_from_midnight(r["booked_at"], day)
            checked = minutes_from_midnight(r["checked_in_at"], day) if r["checked_in_at"].strip() else None
            rows.append([
                r["booking_id"],
                date_idx[r["booking_date"]],
                int(r["floor"]),
                r["desk_id"],
                team_idx[r["team"].strip()],
                booked,
                checked,
            ])
        except (ValueError, KeyError):
            skipped += 1

    payload = {
        "source": src.name,
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "skippedRows": skipped,
        # row = [booking id, date index, floor, desk, team index,
        #        booked-at minutes from booking-day midnight,
        #        checked-in minutes from booking-day midnight or null]
        "dates": dates,
        "teams": teams,
        "rows": rows,
    }
    out.write_text("window.BOOKINGS_DATA = " + json.dumps(payload, separators=(",", ":")) + ";\n")
    print(f"Wrote {out.name}: {len(rows):,} bookings, {len(dates)} days, {len(teams)} teams"
          + (f", {skipped} unreadable rows skipped" if skipped else ""))


if __name__ == "__main__":
    main()

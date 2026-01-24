import datetime

import gpstime

# Test dates across various leap second insertion eras
test_dates = [
    "1980-01-06 00:00:00",  # GPS Epoch
    "1981-07-01 00:00:00",  # LS insertion
    "1983-03-15 12:34:56",  # Mid-era
    "1985-07-01 00:00:00",  # LS insertion
    "1988-12-10 15:20:05",  # Mid-era
    "1992-10-24 08:30:45",  # Mid-era
    "1999-01-01 00:00:00",  # LS insertion
    "2003-05-17 18:45:30",  # Mid-era
    "2006-01-01 00:00:00",  # LS insertion
    "2010-11-05 03:15:12",  # Mid-era
    "2012-07-01 00:00:00",  # LS insertion
    "2015-07-01 00:00:00",  # LS insertion
    "2017-01-01 00:00:00",  # LS insertion
    "2020-08-12 10:20:30",  # Mid-era
    "2024-01-01 00:00:00",  # Recent
    "2026-01-24 14:00:00",  # "Current"
]

print("Calendar (UTC) | GPS Week | GPS TOW")
print("-" * 50)

results = []

for date_str in test_dates:
    # gpstime.unix2gps expects a unix timestamp
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=datetime.timezone.utc
    )
    unix_ts = dt.timestamp()
    gps_seconds = gpstime.unix2gps(unix_ts)

    week = int(gps_seconds // 604800)
    tow = int(gps_seconds % 604800)

    # Store for later use in creating JS test cases
    results.append(
        {
            "y": dt.year,
            "m": dt.month - 1,  # JS Month 0-11
            "d": dt.day,
            "h": dt.hour,
            "min": dt.minute,
            "s": dt.second,
            "w": week,
            "tow": tow,
        }
    )

    print(f"{date_str} | {week} | {tow}")

# Generate JS code snippet for the testData array
with open("js_tests.txt", "w") as f:
    f.write("[\n")
    for r in results:
        f.write(
            f"  {{ y: {r['y']}, m: {r['m']}, d: {r['d']}, h: {r['h']}, min: {r['min']}, s: {r['s']}, w: {r['w']}, mow: {r['tow']} }},\n"
        )
    f.write("]\n")

print("Done. JS array written to js_tests.txt")

#!/usr/bin/env python3
import csv
from datetime import date, timedelta

def next_day(d):
    return (date.fromisoformat(d) + timedelta(days=1)).strftime('%Y%m%d')

lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Training Dashboard//EN',
    'CALSCALE:GREGORIAN',
]

with open('plan.csv', newline='') as f:
    for row in csv.DictReader(f):
        d   = row['date'].strip()
        typ = row['type'].strip()
        km  = row['km'].strip()
        hm  = row['hm'].strip()
        uid = f"{d}-{typ.lower().replace(' ', '-')}@training-plan"
        lines += [
            'BEGIN:VEVENT',
            f'DTSTART;VALUE=DATE:{d.replace("-", "")}',
            f'DTEND;VALUE=DATE:{next_day(d)}',
            f'SUMMARY:{typ} \u2013 {km} km',
            f'DESCRIPTION:{km} km / {hm} m elevation',
            f'UID:{uid}',
            'END:VEVENT',
        ]

lines.append('END:VCALENDAR')

with open('plan.ics', 'w', newline='') as f:
    f.write('\r\n'.join(lines) + '\r\n')

print(f"Generated plan.ics ({len(lines)} lines)")

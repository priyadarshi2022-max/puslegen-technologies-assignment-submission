from pipeline.reporting.daily_counter import process_day

DATES = [
    "2024-07-11",
    "2024-07-12",
    "2024-07-13",
    "2024-07-14",
    "2024-07-15",
]

for d in DATES:
    process_day(d, limit=10)

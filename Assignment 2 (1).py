
import csv
import ast
from collections import Counter

CSV_PATH = r"c:\Users\sebas\Downloads\TV_show_data (2).csv"

def extract_days_field(field_value):
    try:
        # Convert string like "['Sunday', 'Thursday']" → list
        days = ast.literal_eval(field_value)
        if isinstance(days, list):
            return [d.strip() for d in days if d.strip()]
    except Exception:
        pass
    return []

def main():
    counts = Counter()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            field = row.get("Schedule (days)", "")
            for d in extract_days_field(field):
                counts[d] += 1

    if not counts:
        print("No days found in dataset")
        return

    max_count = max(counts.values())
    most_common = sorted([d for d, c in counts.items() if c == max_count])

    if len(most_common) == 1:
        print(f"Most common day: {most_common[0]} ({max_count} shows)")
    else:
        print(f"Most common days: {', '.join(most_common)} ({max_count} shows each)")

if __name__ == "__main__":
    main()

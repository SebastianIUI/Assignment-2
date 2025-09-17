# Simple script to find the most common scheduled day in the TV show CSV
# No external modules used. Python standard features only.

CSV_PATH = r"c:\Users\sebas\Downloads\TV_show_data (2).csv"

def parse_csv_line(line):
    # Very simple CSV splitter assuming commas are only separators at top-level fields
    # This file has quoted fields with commas; implement a basic parser handling quotes
    fields = []
    cur = ''
    in_quotes = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            in_quotes = not in_quotes
            cur += c
        elif c == ',' and not in_quotes:
            fields.append(cur)
            cur = ''
        else:
            cur += c
        i += 1
    fields.append(cur)
    return fields


def extract_days_field(field_value):
    # field_value examples: "['Sunday']" or "[]" or "['Tuesday', 'Thursday']"
    s = field_value.strip()
    # Remove surrounding quotes if present
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    s = s.strip()
    if not s:
        return []
    # If it starts with [ and ends with ] parse items separated by commas
    if s.startswith('[') and s.endswith(']'):
        inner = s[1:-1].strip()
        if not inner:
            return []
        items = []
        cur = ''
        in_q = False
        i = 0
        while i < len(inner):
            ch = inner[i]
            if ch == '"' or ch == "'":
                if in_q:
                    in_q = False
                else:
                    in_q = True
            elif ch == ',' and not in_q:
                item = cur.strip()
                if item:
                    # strip surrounding quotes and spaces
                    if (item[0] == '"' and item[-1] == '"') or (item[0] == "'" and item[-1] == "'"):
                        item = item[1:-1]
                    items.append(item)
                cur = ''
            else:
                cur += ch
            i += 1
        if cur.strip():
            item = cur.strip()
            if (item and ((item[0] == '"' and item[-1] == '"') or (item[0] == "'" and item[-1] == "'"))):
                item = item[1:-1]
            if item:
                items.append(item)
        # final clean
        return [it for it in [it.strip() for it in items] if it]
    else:
        # fallback: try splitting by comma
        parts = [p.strip(" '\"") for p in s.split(',') if p.strip()]
        return parts


def main():
    try:
        f = open(CSV_PATH, 'r', encoding='utf-8')
    except Exception as e:
        print('Error opening CSV:', e)
        return

    header = f.readline()
    if not header:
        print('CSV is empty')
        f.close()
        return
    header = header.strip('\n\r')
    cols = parse_csv_line(header)
    # find index of Schedule (days)
    target = 'Schedule (days)'
    idx = None
    for i, c in enumerate(cols):
        if c.strip() == target:
            idx = i
            break
    if idx is None:
        print('Could not find column', target)
        f.close()
        return

    counts = {}
    line_no = 1
    for line in f:
        line_no += 1
        line = line.strip('\n')
        if not line:
            continue
        fields = parse_csv_line(line)
        # If line has fewer fields than header, try to continue reading until counts match
        if len(fields) < len(cols):
            # Attempt to read subsequent lines and join
            extra = ''
            while len(fields) < len(cols):
                nxt = f.readline()
                if not nxt:
                    break
                line_no += 1
                extra += '\n' + nxt
                fields = parse_csv_line(line + extra)
        if idx >= len(fields):
            # Skip malformed row
            continue
        day_field = fields[idx]
        days = extract_days_field(day_field)
        for d in days:
            d_clean = d.strip()
            if not d_clean:
                continue
            counts[d_clean] = counts.get(d_clean, 0) + 1

    f.close()

    if not counts:
        print('No days found in dataset')
        return

    # find max
    max_count = max(counts.values())
    most = [day for day, c in counts.items() if c == max_count]
    most_sorted = sorted(most)
    if len(most_sorted) == 1:
        print('Most common day:', most_sorted[0], '(', max_count, 'shows)')
    else:
        print('Most common days:', ', '.join(most_sorted), '(', max_count, 'shows each)')

if __name__ == '__main__':
    main()

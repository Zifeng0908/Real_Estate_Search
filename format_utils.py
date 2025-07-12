from datetime import datetime
from openpyxl import load_workbook
import re

# Converts a timestamp into a human-readable date string (YYYY-MM-DD).
# Handles timestamps in milliseconds by dividing by 1000 if necessary.
def format_timestamp(ts):
    if isinstance(ts, int) and ts > 1e12:
        ts = ts / 1000
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except:
        return "N/A"

# Automatically adjusts column widths in an Excel sheet based on cell content.
# Useful for improving readability when exporting structured data.
def column_adjust(excel_path):
    wb = load_workbook(excel_path)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(excel_path)
    print(f"Excel file is created")

# Tries to convert a string to an integer after stripping whitespace.
# Returns None if the input is not a clean numeric string.
# Primarily to handle the min_bed and min_bath requirements
def sanitize_input(value):
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None

# Validates a location string to match "City, ST" format (e.g., "Houston, TX").
# Returns True if the format is correct, otherwise False.
def validate_location(location):
    pattern = r'^[A-Za-z\s]+,\s?[A-Za-z]{2}$'  # e.g. "Houston, TX"
    return bool(re.match(pattern, location))

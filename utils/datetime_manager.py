from datetime import datetime


def string_to_datetime(date_string: str) -> (datetime | None):
    try:
        format = "%Y-%m-%d %H:%M:%S.%f"  # Format to match your string
        return datetime.strptime(date_string, format)
    except Exception as e:
        return None
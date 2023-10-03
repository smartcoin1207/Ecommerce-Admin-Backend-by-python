from datetime import datetime


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valid_start_end_dates(start_date, end_date):
    if start_date and end_date:
        if not validate_date(start_date) or not validate_date(end_date):
            return False

        if start_date > end_date:
            return False

    return True


def get_interval_duration_and_format(interval):
    interval_duration = None
    interval_format = None

    if interval == "daily":
        interval_duration = 1
        interval_format = "%Y-%m-%d"
    elif interval == "weekly":
        interval_duration = 7
        interval_duration = "%Y-%m-%d"
    elif interval == "monthly":
        interval_duration = 30
        interval_format = "%Y-%m"
    elif interval == "annual":
        interval_duration = 365
        interval_format = "%Y"
        return 365, "%Y"

    return interval_duration, interval_format

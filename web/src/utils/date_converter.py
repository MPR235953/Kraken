from datetime import datetime, timedelta

DATEPICKER_FORMAT = "DD-MM-YYYY"
DATE_FORMAT = "%Y-%m-%d"

def date2str(date_obj: datetime) -> str:
    return date_obj.strftime(DATE_FORMAT)

def str2date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)
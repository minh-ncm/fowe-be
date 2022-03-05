import pytz
import datetime
import tzlocal


def convert_datetime_timezone(dt, tz1, tz2):
    """
    Arguments:
        dt: datetime time
        tz1: current timezone
        tz2: target timezone
    Returns:
        dt: converted datetime
    """
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    return dt
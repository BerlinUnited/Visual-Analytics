import datetime as dt


def serialize_datetime(v: dt.datetime) -> str:
    """
    Serialize a datetime including timezone info.

    Uses the timezone info provided if present, otherwise uses the current runtime's timezone info.

    UTC datetimes end in "Z" while all other timezones are represented as offset from UTC, e.g. +05:00.
    """

    def _serialize_zoned_datetime(v: dt.datetime) -> str:
        if v.tzinfo is not None and v.tzinfo.tzname(None) == dt.timezone.utc.tzname(
            None
        ):
            # UTC is a special case where we use "Z" at the end instead of "+00:00"
            return v.isoformat().replace("+00:00", "Z")
        else:
            # Delegate to the typical +/- offset format
            return v.isoformat()

    if v.tzinfo is not None:
        return _serialize_zoned_datetime(v)
    else:
        local_tz = dt.datetime.now().astimezone().tzinfo
        localized_dt = v.replace(tzinfo=local_tz)
        return _serialize_zoned_datetime(localized_dt)

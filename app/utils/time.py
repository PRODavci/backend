import datetime as dt


def get_utc() -> dt.datetime:
    return dt.datetime.now(tz=dt.timezone.utc)


def get_utc_timestamp() -> int:
    return int(get_utc().timestamp())


def timestamp_to_utc(timestamp: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc)


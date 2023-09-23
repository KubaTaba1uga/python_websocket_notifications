from datetime import datetime
from datetime import timedelta


def convert_channel_life_time_to_expiration_date(channel_life_time: int) -> datetime:
    return datetime.now() + timedelta(seconds=channel_life_time)


def convert_expiration_date_to_channel_life_time(expiration_dt: datetime) -> int:
    return int((expiration_dt - datetime.now()).total_seconds())

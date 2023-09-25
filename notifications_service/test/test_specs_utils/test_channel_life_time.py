from datetime import datetime
from unittest.mock import patch

from shared.spec_utils.channel_life_time_utils import \
    convert_channel_life_time_to_expiration_date
from shared.spec_utils.channel_life_time_utils import \
    convert_expiration_date_to_channel_life_time


def test_convert_channel_lifetime_to_expiration_date():
    now, channel_life_time = datetime(2000, 6, 6, 0, 0, 0), 3600  # refresh for 1h

    expected = datetime(2000, 6, 6, 1, 0, 0)

    with patch(
        "shared.spec_utils.channel_life_time_utils.datetime",
    ) as mocked_datetime:
        mocked_datetime.now = lambda: now

        received = convert_channel_life_time_to_expiration_date(channel_life_time)

    assert expected == received


def test_convert_expiration_date_to_channel_lifetime_positive():
    now, expiration_date = datetime(2000, 6, 6, 0, 0, 0), datetime(
        2000, 6, 6, 1, 0, 0
    )  # refresh for 1h

    expected = 3600

    with patch(
        "shared.spec_utils.channel_life_time_utils.datetime",
    ) as mocked_datetime:
        mocked_datetime.now = lambda: now

        received = convert_expiration_date_to_channel_life_time(expiration_date)

    assert expected == received

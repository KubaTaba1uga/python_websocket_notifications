import requests


def create_notification_channel(
    service_url: str,
    user_id: str,
    test_data: dict,
):
    URL_FORMAT = service_url + "/{}/channels"

    return requests.post(URL_FORMAT.format(user_id), json=test_data)


def get_notification_channels_list(
    service_url: str,
    user_id: str,
):
    URL_FORMAT = service_url + "/{}/channels"

    return requests.get(URL_FORMAT.format(user_id))


def get_notification_channel(service_url: str, user_id: str, channel_id: int):
    URL_FORMAT = service_url + "/{}/channels/{}"

    return requests.get(URL_FORMAT.format(user_id, channel_id))

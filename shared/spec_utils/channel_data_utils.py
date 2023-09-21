from abc import ABC
from abc import abstractmethod

from shared.db_models import NotificationChannel


class ChannelData(ABC):
    @abstractmethod
    @classmethod
    def is_channel_type(cls, channel_type: str) -> bool:
        pass

    @abstractmethod
    @classmethod
    def create_data(cls, nc: NotificationChannel, user_data: dict) -> dict:
        """Data that user's sends, need to be completed by the server,
        before they can be returned. For example in WebSocket channel
        type, channelURL need to be created.
        """
        pass


class WebsocketChannelData(ChannelData):
    DEFAULT_MAX_NOTIFICATION = 7200

    @classmethod
    def is_channel_type(self, channel_type: str) -> bool:
        return "WebSockets".lower() == channel_type.lower()

    @classmethod
    def create_data(cls, nc: NotificationChannel, user_data: dict) -> dict:
        # TO-DO add full url, not only path part. Ex: http://127.0.0.1/api/v1/1/channels/5/ws
        return {
            "channelURL": cls.format_channel_url_path(nc),
            "maxNotifications": user_data.get(
                "maxNotifications", cls.DEFAULT_MAX_NOTIFICATION
            ),
        }

    @classmethod
    def format_channel_url_path(cls, nc: NotificationChannel) -> str:
        return f"/{nc.user_id}/channels/{nc.id}/ws"


def render_channel_data(nc: NotificationChannel, user_data: dict) -> dict:
    for class_ in ChannelData.__subclasses__():
        if class_.is_channel_type(nc.channel_type):
            return class_.create_data(nc, user_data)

    raise NotImplementedError()

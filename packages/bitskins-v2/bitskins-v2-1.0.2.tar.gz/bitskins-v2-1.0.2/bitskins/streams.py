import json
from typing import Callable
from threading import Thread
from websocket import WebSocketApp


class WebsocketClient:
    def __init__(self, api_key: str, ws_callback: Callable):
        """
        Initializes a new Client instance for interacting with the BitSkins WebSocket.
        Docs: https://bitskins.com/docs/api/v2

        :param api_key: Bitskins api-key
        :type api_key: str

        :param ws_callback: Websocket callback for receiving data
        :type ws_callback: function
        """

        # WebSocket
        self.WSS_URL = "wss://ws.bitskins.com"
        self.ws = WebSocketApp(
            self.WSS_URL,
            on_open=lambda ws: ws.send(json.dumps(["WS_AUTH", api_key])),
            on_message=ws_callback
        )
        self.ws_thread = Thread(target=self.ws.run_forever)
        self.ws_thread.start()

    def subscribe(self, channel: str) -> None:
        """
        Subscribes to a new WebSocket channel.

        :param channel: One of [listed, delisted_or_sold, price_changed, extra_info]
        :type channel: str
        """
        self.ws.send(json.dumps(["WS_SUB", channel]))

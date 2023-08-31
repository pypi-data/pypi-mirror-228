
import logging
from typing import Callable, List

from paho.mqtt.client import Client

from tb_vendor.utils import Singleton
from tb_vendor.mqtt.callbacks import (
    callback_on_connect,
    callback_on_disconnect,
    OnConnectCallable,
    OnDisconnectCallable,
    OnMessageCallable,
    OnPublishCallable,
)

logger = logging.getLogger(__name__)


class TbDeviceMqttHandler(Singleton):

    mqtt_clients: List[Client] = []

    def append_client(self, client: Client) -> None:
        if client in self.mqtt_clients:
            return
        self.mqtt_clients.append(client)

    def disconnect(self, client: Client):
        client.loop_stop()
        client.disconnect()

    def disconnect_all(self):
        for client in self.mqtt_clients:
            self.disconnect(client)

    def __len__(self):
        return len(self.mqtt_clients)


class TbMqttConnection:
    def __init__(self, host: str, port: int, keepalive: int = 60,
                 tb_device_mqtt_handler: TbDeviceMqttHandler = TbDeviceMqttHandler()):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.__mqtt_client = None
        self.__mqtt_handler = tb_device_mqtt_handler

    @property
    def mqtt_client(self) -> Client:
        """Returns the MQTT client instance."""
        if self.__mqtt_client is None:
            raise ValueError("Mqtt client is not configured. Use configure_client()")
        if self.__mqtt_client._username is None:
            raise ValueError("access_token is not set.")
        return self.__mqtt_client

    @property
    def access_token(self):
        """Returns the ThingsBoard access token."""
        return self.__mqtt_client._username.decode("utf-8")

    @property
    def client_id(self):
        try:
            return str(self.__mqtt_client._client_id, "utf-8")
        except AttributeError:
            return None

    def configure_client(self, *,
                         on_message: OnMessageCallable,
                         userdata: dict = None,
                         access_token: str = None,
                         client_id: str = None,
                         on_connect: OnConnectCallable = callback_on_connect,
                         on_connect_fail: Callable = None,
                         on_disconnect: OnDisconnectCallable = callback_on_disconnect,
                         on_publish: OnPublishCallable = None,
                         on_unsubscribe: Callable = None) -> None:
        """Configure the MQTT client in order to be used to connect to ThingsBoard.

        Args:
            userdata (dict): User data to be sent to ThingsBoard.
            access_token (str): ThingsBoard access token.
            on_connect (callable): Callback to be called on connection.
            on_connect_fail (callable): Callback to be called on connection failure.
            on_disconnect (callable): Callback to be called on disconnection.
            on_message (callable): Callback to be called on message.
            on_publish (callable): Callback to be called on publish.
            on_unsubscribe (callable): Callback to be called on unsubscribe.
        """
        client_params = {}
        if userdata is None:
            userdata = {}
        if client_id:
            client_params['client_id'] = client_id
        client_params['userdata'] = userdata
        self.__mqtt_client = Client(**client_params)
        self.__mqtt_client.on_connect = on_connect
        self.__mqtt_client.on_connect_fail = on_connect_fail
        self.__mqtt_client.on_disconnect = on_disconnect
        self.__mqtt_client.on_message = on_message
        self.__mqtt_client.on_publish = on_publish
        self.__mqtt_client.on_unsubscribe = on_unsubscribe
        self.add_access_token(access_token)
        self.__mqtt_handler.append_client(self.__mqtt_client)

    def add_access_token(self, access_token: str) -> None:
        """Add or change the client access token in order

        to connect to ThingsBoard MQTT Broker

        Args:
            access_token (str): ThingsBoard access token.
        """
        if access_token is None:
            return
        self.__mqtt_client.username_pw_set(username=access_token)

    def connect_blocking(self) -> None:
        self.mqtt_client.connect(host=self.host, port=self.port, keepalive=self.keepalive)
        try:
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            logger.debug(f'Disconnect client: {self.client_id}')
            self.__mqtt_handler.disconnect(self.mqtt_client)

    def __str__(self):
        return str(self.client_id)

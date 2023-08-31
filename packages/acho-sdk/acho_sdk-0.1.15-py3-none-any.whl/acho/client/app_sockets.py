import asyncio
from .socket_client import SocketClient

class AppSocket(SocketClient):

    def __init__(self, token: str, app_version_id: str, base_url = SocketClient.BASE_URL, socket_namespaces = SocketClient.BASE_SOCKET_NAMESPACES, sio = SocketClient.sio, timeout = SocketClient.timeout):
        super().__init__(token=token, base_url=base_url, socket_namespaces=socket_namespaces, sio=sio, timeout=timeout)
        self.app_version_id = app_version_id
        return

    def init(self, app_version_id: str):
        self.app_version_id = app_version_id
        return
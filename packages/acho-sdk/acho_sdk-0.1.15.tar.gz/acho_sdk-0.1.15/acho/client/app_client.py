import asyncio
import os
from typing import Optional

import socketio
from .http_client import HttpClient
from .socket_client import SocketClient

ACHO_TOKEN = os.environ.get("ACHO_PYTHON_SDK_TOKEN") or ""
BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
BASE_SOCKET_NAMESPACES = ['/soc']
DEFAULT_SOCKET_NAMESPACE = '/soc'
ACHO_CLIENT_TIMEOUT = 30
APP_ENDPOINTS = 'apps'

class App():
    
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, id: str, token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = id
        return

    def versions(self):
        response, text = asyncio.run(self.http.call_api(path=f"{APP_ENDPOINTS}/{self.id}/versions", http_method="GET"))
        return (response, text)
    
    def version(self, app_version_id: str):
        return AppVersion(app_id=self.app_id, app_version_id=app_version_id, token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
    
    def push_event(self, event: dict):
        print('Please specify version before publishing events')
        return
    
class AppVersion():
    
    sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, app_id: str, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = sio, timeout = ACHO_CLIENT_TIMEOUT):
        self.socket_url = f'{base_url}{DEFAULT_SOCKET_NAMESPACE}'
        self.socket = SocketClient(token=token, base_url=self.socket_url, socket_namespaces=socket_namespaces, sio=sio, timeout=timeout)
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = app_id
        self.app_version_id = app_version_id
        return
    
    async def connect(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        try:
            self.socket.default_handlers()
            result = await self.socket.conn(namespaces=namespaces)
            return result
        except Exception as e:
            print(e)

    async def join(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        print({'app_version_id': self.app_version_id, 'is_editing': True})
        result = await self.socket.sio.emit('join_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
        return result

    async def leave(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        result = await self.socket.sio.emit('leave_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
        return result
    
    async def nb_nodes(self):
        response, text = await self.http.call_api(path=f"/apps/{self.app_id}/versions/{self.app_version_id}/nb-nodes", http_method="GET")
        return (response, text)
    
    async def send_webhook(self, event: dict):
        event.update({'scope': self.app_version_id})
        event.update({'type': 'notebook_event'})
        event.update({'notebook_name': self.socket.notebook_name})
        event.update({'nodeId': self.socket.node_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        return await self.http.call_api(path="neurons/webhook", http_method="POST", json=payload)
    
    async def push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        result = await self.socket.sio.emit('push', event, namespace=DEFAULT_SOCKET_NAMESPACE)
        return result
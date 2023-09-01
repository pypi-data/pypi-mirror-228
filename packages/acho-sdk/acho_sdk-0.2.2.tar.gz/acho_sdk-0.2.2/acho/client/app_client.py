import asyncio
import logging
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

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class App():
    
    # sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, id: str, token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = id
        return

    async def versions(self):
        versions = await self.http.call_api(path=f"{APP_ENDPOINTS}/{self.app_id}/versions", http_method="GET")
        return versions
    
    def version(self, app_version_id: str):
        return AppVersion(app_id=self.app_id, app_version_id=app_version_id, token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
    
    async def version_published(self):
        versions = await self.versions()
        for version in versions:
            if version['status'] in ['published']:
                return AppVersion(app_id=self.app_id, app_version_id=version['id'], token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
        raise('No published version found for app: ', self.app_id)
            
    def push_event(self, event: dict):
        logging.warning('Please specify version before publishing events')
        return
    
class AppVersion():

    def __init__(self, app_id: str, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = socketio.AsyncClient(logger=True, engineio_logger=True), timeout = ACHO_CLIENT_TIMEOUT):
        self.socket_url = f'{base_url}{DEFAULT_SOCKET_NAMESPACE}'
        self.socket = SocketClient(token=token, base_url=self.socket_url, socket_namespaces=socket_namespaces, sio=sio, timeout=timeout)
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = app_id
        self.app_version_id = app_version_id
        return
    
    async def connect(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        try:
            await self.http.identify()
            self.socket.default_handlers()
            result = await self.socket.conn(namespaces=namespaces)
            return result
        except Exception as e:
            raise Exception(e)

    async def join(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        logging.debug({'app_version_id': self.app_version_id, 'is_editing': True})
        result = await self.socket.sio.emit('join_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
        return result

    async def leave(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        result = await self.socket.sio.emit('leave_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
        return result
    
    async def nb_nodes(self):
        nodes = await self.http.call_api(path=f"/apps/{self.app_id}/versions/{self.app_version_id}/nb-nodes", http_method="GET")
        return nodes
    
    async def nb_claim(self):
        nodes = await self.nb_nodes()
        for node in nodes:
            if node['endpointUrl'] == self.socket.notebook_name:
                self.socket.node_id = node['id']
                break
        if self.socket.node_id is None:
            logging.warning('Current nodebook is not claimed by any node')
            return
        else:
            logging.info(f'Current nodebook is claimed by node: {self.socket.node_id}')
            await self.socket.notebook_detect({'app_version_id': self.app_version_id})
            return
    
    async def send_webhook(self, event: dict):
        event.update({'scope': self.app_version_id})
        event.update({'type': 'notebook_event'})
        event.update({'notebook_name': self.socket.notebook_name})
        event.update({'nodeId': self.socket.node_id})
        payload = {
            'scope': self.app_version_id,
            'event': event
        }
        logging.debug('sending webhook')
        logging.debug(payload)
        return await self.http.call_api(path="neurons/webhook", http_method="POST", json=payload)
    
    async def push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        result = await self.socket.sio.emit('push', event, namespace=DEFAULT_SOCKET_NAMESPACE)
        return result
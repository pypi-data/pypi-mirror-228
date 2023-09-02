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

logging.basicConfig(format='%(levelname)s: %(name)s | %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

class App():
    
    # sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, id: str, token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = id
        return

    async def versions(self):
        versions = await self.http.call_api(path=f"{APP_ENDPOINTS}/{self.app_id}/versions", http_method="GET")
        return versions
    
    async def details(self):
        details = await self.http.call_api(path=f"{APP_ENDPOINTS}/{self.app_id}", http_method="GET")
        return details
    
    def version(self, app_version_id: str):
        return AppVersion(app_id=self.app_id, app_version_id=app_version_id, token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
    
    async def version_editing(self):
        appDetails = await self.details()
        userDefaults = appDetails['userDefaults']
        app_version_id = userDefaults['version_id']
        return AppVersion(app_id=self.app_id, app_version_id=app_version_id, token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
    
    async def version_published(self):
        versions = await self.versions()
        for version in versions:
            if version['status'] in ['published']:
                return AppVersion(app_id=self.app_id, app_version_id=version['id'], token=self.http.token, base_url=self.http.base_url, timeout=self.http.timeout)
        raise('No published version found for app: ', self.app_id)
            
    def push_event(self, event: dict):
        logger.warning('Please specify version before publishing events')
        return
    
class AppVersion():

    # sio = socketio.AsyncClient(logger=True, engineio_logger=True)

    def __init__(self, app_id: str, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, timeout = ACHO_CLIENT_TIMEOUT):
        self.socket_url = f'{base_url}{DEFAULT_SOCKET_NAMESPACE}'
        self.socket = SocketClient(app_version_id=app_version_id, token=token, base_url=self.socket_url, socket_namespaces=socket_namespaces, timeout=timeout)
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.app_id = app_id
        self.app_version_id = app_version_id
        self.connected = False
        self.joined = False
        return
    
    def version_default_handlers(self):
        self.socket.sio.on('connect', namespace=DEFAULT_SOCKET_NAMESPACE, handler=self.reconnect_attempt)
    
    async def connect(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        try:
            await self.http.identify()
            self.socket.default_handlers()
            result = await self.socket.conn(namespaces=namespaces)
            self.connected = True
            self.version_default_handlers()
            await self.join()
            await self.nb_claim()
            return result
        except Exception as e:
            self.connected = False
            raise Exception(e)
        
    async def reconnect_attempt(self):
        logger.info('reconnecting')
        try:
            # if (self.connected):
            #     await self.connect()
            if (self.joined):
                await self.join()
                await self.nb_claim()
            return
        except Exception as e:
            raise Exception(e)

    async def join(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        try:
            logger.debug({'app_version_id': self.app_version_id, 'is_editing': True})
            result = await self.socket.sio.emit('join_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
            self.joined = True
            return result
        except Exception as e:
            self.joined = False
            raise Exception(e)

    async def leave(self, namespaces: Optional[list] = DEFAULT_SOCKET_NAMESPACE):
        try:
            result = await self.socket.sio.emit('leave_app_builder_room', {'app_version_id': self.app_version_id}, namespace=namespaces)
            self.joined = False
            return result
        except Exception as e:
            self.joined = False
            raise Exception(e)
    
    async def nb_nodes(self):
        nodes = await self.http.call_api(path=f"/apps/{self.app_id}/versions/{self.app_version_id}/nb-nodes", http_method="GET")
        return nodes
    
    async def nb_claim(self):
        if (not self.connected):
            logger.warning('Please connect to socket first')
        if (not self.joined):
            logger.warning('Please join app builder room first')
        nodes = await self.nb_nodes()
        for node in nodes:
            if node['endpointUrl'] == self.socket.notebook_name:
                self.socket.node_id = node['id']
                break
        if self.socket.node_id is None:
            logger.warning('Current nodebook is not claimed by any node')
            return
        else:
            logger.info(f'Current nodebook is claimed by node: {self.socket.node_id}')
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
        logger.debug('sending webhook')
        logger.debug(payload)
        return await self.http.call_api(path="neurons/webhook", http_method="POST", json=payload)
    
    async def push_event(self, event: dict):
        event.update({'scope': self.app_version_id})
        result = await self.socket.sio.emit('push', event, namespace=DEFAULT_SOCKET_NAMESPACE)
        return result
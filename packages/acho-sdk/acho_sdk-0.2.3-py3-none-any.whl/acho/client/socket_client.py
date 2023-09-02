import logging
import os
from typing import Optional
import socketio
import ipynbname

logger = logging.getLogger(__name__)

class SocketClient:
    BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
    BASE_SOCKET_NAMESPACES = ['/soc']
    sio = socketio.AsyncClient(logger=False, engineio_logger=False)

    def __init__(self, app_version_id: str, token: Optional[str] = None, base_url = BASE_URL, socket_namespaces = BASE_SOCKET_NAMESPACES, sio = sio, timeout = 30, notebook_name = 'unknown_notebook'):
        self.token = None if token is None else token.strip()
        """A JWT Token"""
        self.base_url = base_url
        self.socket_namespaces = socket_namespaces
        self.default_namespace = '/soc'
        """A string representing the Acho API base URL.
        Default is `'https://kube.acho.io'`."""
        self.timeout = timeout
        """The maximum number of seconds client staying alive"""
        self.default_params = {}
        self.sio = sio
        self.notebook_name = notebook_name
        self.node_id = None
        self.app_version_id = app_version_id
        self.get_notebook_attr()

    async def conn(self, namespaces: Optional[list] = None):
        logger.debug(f"Connecting to namespace {namespaces or self.socket_namespaces}")
        try:
            authenticated_url = f'{self.base_url}?token=jwt {self.token}'
            logger.debug(f'authenticated_url: {authenticated_url}')
            logger.debug(f'status: {self.sio.connected}')
            if (self.sio.connected):
                logger.debug('already connected')
                return
            else:
                result = await self.sio.connect(url=authenticated_url, namespaces=namespaces or self.socket_namespaces)
                return result
        except Exception as e:
            logger.error(f"Socket connection failed with error {e}")
            raise Exception(f"Socket connection failed with error {e}")

    def get_notebook_attr(self):
        try:
            ip = get_ipython()
            hm = ip.history_manager
            ipsession = hm.get_session_info()
            dt = ipsession[1]
            dt_string = dt.strftime("%s")
            ipname = ipynbname.name()
            ipsession = hm.get_session_info()
            self.notebook_name = ipname
            self.started_at = dt_string
            return
        except Exception as e:
            logger.error('Please run this command in a notebook')

    def default_handlers(self):
        self.sio.on('notebook_detect', namespace=self.default_namespace, handler=self.notebook_detect)
        self.sio.on('notebook_claim', namespace=self.default_namespace, handler=self.notebook_claim)

    def hook(self, event: str, callback):
        self.sio.on(event, namespace=self.default_namespace, handler=callback)

    # async def event_parser(self, callback):
    #     return lambda data: (await callback(data) for _ in '_').__anext__()
        
    async def notebook_detect(self, data):
        logger.debug('notebook detection request')
        print('notebook detection request')
        app_version_id = data['app_version_id']
        detect_result = await self.sio.emit('notebook_ready', data={'app_version_id': app_version_id, 'nodeId': self.node_id, 'notebook_name': self.notebook_name}, namespace=self.default_namespace)

    async def notebook_claim(self, data):
        logger.debug('notebook claim request')
        print('notebook claim request')
        app_version_id = data['app_version_id']
        notebook_name = data['notebook_name']
        node_id = data['nodeId']
        if (notebook_name == self.notebook_name):
            self.node_id = node_id
            if (node_id):
                detect_result = await self.sio.emit('notebook_claimed', data={'app_version_id': app_version_id, 'nodeId': node_id, 'notebook_name': self.notebook_name}, namespace=self.default_namespace)
            else:
                await self.sio.emit('notebook_claim_failed', data={'app_version_id': app_version_id, 'nodeId': node_id, 'notebook_name': self.notebook_name}, namespace=self.default_namespace)
                logger.warn('node_id is missing')

    def tag(self):
        return f'[{self.app_version_id[-4:]}][{self.node_id[-4:]}]'

    @sio.on('connect', namespace='/soc')
    def on_connect():
        # logger.debug("I'm connected to the /soc namespace!")
        print("I'm connected to the /soc namespace!")
        return
    
    @sio.event
    async def connect():
        logger.info('connected to server')
        return
    
    @sio.event
    async def connect_error(data):
        print("The connection failed!")

    @sio.event
    async def disconnect():
        logger.info('disconnected from server')
        return

    @sio.on('*', namespace='/soc')
    async def catch_all(event, data):
        logger.info(f'incoming event: {event}')
        return

    
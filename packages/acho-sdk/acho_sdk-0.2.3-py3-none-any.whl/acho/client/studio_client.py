import asyncio
import logging
import os
from typing import Optional

from .http_client import HttpClient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ACHO_TOKEN = os.environ.get("ACHO_PYTHON_SDK_TOKEN") or ""
BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
ACHO_CLIENT_TIMEOUT = 30

class Acho():

    def __init__(self):
        return

class AssetManager():

    def __init__(self, path = '', token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.path = path
        return

    def redirect(self, path):
        self.path = path

    async def list(self, options = {}):
        payload = {
            'path': self.path,
            'depth': options.get('depth', 1),
            'options': options,
        }
        result = await self.http.call_api(path=f"/uploaded/search", http_method="POST", json=payload)
        return result

    async def upload(self, options = {}):
        params = {
            'destination': self.path,
            'public': options.get('public', 'true'),
        }
        # TODO: Add files to multipart/form-data
        result = await self.http.call_api(path=f"/uploaded/file/upload", http_method="POST", params=params)
        return result
    
    async def download(self, filename, options = {}):
        payload = {
            'file': { 'path': self.path + filename },
            'options': options,
        }
        # TODO: Save file stream to storage / memory
        # result = await self.http.call_api(path=f"/uploaded/download", http_method="POST", json=payload)
        # return result

    async def get_url(self, filename, options = {}):
        payload = {
            'file': { 'path': self.path + filename },
            'options': options,
        }
        result = await self.http.call_api(path=f"/uploaded/file/get-link", http_method="POST", json=payload)
        return result


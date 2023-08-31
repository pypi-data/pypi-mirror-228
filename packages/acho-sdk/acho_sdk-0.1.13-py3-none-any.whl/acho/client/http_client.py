import os
import asyncio
import requests
import socketio

from typing import Optional, Union, Dict, Any, List

from .client_utils import _build_req_args, _get_url

class HttpClient:
    BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""

    def __init__(self, token: Optional[str] = None, base_url = BASE_URL, timeout = 30):
        self.token = None if token is None else token.strip()
        """A JWT Token"""
        self.base_url = base_url
        """A string representing the Acho API base URL.
        Default is `'https://kube.acho.io'`."""
        self.timeout = timeout
        """The maximum number of seconds client staying alive"""
        self.default_params = {}

    async def call_api(self, path, http_method: str = "POST", params: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
        auth: Optional[dict] = None) -> Any:

        api_url = _get_url(self.base_url, path)

        if auth is not None:
            if isinstance(auth, dict):
                if headers is None:
                    headers = {}
                headers["Authorization"] = '{} {}'.format(auth.token_type, auth.token)
        else:
            headers = {}
            headers["Authorization"] = 'jwt {}'.format(self.token)

        headers = headers or {}
        
        req_args = _build_req_args(
            token=self.token,
            http_method=http_method,
            default_params=self.default_params,
            params=params,
            json=json,
            headers=headers,
            auth=auth,
        )

        return await self._send(
            http_method=http_method,
            api_url=api_url,
            req_args=req_args,
        )

    async def _send(self, http_method: str, api_url: str, req_args: dict) -> Any:
        """Sends the request out for transmission.
        Args:
            http_verb (str): The HTTP verb. e.g. 'GET' or 'POST'.
            api_url (str): The Acho API url'
            req_args (dict): The request arguments to be attached to the request.
            e.g.
            {
                json: {
                    'attachments': [{"pretext": "pre-hello", "text": "text-world"}],
                    'channel': '#random'
                }
            }
        """

        res = {}
        
        print(req_args)

        if (http_method == "GET"):
            res = requests.get(url=api_url)
        elif (http_method == "POST"):
            res = requests.post(url=api_url, json=req_args.get('json'))
        data = {
            "client": self,
            "http_method": http_method,
            "api_url": api_url,
            "req_args": req_args,
        }
        return (res, data)
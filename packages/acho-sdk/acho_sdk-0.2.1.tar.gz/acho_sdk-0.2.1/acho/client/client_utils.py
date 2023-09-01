
import platform
import sys
from typing import Any, Optional, Union, Dict
from urllib.parse import urljoin
from acho import version

def _get_url(base_url: str, path: str) -> str:
    """Join the base_url with path
    """
    return urljoin(base_url, path)

def _build_req_args(
    *,
    token: Optional[str],
    http_method: str,
    default_params: dict,
    params: dict,
    json: dict,  # skipcq: PYL-W0621
    headers: dict,
    auth: dict,
) -> dict:
    has_json = json is not None
    if has_json and http_method != "POST":
        msg = "Json data can only be submitted as POST requests. GET requests should use the 'params' argument."
        raise TypeError(msg)

    if params is not None and isinstance(params, dict):
        params = {k: v for k, v in params.items() if v is not None}
        _set_default_params(params, default_params)
    if json is not None and isinstance(json, dict):
        _set_default_params(json, default_params)

    token: Optional[str] = token
    if params is not None and "token" in params:
        token = params.pop("token")
    if json is not None and "token" in json:
        token = json.pop("token")
    req_args = {
        "headers": _get_headers(
            headers=headers,
            token=token,
            has_json=has_json,
            request_specific_headers=headers,
        ),
        "params": params,
        "json": json,
        "auth": auth,
    }
    return req_args


def _set_default_params(target: dict, default_params: dict) -> None:
    for name, value in default_params.items():
        if name not in target:
            target[name] = value

def _get_headers(
    *,
    headers: dict,
    token: Optional[str],
    has_json: bool,
    request_specific_headers: Optional[dict],
) -> Dict[str, str]:
    """Constructs the headers need for a request.
    Args:
        has_json (bool): Whether or not the request has json.
        has_files (bool): Whether or not the request has files.
        request_specific_headers (dict): Additional headers specified by the user for a specific request.
    Returns:
        The headers dictionary.
            e.g. {
                'Content-Type': 'application/json;charset=utf-8',
                'Authorization': 'jwt ey.....',
                'User-Agent': 'Python/3.10.6 Acho/0.0.1 Darwin/17.7.0'
            }
    """
    final_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if headers is None or "User-Agent" not in headers:
        final_headers["User-Agent"] = get_user_agent()

    if token:
        final_headers.update({"Authorization": "jwt {}".format(token)})
    if headers is None:
        headers = {}

    # Merge headers specified at client initialization.
    final_headers.update(headers)

    # Merge headers specified for a specific request. e.g. oauth.access
    if request_specific_headers:
        final_headers.update(request_specific_headers)

    if has_json:
        final_headers.update({"Content-Type": "application/json;charset=utf-8"})

    # if has_files:
    #     # These are set automatically by the aiohttp library.
    #     final_headers.pop("Content-Type", None)

    return final_headers

def get_user_agent(prefix: Optional[str] = None, suffix: Optional[str] = None):
    """Construct the user-agent header with the package info,
    Python version and OS version.
    Returns:
        The user agent string.
        e.g. 'Python/3.6.7 acho_py/0.0.1 Darwin/17.7.0'
    """
    # __name__ returns all classes, we only want the client
    client = "{0}/{1}".format("acho_py", version.__version__)
    python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info)
    system_info = "{0}/{1}".format(platform.system(), platform.release())
    user_agent_string = " ".join([python_version, client, system_info])
    prefix = f"{prefix} " if prefix else ""
    suffix = f" {suffix}" if suffix else ""
    return prefix + user_agent_string + suffix
    
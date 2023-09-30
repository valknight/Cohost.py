import logging
import time
import json
import json.decoder
import requests
from typing import Any, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
API_BASE = "https://cohost.org/api/v1"

cache: dict[str, dict[str, Any]] = {}

headers: dict[str, str] = {
    'User-Agent': 'cohost.py'
}

timeout = 30


def fetch(
    method: str,
    endpoint: str,
    data: Optional[dict[str, Any]],
    cookies: dict[str, str] = {},
    complex: bool = False
) -> dict[str, Any]:
    """Send requests to cohost API, and return back data

    Args:
        method (str): _description_
        endpoint (str): _description_
        data (Optional[dict[str, Any]]): _description_
        cookies (str, optional): _description_. Defaults to "".
        complex (bool, optional): _description_. Defaults to False.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if not endpoint.startswith('/'):
        endpoint = "/" + endpoint
    url = API_BASE + endpoint
    logger.debug('{} to {}'.format(method, url))
    if method.lower() == "get":
        req = requests.get(url, cookies=cookies, params=data, headers=headers)
    elif method.lower() == "post":
        req = requests.post(url, cookies=cookies, data=data, headers=headers)
    elif method.lower() == 'postjson':
        req = requests.post(url, cookies=cookies, json=data, headers=headers)
    elif method.lower() == 'put':
        req = requests.put(url, cookies=cookies, json=data, headers=headers)
    else:
        logger.error('No such method handled: ' + method)
        logger.error('Defaulting to get')
        return fetch("GET", endpoint, data, cookies, complex)

    try:
        res = req.json()
    except json.decoder.JSONDecodeError:
        raise Exception(req.text)

    if (req.status_code >= 400 and method != 'put'):
        raise Exception(res)
    if complex:
        return {
            'headers': req.headers,
            'body': res
        }
    return res


def fetchTrpc(methods: list[str] | str, cookie: str,
              data: Optional[dict[str, Any]] = None, methodType="get") -> dict[str, Any]:
    global cache
    """Fetch data from trpc API

    Args:
        methods (list[str] | str): List of data points (or single data point) to retrieve
        cookie (str): Cookie of the user to retrieve from

    Returns:
        _type_: JSON encoded list from the trpc endpoint
    """
    if isinstance(methods, str):
        m = methods
    else:
        m = ','.join(methods)
    if methodType == "get":
        cacheData = get_cache_data(cookie, m)
        if cacheData is not None:
            logger.debug('Cache hit!')
            return cacheData
    
    # The trpc api expects values under "input" in a particular format, so we'll validate that here
    if data and 'input' in data:
        input_val = data.get('input')
        if not isinstance(input_val, dict):
            raise ValueError('"input" key must have a dict value')
        # We need to serialize the input object to JSON here
        # Default requests behavior doesn't handle nested dicts the way we want
        data['input'] = json.dumps(input_val)

    returnData = fetch(methodType, "/trpc/{}".format(m), data=data,
                       cookies=generate_login_cookies(cookie))
    assert isinstance(returnData, dict)
    if methodType == "get":
        set_cache_data(cookie, m, returnData)
    return returnData


# Caching utils !
def set_cache_data(cookie: str, key: str, data: Any) -> None:
    if cache.get(cookie, None) is None:
        cache[cookie] = {}
    cache[cookie][key] = {
        'data': data,
        'time': time.time()
    }


def get_cache_data(cookie: str, key: str) -> Any:
    entry = cache.get(cookie, {}).get(key, None)
    if entry is None:
        return None
    if time.time() - entry['time'] > timeout:
        return None
    return entry['data']


def generate_login_cookies(cookie: str) -> dict[str, str]:
    return {
        'connect.sid': cookie
    }

import httpx
import xml.etree.ElementTree as ElementTree

from .config import settings

url_get_tree: str
auth_sid: str


def setup():
    # setup nas url
    params = {
        "user": settings.nas_username,
        "pwd": settings.nas_password,
    }
    url_login = "http://" + settings.nas_ip + \
        ":" + settings.nas_port + "/cgi-bin/authLogin.cgi"
    try:
        r = httpx.get(url_login, params=params)
        # print(f"Sending request : {r.url}")
        dom = ElementTree.fromstring(r.text)
        global auth_sid
        for log in dom.iter('authSid'):
            auth_sid = log.text
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    global url_get_tree
    url_get_tree = "http://" + settings.nas_ip + ":" + \
        settings.nas_port + "/cgi-bin/filemanager/utilRequest.cgi"


def read_folder(path: str):
    """
    Read subfolder inside inward folder
    """
    params = {
        "func": "get_tree",
        "sid": auth_sid,
        "is_iso": 0,
        "node": path
    }
    try:
        r = httpx.get(url_get_tree, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    assets = []
    for item in response:
        assets.append(item['text'])
    return assets


def read_inward(base_path):
    """
    Read assets inside inward folder
    """
    params = {
        "func": "get_tree",
        "sid": auth_sid,
        "is_iso": 0,
        "node": base_path
    }
    try:
        r = httpx.get(url_get_tree, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    if isinstance(response, dict):
        raise Exception("No records found")

    assets = []
    for item in response:
        path = base_path + "/" + item['text']
        path_assets = read_folder(path)
        assets += path_assets

    # remove duplicates
    assets = set(assets)
    assets = list(assets)

    return assets


def read_assets(date: str, inward: str):
    """
    Reas assets for specified date and inward
    """

    # initialize
    setup()
    base_path = settings.nas_prefix + "/" + date

    params = {
        "func": "get_tree",
        "sid": auth_sid,
        "is_iso": 0,
        "node": base_path
    }
    try:
        r = httpx.get(url_get_tree, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    if isinstance(response, dict):
        raise Exception("No records found")

    # identify inward folder
    for item in response:
        folder = item['text']
        tokens = folder.split("-", 1)
        if tokens[0] == inward:
            base_path = base_path + "/" + folder
            break

    return read_inward(base_path)

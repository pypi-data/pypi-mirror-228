import httpx

from .config import settings


def upload_inward(inward: str, assets: list):
    """
    Update upload status of the assets for specified inward
    """
    url = settings.console_endpoint + "/studio/job_inwards/upload/status"
    data = {
        "inward_id": inward,
        "asset_names": assets
    }
    try:
        headers = {"Authorization": f"Bearer {settings.console_token}"}
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Server : {response.text}")
    except httpx.RequestError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise Exception(f"Server error : {exc.response.text}")
        else:
            raise Exception(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

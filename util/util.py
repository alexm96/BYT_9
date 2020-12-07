import requests

def get_last_modified(some_response:requests.Response):
    return some_response.headers.get("last-modified") or None
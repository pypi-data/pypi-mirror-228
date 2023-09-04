import re

from seleniumwire.request import Request


def get_request_with_path(requests: list[Request], path: str) -> Request | None:
    for request in requests:
        if re.search(re.escape(path), request.url):
            return request
    return None

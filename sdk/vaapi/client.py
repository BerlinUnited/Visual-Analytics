from .base_client import VaapiBase
import requests
import json


class Vaapi(VaapiBase):
    """"""

    __doc__ += VaapiBase.__doc__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VATClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def execute(self, query, variables=None):
        # TODO check if we can return data in better way
        default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}",
        }
        data = {"query": query, "variables": variables}
        req = requests.post(
            f"{self.base_url}graphql/",
            data=json.dumps(data).encode("utf-8"),
            headers=default_headers,
        )
        return req.json()

import requests
import os

base_url = os.getenv("VAT_API_URL")
api_key = os.getenv("VAT_API_TOKEN")


default_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Token {api_key}",
}

# filtering still works
query_params = {
    "log": 282,
    "offset": 25000,  # starting point
    "limit": 30,  # max images per page
    "camera": "TOP",
}


resp = requests.get(
    f"{base_url}api/image-list", headers=default_headers, params=query_params
)

# next contains url to next page including query_params
while resp.json()["next"]:
    resp = requests.get(resp.json()["next"], headers=default_headers)

    print(resp.json()["results"])

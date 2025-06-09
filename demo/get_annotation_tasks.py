"""
Fetches links to images that need their annotations validated
"""

import os
from vaapi.client import Vaapi

client = Vaapi(
    base_url=os.environ.get("VAT_API_URL"),
    api_key=os.environ.get("VAT_API_TOKEN"),
)
mylist = client.annotations.task(class_name="ball", amount=20, prio_only=False)[
    "result"
]

print(len(mylist))
print(mylist)

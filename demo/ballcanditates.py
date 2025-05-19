"""
Similar to
response = client.ballcandidates.list(
        log_id=1,
    )

you can use any representation name present in the game.log to query it except behavior. Behavior is handled differently.
"""

from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    response = client.ballcandidates.list(
        log=1,
    )
    print(response)

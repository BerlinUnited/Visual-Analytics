from vaapi.client import Vaapi
import os

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    response = client.ballcandidates.list(
        log_id=1,
    )
    print(response)
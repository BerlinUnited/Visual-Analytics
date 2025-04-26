from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    """
    Get Top Images
    """
    response = client.image.list(
        log=155,
        camera="TOP",
    )
    for i in response:
        print(i)

from vaapi.client import Vaapi
import os

def count_bottom_image():
    response = client.image.get_image_count(camera="BOTTOM")
    print(response)

def count_bottom_image_no_blurredness():
    response = client.image.get_image_count(camera="BOTTOM", blurredness_value="None")
    print(response)

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
    print(response[0])

    count_bottom_image()
    count_bottom_image_no_blurredness()

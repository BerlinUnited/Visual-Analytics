from vaapi.client import Vaapi
import os

def get_image_list():
    """
    Get Top Images from log 155 and print the first image
    The list is not sorted. The actual image data is not part of the response. 
    You have to get that from the returned image url
    """
    response = client.image.list(
        log=155,
        camera="TOP",
    )
    print(response[0])

def print_image_stats():
    all_top_images = client.image.get_image_count(camera="TOP")["count"]
    all_bottom_images = client.image.get_image_count(camera="BOTTOM")["count"]

    top_images_values_not_calculated = client.image.get_image_count(camera="TOP", blurredness_value="None")["count"]
    bottom_images_values_not_calculated = client.image.get_image_count(camera="BOTTOM", blurredness_value="None")["count"]
    
    top_calculated_perc = 100 - (top_images_values_not_calculated / all_top_images) * 100
    bottom_calculated_perc = 100 - (bottom_images_values_not_calculated / all_bottom_images) * 100
    print(f"Top Images where blurredness factor is calculated: {top_calculated_perc}%")
    print(f"Bottom Images where blurredness factor is calculated: {bottom_calculated_perc}%")


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    print_image_stats()

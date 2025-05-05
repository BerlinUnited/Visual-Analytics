from vaapi.client import Vaapi
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import requests
import cv2
import os


def download_image():
    response = client.image.list(
        log=155,
        camera="TOP",
    )
    print(response[0].image_url)
    url = "https://logs.berlin-united.com/" + response[0].image_url
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    image = np.asarray(bytearray(response.content), dtype="uint8")
    image_cv = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite("test.png", image_cv)


def example_histogram():
    response = client.image.list(
        log=155,
        camera="BOTTOM",
    )
    brightness_values = [val.brightness_value for val in response]
    blurredness_values = [val.blurredness_value for val in response]
    plt.title("brightness_values")
    plt.hist(brightness_values)
    plt.show() 

    plt.title("blurredness_values")
    plt.hist(blurredness_values)
    plt.show() 


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

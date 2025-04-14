from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    resp = client.annotations.create(
        image_id=2,
        annotation={
            "bbox": [
                {
                    "x": 170,
                    "y": 280,
                    "id": 123,
                    "label": "ball",
                    "width": 100,
                    "height": 100,
                }
            ]
        },
    )
    print(resp)

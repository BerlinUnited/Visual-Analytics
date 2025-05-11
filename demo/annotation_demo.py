from vaapi.client import Vaapi
import os

def print_annotation_stats():
    # FIXME we cant filter for camera yet
    all_annotations = client.annotations.count(class_name="ball")["count"]
    validated_annotations = client.annotations.count(class_name="ball", validated=True)["count"]
    
    validation_progress = (validated_annotations / all_annotations) * 100

    print(f"Percent of Ball Annotations validated: {validation_progress}%")


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    print_annotation_stats()

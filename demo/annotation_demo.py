from vaapi.client import Vaapi
import os

def list_annotations_per_log():
    log = client.logs.list()

    def sort_key_fn(log):
        return log.id
    
    for log in sorted(log, key=sort_key_fn):
        count = client.annotations.count(log=log.id, class_name="ball", validated=False)["count"]
        if count < 100 and count > 0:
            print(f"{log.id} - {count} ball annotations")

def print_annotation_stats():
    # FIXME we cant filter for camera yet
    all_annotations = client.annotations.count(class_name="ball")["count"]
    validated_annotations = client.annotations.count(class_name="ball", validated=True)["count"]
    
    validation_progress = (validated_annotations / all_annotations) * 100

    print(f"Percent of Ball Annotations validated: {validation_progress}%")
    print(f"You already validated {validated_annotations} Ball Annotations of of {all_annotations}")


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    print_annotation_stats()
    #list_annotations_per_log()
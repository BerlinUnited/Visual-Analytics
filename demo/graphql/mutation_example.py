import os
import json
from vaapi.client import VATClient

event_mutation = """
mutation CreateOrGetEvent($input: CreateEventInput!) {
  bla(input: $input) {
    endDay
    errors {
      field
      messages
    }
  }
}
"""

event_variables = {
    "input": {
        "name": "2024-07-15_RC26",
        "startDay": "2026-11-15",
        "endDay": "2026-11-17",
        "timezone": "UTC",
        "country": "Germany",
        "location": "40.7128° N, 74.0060° W",
    }
}


create_annotation_mutation = """mutation CreateAnnotation($input: CreateAnnotationInput!){
  CreateAnnotation(input: $input)
  {
    image
    annotation
  }
}"""

json_box = {
    "bbox": [
        {
            "x": 0.42298688888549807,
            "y": 0.5065087000528972,
            "id": "DDF51B611",
            "label": "ich",
            "width": 0.06891517639160157,
            "height": 0.09018630981445312,
        }
    ]
}

create_mutation_variables = {
    "input": {"image": "2", "annotation": json.dumps(json_box)}
}

update_annotation_mutation = """mutation updateAnnotation($input:UpdateAnnotationInput!)
{
  UpdateAnnotation(input:$input){
    image
  }
}"""

json_box_2 = {
    "bbox": [
        {
            "x": 0.42298688888549807,
            "y": 0.5065087000528972,
            "id": "DDF51B611",
            "label": "nao",
            "width": 0.06891517639160157,
            "height": 0.09018630981445312,
        }
    ]
}

update_mutation_variables = {
    "input": {"image": "2", "annotation": json.dumps(json_box_2)}
}


if __name__ == "__main__":
    client = VATClient(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    data = client.execute(update_annotation_mutation, update_mutation_variables)
    print(data)

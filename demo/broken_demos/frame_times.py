from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    """
    Get FrameInfo from Cognition Process
    """
    response = client.cognition_repr.list(
        log_id=168,
        representation_name="FrameInfo",
    )
    print(response[0])

    """
    Get FrameInfo from Motion Process
    """
    response = client.motion_repr.list(
        log_id=168,
        representation_name="FrameInfo",
    )
    print(response[0])

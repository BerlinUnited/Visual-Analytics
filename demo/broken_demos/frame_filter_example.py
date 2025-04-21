from vaapi.client import Vaapi
import os


def frame_filter_demo(client):
    response = client.behavior_frame_option.filter(
        log_id=168,
        option_name="path_striker2024",
        state_name="forwardkick",
    )

    # publish the frames list
    resp = client.frame_filter.create(
        log_id=168,
        frames={"frame_list": response},
    )
    print(resp)


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    frame_filter_demo(client)

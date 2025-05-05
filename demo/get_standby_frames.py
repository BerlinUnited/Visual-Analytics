from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="decide_game_state",
        state_name="standby",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

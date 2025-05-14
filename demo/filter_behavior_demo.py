from vaapi.client import Vaapi
import os


def get_standby_frames():
    response = client.behavior_frame_option.filter(
        log=282,
        option_name="decide_game_state",
        state_name="standby",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))


def get_fallen_frames():
    """
    You need to query all states except idle
    https://scm.cms.hu-berlin.de/berlinunited/naoth-2020/-/blob/develop/NaoTHSoccer/Source/Cognition/Modules/Behavior/XABSLBehaviorControl/Options/Basics/fall_down_and_stand_up.xabsl?ref_type=heads
    """
    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="falling_front",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="falling_front_wait",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="falling_back",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="falling_back_wait",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="falling",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="wait_before_stand_up",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="stand_up",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="stand",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))

    response = client.behavior_frame_option.filter(
        log=282,
        option_name="fall_down_and_stand_up",
        state_name="wait_for_completed_stand",
    )
    frame_numbers = [frame.frame_number for frame in response]
    print(sorted(frame_numbers))


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_fallen_frames()

"""
TODO given any time in ms give the closest frame number back
"""

from vaapi.client import Vaapi
import numpy as np
import os


# 20230
def main(timestamp=7000, log_id=282):
    # TODO get first standby frame as baseline
    response = client.behavior_frame_option.filter(
        log=log_id,
        option_name="decide_game_state",
        state_name="standby",
    )

    def sort_key_fn(frame):
        return frame.frame_number

    sorted_frames = sorted(response, key=sort_key_fn)
    print("first standby frame", sorted_frames[0])  # first standby frame

    # TODO get all cognition frames here
    cognition_frames = client.cognitionframe.list(log=282)
    cognition_frames = sorted(cognition_frames, key=sort_key_fn)
    print("first frame time: ", cognition_frames[0].frame_time)
    frame_time_diffs = [frame.frame_time - (sorted_frames[0].frame_time + timestamp) for frame in cognition_frames]
    frame_time_diffs = np.array(frame_time_diffs)

    target_frame_index = np.argmin(np.abs(frame_time_diffs))

    print(target_frame_index)
    print(frame_time_diffs[target_frame_index])
    print("target: ", cognition_frames[target_frame_index])
    # print(min(abs(frame_time_diffs)))


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    main()

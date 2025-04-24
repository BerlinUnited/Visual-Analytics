"""
Small demo showing what is possible with our new Visual Analytics Tool

1. get all frames where option name path_striker2024 and forwardkick from behavior frame options
    => only return the frame numbers
2. Use the frames as filter for Images (not implemented yet)
"""

from vaapi.client import Vaapi
from iterfzf import iterfzf
import os


def group_consecutive_integers(numbers):
    if not numbers:
        return []

    # Sort the list
    sorted_numbers = sorted(numbers)

    # Initialize the result and the first group
    result = []
    current_group = [sorted_numbers[0]]

    # Iterate through the sorted list starting from the second element
    for num in sorted_numbers[1:]:
        if num == current_group[-1] + 1:
            # If the number is consecutive, add it to the current group
            current_group.append(num)
        else:
            # If there's a gap, add the current group to the result and start a new group
            result.append(current_group)
            current_group = [num]

    # Add the last group
    result.append(current_group)

    return result


def demo1(client, log_id):
    response = client.behavior_frame_option.filter(
        log=log_id,
        option_name="path_striker2024",
        state_name="forwardkick",
    )
    frame_numbers = [frame.frame_number for frame in response]

    grouped_numbers = group_consecutive_integers(frame_numbers)
    print(f"Number of times the robot tried to kick: {len(grouped_numbers)}")
    for group in grouped_numbers:
        print(f"Spend {len(group)} frames doing the forwardkick")


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    logs = client.logs.list()

    log_map = {str(log): log for log in logs}
    selected_str = iterfzf(log_map.keys())
    if selected_str:
        selected_log = log_map[selected_str]
        demo1(client, selected_log.id)

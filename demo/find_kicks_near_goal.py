""" """

from vaapi.client import Vaapi
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


def find_kick_frames(client):
    response = client.behavior_frame_option.filter(
        log_id=168,
        option_name="path_striker2024",
        state_name="forwardkick",
    )

    grouped_numbers = group_consecutive_integers(response)
    print(f"Number of times the robot tried to kick: {len(grouped_numbers)}")
    for group in grouped_numbers:
        print(group[0])
        # TODO find the location in the xabsl symbols
        symbols = client.xabsl_symbol_sparse.list(log_id=168, frame=group[0])

        print(symbols[0].data["input"]["robot_pose.planned.x"])

        quit()


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    find_kick_frames(client)

"""
    Small demo showing what is possible with our new Visual Analytics Tool

    1. get all frames where option name path_striker2024 and forwardkick from behavior frame options
        => only return the frame numbers
    2. Use the frames as filter for Images (not implemented yet)
"""
from vaapi.client import Vaapi
import os

def check_if_imu_changes(response):
    if len(response) < 2:
        return True
    
    for i in range(len(response) - 1):
        if response[i].representation_data["location"]["x"] == response[i + 1].representation_data["location"]["x"]:
            print(i)
            return False
    return True

if __name__ == "__main__":
    client = Vaapi(
        base_url='https://api.berlin-united.com/',  
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    response = client.motion_repr.list(
        log_id=168,
        representation_name='IMUData',
    )
    #print(len(response))
    #print(response[0])
    #print(type(response[0]))
    #print(response[0].representation_data)

    a = check_if_imu_changes(response)
    print(a)
    
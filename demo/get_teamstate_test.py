from vaapi.client import Vaapi
import os


def get_logs():
    response = client.teamstate.list(
        log_id=2,
    )
    print(response[1])


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    get_logs()


"""
OUTPUT: 

"""



from vaapi.client import Vaapi
import os
from tests.event_tests import basic_event_tests
from tests.game_tests import basic_game_tests
from tests.logs_tests import basic_log_tests
from tests.cognition_repr_test import basic_cognition_repr_tests
from tests.motion_repr_test import basic_motion_repr_tests


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    # a = client.annotations.get(id=1)
    # print(a)

    basic_event_tests(client)
    print()
    basic_game_tests(client)
    print()
    basic_log_tests(client)
    print()
    basic_cognition_repr_tests(client)
    print()
    basic_motion_repr_tests(client)

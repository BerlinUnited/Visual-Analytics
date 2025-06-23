"""
Parse log data locally
"""

from vaapi.client import Vaapi
from google.protobuf.json_format import MessageToDict
from naoth.log import Reader as LogReader
from naoth.log import Parser
import mmap
import os

client = Vaapi(
    base_url=os.environ.get("VAT_API_URL"),
    api_key=os.environ.get("VAT_API_TOKEN"),
)

response = client.imudata.list(log=282)

my_parser = Parser()
a = response["results"]
"""
for idx, i in enumerate(response["results"]):
    print(idx)
    message = my_parser.parse("IMUData", bytes(i["binary_data"]))
    message_dict = MessageToDict(message)
    print(message_dict)

# quit()
log_path = "/mnt/e/logs/2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/game_logs/7_33_Nao0022_250315-1822/sensor.log"
file = open(log_path, "rb")

my_parser = Parser()
game_log = LogReader(str(log_path), my_parser)

my_mmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

data = my_mmap[a[0]["start_pos"] : a[0]["start_pos"] + a[0]["size"]]
print()
message = my_parser.parse("IMUData", bytes(data))
message_dict = MessageToDict(message)
print(message_dict)
"""

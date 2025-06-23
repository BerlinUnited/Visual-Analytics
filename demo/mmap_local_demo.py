"""
Parse log data locally
"""

from vaapi.client import Vaapi
from naoth.log import Reader as LogReader
from naoth.log import Parser
import mmap
import os

client1 = Vaapi(
    base_url="https://vat.berlin-united.com/",
    api_key="b1abe053d2eaae8e3232c11d65caf8ad3f296ea4",
)

response = client1.imudata.list(log=282)
print(response[0])
quit()

client2 = Vaapi(
    base_url=os.environ.get("VAT_API_URL"),
    api_key=os.environ.get("VAT_API_TOKEN"),
)
log_path = "/mnt/e/logs/2025-03-12-GO25/2025-03-13_10-10-00_BerlinUnited_vs_Bembelbots_half1/game_logs/2_36_Nao0018_250313-1032/sensor.log"
file = open(log_path, "rb")


my_parser = Parser()
my_parser.register("ImageJPEG", "Image")
my_parser.register("ImageJPEGTop", "Image")
game_log = LogReader(str(log_path), my_parser)

my_mmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

data = my_mmap[position : position + size]

message = my_parser.parse("ImageJPEGTop", bytes(data))

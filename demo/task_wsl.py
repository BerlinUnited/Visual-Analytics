import subprocess
import os
from vaapi.client import Vaapi

client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
mylist= client.annotations.task(class_name="ball", amount=10)["result"]

print(mylist)
for link in mylist:
    subprocess.run(['powershell.exe', '-Command', f'Start-Process "{link}"'])
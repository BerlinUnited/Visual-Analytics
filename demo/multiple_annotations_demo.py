import os
import subprocess
from vaapi.client import Vaapi

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    links = client.annotations.multiple(amount=10)["result"]
    for link in links:
        subprocess.run(['powershell.exe', '-Command', f'Start-Process "{link}"'])
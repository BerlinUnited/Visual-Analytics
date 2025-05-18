import os
import subprocess
from vaapi.client import Vaapi

query_params = {
   "amount":10,
   "y_gte": 0.01,
    "width_lte" : 0.07,
    "x_gte":0.9, #right border
    # "x_lte":0.01 #left border
}

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    links = client.annotations.border(amount=10,
                                      y_gte=0.01,
                                      width_lte=0.07,
                                      x_gte=0.9, # right border
                                    #   x_lte=0.01 #left border
                                      )["result"]
    for link in links:
        subprocess.run(['powershell.exe', '-Command', f'Start-Process "{link}"'])
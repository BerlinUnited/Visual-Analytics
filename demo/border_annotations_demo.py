import requests
import os
import subprocess

base_url=os.getenv("VAT_API_URL")
api_key=os.getenv("VAT_API_TOKEN")


default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Token {api_key}",
        }


query_params = {
   "amount":10,
   "y_gte": 0.01,
    "width_lte" : 0.07,
    "x_gte":0.9, #right border
    # "x_lte":0.01 #left border
}




resp = requests.get(f"{base_url}api/annotation-task/border",headers=default_headers,params=query_params)

for link in resp.json()["result"]:
    subprocess.run(['powershell.exe', '-Command', f'Start-Process "{link}"'])
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

#filtering still works
query_params = {
   "amount":10
}


resp = requests.get(f"{base_url}api/annotation-task/multiple",headers=default_headers,params=query_params)

for link in resp.json()["result"]:
    subprocess.run(['powershell.exe', '-Command', f'Start-Process "{link}"'])
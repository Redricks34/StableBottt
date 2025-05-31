from requests.auth import HTTPBasicAuth

api_key = "8FDMB6CCISMARJK4C6LP24GPCGI59MUAS1UEPXIF"
import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

job_id = "04e7f177-6d87-48e8-8b67-3a13448cdd01-e1"

res = requests.post(url=f'https://api.runpod.ai/v2/r9puknkh1poi7d/status/{job_id}', auth=BearerAuth(f'{api_key}'))
print(res.text)
if "images" in res.text:
    print("")
elif "request does not exist" in res.text:
    print("test")
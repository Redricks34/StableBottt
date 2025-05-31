import requests

url = "https://api.runpod.ai/v2/blip/runsync"

payload = { "input": {
        "data_url": "https://api.telegram.org/file/bot6033859236:AAHWUn47MwBQCNRV39nRHutS0ZuuksLI_W8/photos/file_269.jpg",
        "max_length": 75,
        "min_length": 5
    } }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "8FDMB6CCISMARJK4C6LP24GPCGI59MUAS1UEPXIF"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
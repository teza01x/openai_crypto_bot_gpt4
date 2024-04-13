import requests

url = "https://api.tokenmetrics.com/tmai"

payload = "{ \"messages\":[ { \"user\": \"Give me please analyze 0xdac17f958d2ee523a2206206994597c13d831ec7 on this contract\" } ] }"
headers = {
    "accept": "application/json",
    "api_key": "tm-6d7cc4f6-86b6-4021-8745-a48faf3d5f0f",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
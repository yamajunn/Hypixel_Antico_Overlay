import requests
import pprint

uuid = "1ced16db2bc54354917f7bf8382b8840"
POLSU_KEY = "a5759d02-94e9-466a-8e40-6679b1ccb256"

url = "https://api.polsu.xyz/polsu/minecraft/api"

querystring = {"name":"antisniper"}

headers = {"Api-Key": POLSU_KEY}

response = requests.get(url, headers=headers, params=querystring)

response = requests.get(url, headers=headers, params=querystring)
response.raise_for_status()  # HTTP エラーがあれば例外を発生させる
pings = response.json()
pprint.pprint(pings)
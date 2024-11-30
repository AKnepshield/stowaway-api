import requests
import os

DISCOGS_KEY = os.environ["DISCOGS_KEY"]
DISCOGS_SECRET = os.environ["DISCOGS_SECRET"]

url = f"https://api.discogs.com/database/search?q=Nirvana&key={DISCOGS_KEY}&secret={DISCOGS_SECRET}"

payload = {}
headers = {
    "Cookie": "__cf_bm=jl98Vk50otrzA62d2Co9Tp2JpdR_gHuwI9qpwLlJW20-1732995312-1.0.1.1-AssJwFuWSFtRcszUhUO8jSHCwSqrcO0Rkoo6jO1ZJZWQemHB6qOzczkUTm.233dlVWUOPc3l0.oUVy6r4sSJUA"
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

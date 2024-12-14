import requests
import os


DISCOGS_KEY = os.environ["DISCOGS_KEY"]
DISCOGS_SECRET = os.environ["DISCOGS_SECRET"]


def search_discogs(query):

    url = f"https://api.discogs.com/database/search"

    params = {
        "q": query,
        "key": DISCOGS_KEY,
        "secret": DISCOGS_SECRET,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    user_query = input("Enter an artist you would like to search for: ")
    result = search_discogs(user_query)
    print(result)

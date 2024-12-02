import requests
from typing import Optional, List


class NominatimAPI:
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, user_agent: str):
        if not user_agent:
            raise ValueError("A User-Agent header is required to use the Nominatim API.")
        self.headers = {"User-Agent": user_agent}

    def search_location(self, query: str, format: str = "json", limit: Optional[int] = 1) -> List[dict]:
        params = {
            "q": query,
            "format": format,
            "limit": limit,
        }
        try:
            response = requests.get(self.BASE_URL, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while accessing the Nominatim API: {e}")
            return []
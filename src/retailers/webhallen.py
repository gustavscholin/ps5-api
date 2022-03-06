import requests


class WebhallenProductStockScraper:

    ps5_url = "https://www.webhallen.com/api/product/300815"

    @classmethod
    def scrape(cls, url: str):
        api_response = requests.get(url)
        data = api_response.json()
        for i, s in data["product"]["stock"].items():
            if i in ("web", "supplier", "orders") or i.isnumeric():
                if s > 0:
                    return True
        return False

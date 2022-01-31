import requests


class WebhallenProductStockScraper:

    ps5_url = "https://www.webhallen.com/api/product/300815"

    @classmethod
    def scrape(cls, url: str):
        response = requests.get(url)
        return response.status_code == 200

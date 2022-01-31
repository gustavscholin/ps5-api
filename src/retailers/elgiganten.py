import requests
from bs4 import BeautifulSoup


class ElgigantenProductStockScraper:

    ps5_url = 'https://www.elgiganten.se/cxorchestrator/se/api?appMode=b2c&user=anonymous&operationName=getProductWithDynamicDetails&variables={"articleNumber":"345097","withCustomerSpecificPrices":false}&extensions={"persistedQuery":{"version":1,"sha256Hash":"71e301b8e2a96d97efb141d297ab0880ae67cebb9e3c0f6d4184977075f64c06"}}'

    @classmethod
    def scrape(cls, url: str):
        api_response = requests.get(url, headers={"User-Agent": "My User Agent 1.0"})
        data = api_response.json()
        return data["data"]["product"]["buyableOnline"]

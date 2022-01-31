import requests
from bs4 import BeautifulSoup


class InetProductStockScraper:

    ps5_url = "https://www.inet.se/produkt/6609649/sony-playstation-5"

    @classmethod
    def scrape(cls, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="html.parser")
        stock_text = (
            soup.find("section", {"class": "box box-body product-stock"})
            .find_next("span")
            .get_text(strip=True)
        )
        return "I lager" in stock_text

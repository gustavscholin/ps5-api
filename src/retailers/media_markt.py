import requests
from bs4 import BeautifulSoup


class MediaMarktProductStockScraper:

    ps5_url = (
        "https://www.mediamarkt.se/sv/product/_sony-playstation-5-ps5-1283580.html"
    )

    @classmethod
    def scrape(cls, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, features="html.parser")
        stock_text = soup.find("div", {"class": "box infobox availability"}).get_text(
            strip=True
        )
        return "Finns i webblager" in stock_text

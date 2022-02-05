import requests
from bs4 import BeautifulSoup


class NetOnNetProductStockScraper:

    ps5_url = "https://www.netonnet.se/art/gaming/spel-och-konsol/playstation/playstation-konsol/sony-playstation-5/1012886.14413/"

    @classmethod
    def scrape(cls, url: str):
        html = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "www.netonnet.se",
            },
        ).text
        soup = BeautifulSoup(html, features="html.parser")
        stock_text = soup.find("div", {"class": "productSpec"}).get_text(strip=True)
        return "PlayStation 5 är slut i lager" not in stock_text


if __name__ == "__main__":
    print(NetOnNetProductStockScraper.scrape(NetOnNetProductStockScraper.ps5_url))

import logging

from flask import Flask, jsonify

from retailers.elgiganten import ElgigantenProductStockScraper
from retailers.inet import InetProductStockScraper
from retailers.media_markt import MediaMarktProductStockScraper
from src.retailers.webhallen import WebhallenProductStockScraper

app = Flask(__name__)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

SCRAPING_CLASSES = {
    "media_markt": MediaMarktProductStockScraper,
    "elgiganten": ElgigantenProductStockScraper,
    "inet": InetProductStockScraper,
    "webhallen": WebhallenProductStockScraper,
}


@app.route("/ps5_availability/<retailer>")
def ps5_availability(retailer):
    scraping_class = SCRAPING_CLASSES[retailer]
    url = scraping_class.ps5_url
    in_stock = scraping_class.scrape(url)
    return jsonify(
        {
            "retailer": retailer,
            "url": url,
            "in_stock": in_stock,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

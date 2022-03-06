import argparse
from datetime import datetime

import psycopg2
import requests
from psycopg2 import sql

RETAILERS = [
    "media_markt",
    "elgiganten",
    "inet",
    "webhallen",
    "netonnet",
]


def main(
    db_name: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: str,
    api_host: str,
    telegram_bot_token: str,
    telegram_chat_id: int,
    testing: bool,
):
    db_table = "ps5_availability"
    if testing:
        db_table += "_test"

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    cur = conn.cursor()

    cur.execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                retailer VARCHAR,
                in_stock VARCHAR,
                check_time TIMESTAMP
            );
            """
        ).format(sql.Identifier(db_table)),
    )

    for retailer in RETAILERS:
        # Get status from last check
        cur.execute(
            sql.SQL(
                """
                SELECT in_stock
                FROM {}
                WHERE retailer = %s
                ORDER BY check_time DESC
                """
            ).format(sql.Identifier(db_table)),
            (retailer,),
        )
        latest_stock_status = cur.fetchone()
        latest_stock_status = latest_stock_status[0] if latest_stock_status else None

        # Get current status from API
        current = requests.get(f"https://{api_host}/ps5_availability/{retailer}")
        if current.status_code != 200:
            current_stock_status = "Error"
        else:
            current_stock_status = str(current.json()["in_stock"])

        # Insert current status
        cur.execute(
            sql.SQL(
                """
                INSERT INTO {} (retailer, in_stock, check_time)
                VALUES (%s, %s, %s)
                """
            ).format(sql.Identifier(db_table)),
            (
                retailer,
                current_stock_status,
                datetime.now(),
            ),
        )

        if current_stock_status != latest_stock_status:
            if latest_stock_status == "False" and current_stock_status == "True":
                status_string = f"✅ PS5 is possibly available at {retailer} ✅"
            elif latest_stock_status == "True" and current_stock_status == "False":
                status_string = f"❌ PS5 is no longer available at {retailer} ❌"
            elif current_stock_status == "Error":
                status_string = f"⛔️ Something's wrong with the API for {retailer} ⛔️\nGave status code {current.status_code}"
            elif latest_stock_status == "Error" or latest_stock_status is None:
                status_string = f"🆗 API for {retailer} is up and running 🆗\n"
                if current_stock_status == "False":
                    status_string += "No PS5s though 😞"
                elif current_stock_status == "True":
                    status_string += "✅ And PS5s are possibly available ✅"

            if not testing:
                requests.post(
                    f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                    data={"chat_id": telegram_chat_id, "text": status_string},
                )
        else:
            status_string = ""

        if testing:
            print(f"Stats for {retailer}")
            print(f"Latest status: {latest_stock_status}")
            print(f"API response: {current.json()}")
            print(f"Status string: {status_string}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db_name", type=str, default="ps5api", help="name of the Postgres database"
    )
    parser.add_argument("--db_user", type=str, required=True, help="database username")
    parser.add_argument(
        "--db_password", type=str, required=True, help="database password"
    )
    parser.add_argument(
        "--db_host", type=str, default="localhost", help="database host"
    )
    parser.add_argument("--db_port", type=int, default=5432, help="database port")
    parser.add_argument(
        "--api_host", type=str, required=True, help="domain name for the API"
    )
    parser.add_argument(
        "--tg_bot_token", type=str, required=True, help="Telegram bot HTTPS token"
    )
    parser.add_argument(
        "--tg_chat_id",
        type=int,
        required=True,
        help="Telegram chat id (chat where updates are posted)",
    )
    parser.add_argument(
        "--testing",
        action=argparse.BooleanOptionalAction,
        help="run in test mode (test database and status in std_out)",
    )

    args = parser.parse_args()
    main(
        args.db_name,
        args.db_user,
        args.db_password,
        args.db_host,
        args.db_port,
        args.api_host,
        args.tg_bot_token,
        args.tg_chat_id,
        args.testing,
    )

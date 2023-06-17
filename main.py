#!/usr/bin/env python3
import datetime
import traceback
from typing import Sequence, Tuple
from sources import DataSource, Dish, display_dishes
from sources.garden_restaurant import GardenRestaurant
from sources.west_hub_canteen import WestHubCanteen
from sources.chu_dining import ChuDining
from html import escape
import telegram_send
import argparse


def render_html(
    meal: str, restaurants: Sequence[Tuple[DataSource, Sequence[Dish]]]
) -> str:
    date = datetime.date.today().strftime("%d %b %Y")
    html = f"<i>What to eat for {meal} on {date}</i>\n\n"
    for restaurant, dishes in restaurants:
        if len(dishes) == 0:
            continue

        html += f'<b><a href="{restaurant.link}">{escape(restaurant.name)}</a></b>\n'
        html += display_dishes(dishes)
        html += "\n\n"
    return html


RESTAURANTS = [GardenRestaurant(), WestHubCanteen(), ChuDining()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("meal", choices=["lunch", "dinner"])
    parser.add_argument("--telegram-send-conf", type=str)
    args = parser.parse_args()

    menus = []

    for restaurant in RESTAURANTS:
        try:
            if args.meal == "lunch":
                menu = restaurant.get_lunch()
            else:
                menu = restaurant.get_dinner()
        except:
            traceback.print_exc()
            menu = []

        menus.append(menu)

    html = render_html(args.meal, zip(RESTAURANTS, menus))

    telegram_send.send(
        messages=[html],
        parse_mode="html",
        disable_web_page_preview=True,
        conf=args.telegram_send_conf,
    )

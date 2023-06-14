import datetime
from typing import Sequence, Tuple
from sources import DataSource, Dish, display_dishes
from sources.garden_restaurant import GardenRestaurant
from html import escape
import telegram_send
import argparse


def render_html(meal: str, restaurants: Sequence[Tuple[DataSource, Sequence[Dish]]]) -> str:
    date = datetime.date.today().strftime("%d %b %Y")
    html = f"<i>What to eat for {meal} on {date}</i>\n\n"
    for restaurant, dishes in restaurants:
        html += f'<b><a href="{restaurant.link}">{escape(restaurant.name)}</a></b>\n'
        html += display_dishes(dishes)
        html += "\n"
    return html


RESTAURANTS = [GardenRestaurant()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("meal", choices=["lunch", "dinner"])
    args = parser.parse_args()

    dishes = [restaurant.get_lunch() if args.meal == "lunch" else restaurant.get_dinner()
              for restaurant in RESTAURANTS]

    html = render_html(args.meal, zip(RESTAURANTS, dishes))

    telegram_send.send(
        messages=[html], parse_mode="html", disable_web_page_preview=True)

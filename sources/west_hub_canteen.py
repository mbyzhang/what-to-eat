import datetime
import traceback
from typing import Optional, Sequence, Tuple
from . import DataSource, Dish, DishCategory
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
import fitz


class WestHubCanteen(DataSource):
    @property
    def name(self) -> str:
        return "↔️ West Hub Canteen"

    @property
    def link(self) -> Optional[str]:
        return "https://www.westcambridgehub.uk/canteen"

    def get_data(self, weekday: int) -> str:
        page = requests.get("https://www.westcambridgehub.uk/canteen")
        b = BeautifulSoup(page.text, "html.parser")
        link = b.select_one(
            "#block-sfh-content > article > div.content > div > div:nth-child(2) > div > div > div > div > div > div > div > a").attrs["href"]
        doc = fitz.open("pdf", requests.get(link).content)

        coords = [
            fitz.Rect(220, 180, 612, 290),
            fitz.Rect(220, 290, 612, 410),
            fitz.Rect(220, 410, 612, 540),
            fitz.Rect(220, 540, 612, 660),
            fitz.Rect(220, 660, 612, 1000)
        ]

        coord = coords[weekday]
        menu = doc[0].get_textbox(coord)
        return menu

    def get_lunch(self) -> Sequence[Dish]:
        weekday = datetime.date.today().weekday()
        if weekday >= 5:
            return []

        return self.parse(self.get_data(weekday=weekday))

    def get_dinner(self) -> Sequence[Dish]:
        return []

    @staticmethod
    def parse(s: str) -> Sequence[Dish]:
        s = re.sub(r"\n([a-z])", r"\1", s)
        return [Dish(name.strip(), None) for name in s.split("\n") if name.strip() != ""]

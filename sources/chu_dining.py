import datetime
import random
from typing import Optional, Sequence, Tuple
from . import DataSource, Dish, DishCategory
import requests
from bs4 import BeautifulSoup
import unicodedata


user_agents_list = [
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
]


class ChuDining(DataSource):
    @property
    def name(self) -> str:
        return "Churchill Dining"

    @property
    def link(self) -> Optional[str]:
        return "https://www.chu.cam.ac.uk/student-hub/college-dining/menus"

    def get_data(self, weekday: int) -> Tuple[str, str]:
        page = requests.get(
            "https://www.chu.cam.ac.uk/student-hub/college-dining/menus",
            headers={"User-Agent": random.choice(user_agents_list)},
        )

        b = BeautifulSoup(page.text, "html.parser")

        lunch = b.find("div", class_="menu-content", id=f"lunch-menu-{weekday+1}").text
        dinner = b.find(
            "div", class_="menu-content", id=f"dinner-menu-{weekday+1}"
        ).text

        return lunch, dinner

    def get_lunch(self) -> Sequence[Dish]:
        weekday = datetime.date.today().weekday()

        return self.parse(self.get_data(weekday=weekday)[0])

    def get_dinner(self) -> Sequence[Dish]:
        weekday = datetime.date.today().weekday()

        return self.parse(self.get_data(weekday=weekday)[1])

    @staticmethod
    def parse(s: str) -> Sequence[Dish]:
        s = unicodedata.normalize("NFKD", s).strip("\n ")
        return [Dish(name, None) for name in s.split("\n") if name != ""]

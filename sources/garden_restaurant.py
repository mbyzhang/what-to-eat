from typing import Optional, Sequence, Tuple
from . import DataSource, Dish, DishCategory
import requests
from bs4 import BeautifulSoup
import re


class GardenRestaurant(DataSource):
    @property
    def name(self) -> str:
        return "🏡 Garden Restaurant"

    @property
    def link(self) -> Optional[str]:
        return "https://www.robinson.cam.ac.uk/college-life/garden-restaurant-menu"

    def find_menu(self, b: BeautifulSoup, keyword: str) -> Optional[str]:
        for elem in b.select(".menuColumn"):
            h3 = elem.select_one("h3")
            if h3 and keyword == h3.text:
                menu = elem.select_one(".menuItem")
                return "\n".join(filter(lambda x: isinstance(x, str), menu.children))
        return None

    def get_data(self) -> Tuple[str, str]:
        page = requests.get(
            "https://www.robinson.cam.ac.uk/college-life/garden-restaurant-menu")
        b = BeautifulSoup(page.text, "html.parser")
        lunch = self.find_menu(b, "On Offer for Lunch")
        dinner = self.find_menu(b, "On Offer for Dinner")
        return lunch, dinner

    def get_lunch(self) -> str:
        return self.parse(self.get_data()[0])

    def get_dinner(self) -> str:
        return self.parse(self.get_data()[1])

    @classmethod
    def parse(cls, s: str) -> Sequence[Dish]:
        s = re.sub(r"\r\n", "\n", s)
        s = re.sub(r"\n£", " £", s)
        s = re.sub(r" +", " ", s)
        s = re.sub(r"(?m)^\s+", "", s)
        s = re.sub(r"\n+", "\n", s)

        return [Dish(name) for name in re.findall(r"(?m)^([\w ,]+)", s)]

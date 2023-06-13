from typing import Sequence, Tuple
from . import DataSource, Dish, DishCategory
import requests
from bs4 import BeautifulSoup
import re


class GardenRestaurant(DataSource):
    @property
    def name(self) -> str:
        return "🏡 Garden Restaurant"

    def get_data(self) -> Tuple[str, str]:
        page = requests.get(
            "https://www.robinson.cam.ac.uk/college-life/garden-restaurant-menu")
        b = BeautifulSoup(page.text, "html.parser")
        lunch = b.select_one(
            "#content > div > div > article > div > div > div:nth-child(6) > div").text
        dinner = b.select_one(
            "#content > div > div > article > div > div > div:nth-child(7) > div").text
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

        return [Dish(name, float(price)) for name, price in re.findall(r"(?m)^([\w ,]+) £([0-9.]+) /", s)]

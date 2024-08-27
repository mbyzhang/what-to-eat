from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence
from enum import Enum
import re


class DishCategory(Enum):
    DESSERT = "dessert"
    CHICKEN = "chicken"
    BEEF = "beef"
    VEGAN = "vegan"
    LAMB = "lamb"
    PORK = "pork"  # pork / gammon
    FISH = "fish"  # fish / plaice / cod
    POTATO = "potato"
    CARROT = "carrot"
    RICE = "rice"
    PASTA = "pasta"
    SALAD = "salad"
    FRITTATA = "frittata"
    PIZZA = "pizza"
    MUSHROOM = "mushroom"
    TOFU = "tofu"
    SPAGHETTI = "spaghetti"
    UNKNOWN = "unknown"

    @property
    def emoji(self) -> str:
        return {
            self.CHICKEN: "🐔",
            self.BEEF: "🐂",
            self.LAMB: "🐑",
            self.PORK: "🐷",
            self.FISH: "🐟",
            self.DESSERT: "🍰",
            self.VEGAN: "🥬",
            self.POTATO: "🥔",
            self.CARROT: "🥕",
            self.RICE: "🍚",
            self.PASTA: "🍝",
            self.SALAD: "🥗",
            self.FRITTATA: "🥘",
            self.PIZZA: "🍕",
            self.MUSHROOM: "🍄",
            self.TOFU: "🧈",
            self.SPAGHETTI: "🍝",
            self.UNKNOWN: "❓",
        }[self]


@dataclass
class Dish:
    name: str
    price: Optional[float] = None

    @property
    def category(self) -> DishCategory:
        tokens = re.sub(r"\W+", " ", self.name.lower()).split(" ")

        keywords = [
            (DishCategory.CHICKEN, ["chicken", "turkey"]),
            (DishCategory.BEEF, ["beef"]),
            (DishCategory.LAMB, ["lamb"]),
            (DishCategory.PORK, ["pork", "gammon"]),
            (DishCategory.FISH, ["fish", "plaice", "cod", "haddock"]),
            (DishCategory.DESSERT, ["cake", "dessert"]),
            (DishCategory.POTATO, ["potato", "potatoes", "chips", "fries"]),
            (DishCategory.CARROT, ["carrot", "carrots"]),
            (DishCategory.RICE, ["rice"]),
            (DishCategory.PASTA, ["pasta"]),
            (DishCategory.SALAD, ["salad"]),
            (DishCategory.FRITTATA, ["frittata"]),
            (DishCategory.PIZZA, ["pizza"]),
            (DishCategory.MUSHROOM, ["mushroom"]),
            (DishCategory.TOFU, ["tofu"]),
            (DishCategory.SPAGHETTI, ["spaghetti"]),
            (DishCategory.VEGAN, ["vegetable", "vg", "vegetables"]),
        ]

        for cat, kws in keywords:
            if any(map(lambda w: w in kws, tokens)):
                return cat

        return DishCategory.UNKNOWN

    def display(self) -> str:
        s = f"{self.category.emoji} {self.name}"

        if self.price is not None:
            s += f": £{self.price}"

        return s


def display_dishes(d: Sequence[Dish]) -> str:
    return "\n".join(map(lambda d: d.display(), d))


class DataSource(ABC):
    @property
    def name(self) -> str:
        pass

    @property
    def link(self) -> Optional[str]:
        return None

    @abstractmethod
    def get_lunch(self) -> Sequence[Dish]:
        pass

    @abstractmethod
    def get_dinner(self) -> Sequence[Dish]:
        pass
